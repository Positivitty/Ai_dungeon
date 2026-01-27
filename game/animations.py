"""
Animation system for visual effects
Handles scale, shake, flash, and other animations
"""

import pygame
import math
import random


class Animation:
    """Base animation class"""

    def __init__(self, duration=1.0):
        """
        Initialize animation

        Args:
            duration: How long animation lasts in seconds
        """
        self.duration = duration
        self.elapsed = 0
        self.active = True

    def update(self, dt):
        """Update animation state"""
        if not self.active:
            return

        self.elapsed += dt
        if self.elapsed >= self.duration:
            self.active = False

    @property
    def progress(self):
        """Get animation progress (0 to 1)"""
        return min(1.0, self.elapsed / max(0.001, self.duration))


class ScaleAnimation(Animation):
    """Pop/bounce scale effect"""

    def __init__(self, target, scale_peak=1.3, duration=0.2):
        """
        Initialize scale animation

        Args:
            target: Object with width/height to animate
            scale_peak: Maximum scale factor
            duration: Animation duration
        """
        super().__init__(duration)
        self.target = target
        self.scale_peak = scale_peak
        self.original_width = getattr(target, 'width', 48)
        self.original_height = getattr(target, 'height', 48)

    def update(self, dt):
        """Update scale animation"""
        super().update(dt)

        if not self.active:
            # Reset to original size
            if hasattr(self.target, 'width'):
                self.target.width = self.original_width
            if hasattr(self.target, 'height'):
                self.target.height = self.original_height
            return

        # Calculate scale using sine curve for smooth bounce
        # Goes from 1 -> peak -> 1
        t = self.progress
        scale = 1.0 + (self.scale_peak - 1.0) * math.sin(t * math.pi)

        # Apply to target
        if hasattr(self.target, 'width'):
            self.target.width = int(self.original_width * scale)
        if hasattr(self.target, 'height'):
            self.target.height = int(self.original_height * scale)

    def get_scale(self):
        """Get current scale factor"""
        if not self.active:
            return 1.0
        t = self.progress
        return 1.0 + (self.scale_peak - 1.0) * math.sin(t * math.pi)


class ShakeAnimation(Animation):
    """Screen shake effect"""

    def __init__(self, intensity=10, duration=0.3, decay=True):
        """
        Initialize shake animation

        Args:
            intensity: Maximum shake offset in pixels
            duration: How long shake lasts
            decay: Whether shake decreases over time
        """
        super().__init__(duration)
        self.intensity = intensity
        self.decay = decay
        self.offset_x = 0
        self.offset_y = 0

    def update(self, dt):
        """Update shake animation"""
        super().update(dt)

        if not self.active:
            self.offset_x = 0
            self.offset_y = 0
            return

        # Calculate current intensity (with optional decay)
        if self.decay:
            current_intensity = self.intensity * (1.0 - self.progress)
        else:
            current_intensity = self.intensity

        # Random offset
        self.offset_x = random.uniform(-current_intensity, current_intensity)
        self.offset_y = random.uniform(-current_intensity, current_intensity)

    def get_offset(self):
        """Get current shake offset (x, y)"""
        return (int(self.offset_x), int(self.offset_y))


class FlashAnimation(Animation):
    """Flash overlay effect (for damage, etc)"""

    def __init__(self, color=(255, 0, 0), alpha_peak=100, duration=0.2):
        """
        Initialize flash animation

        Args:
            color: Flash color (R, G, B)
            alpha_peak: Maximum alpha value
            duration: Flash duration
        """
        super().__init__(duration)
        self.color = color
        self.alpha_peak = alpha_peak

    def get_alpha(self):
        """Get current flash alpha"""
        if not self.active:
            return 0

        # Quick flash then fade
        t = self.progress
        # Peaks early then fades
        if t < 0.2:
            return int(self.alpha_peak * (t / 0.2))
        else:
            return int(self.alpha_peak * (1.0 - (t - 0.2) / 0.8))

    def draw(self, surface, rect):
        """
        Draw flash overlay on a rect

        Args:
            surface: Surface to draw on
            rect: Area to flash
        """
        if not self.active:
            return

        alpha = self.get_alpha()
        if alpha <= 0:
            return

        flash_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        flash_surface.fill((*self.color, alpha))
        surface.blit(flash_surface, rect.topleft)


class PulseAnimation(Animation):
    """Continuous pulsing glow effect"""

    def __init__(self, frequency=2.0, min_alpha=50, max_alpha=150):
        """
        Initialize pulse animation

        Args:
            frequency: Pulses per second
            min_alpha: Minimum glow alpha
            max_alpha: Maximum glow alpha
        """
        super().__init__(duration=float('inf'))  # Infinite duration
        self.frequency = frequency
        self.min_alpha = min_alpha
        self.max_alpha = max_alpha
        self.active = True  # Always active until manually stopped

    def update(self, dt):
        """Update pulse animation"""
        self.elapsed += dt
        # Don't deactivate

    def get_alpha(self):
        """Get current pulse alpha"""
        # Use sine wave for smooth pulsing
        t = self.elapsed * self.frequency * math.pi * 2
        normalized = (math.sin(t) + 1) / 2  # 0 to 1
        return int(self.min_alpha + (self.max_alpha - self.min_alpha) * normalized)


class BobAnimation(Animation):
    """Floating bob effect (for items)"""

    def __init__(self, amplitude=3, frequency=2.0):
        """
        Initialize bob animation

        Args:
            amplitude: Maximum vertical offset
            frequency: Bobs per second
        """
        super().__init__(duration=float('inf'))  # Infinite
        self.amplitude = amplitude
        self.frequency = frequency
        self.offset_y = 0

    def update(self, dt):
        """Update bob animation"""
        self.elapsed += dt
        t = self.elapsed * self.frequency * math.pi * 2
        self.offset_y = math.sin(t) * self.amplitude

    def get_offset(self):
        """Get current vertical offset"""
        return self.offset_y


class AnimationManager:
    """Manages all active animations"""

    def __init__(self):
        """Initialize animation manager"""
        self.animations = []
        self.screen_shake = None
        self.screen_flash = None
        self.entity_flashes = {}  # entity_id -> FlashAnimation

    def update(self, dt):
        """Update all animations"""
        # Update generic animations
        for anim in self.animations[:]:
            anim.update(dt)
            if not anim.active:
                self.animations.remove(anim)

        # Update screen shake
        if self.screen_shake:
            self.screen_shake.update(dt)
            if not self.screen_shake.active:
                self.screen_shake = None

        # Update screen flash
        if self.screen_flash:
            self.screen_flash.update(dt)
            if not self.screen_flash.active:
                self.screen_flash = None

        # Update entity flashes
        for entity_id in list(self.entity_flashes.keys()):
            flash = self.entity_flashes[entity_id]
            flash.update(dt)
            if not flash.active:
                del self.entity_flashes[entity_id]

    def add_animation(self, animation):
        """Add a generic animation"""
        self.animations.append(animation)

    def trigger_screen_shake(self, intensity=10, duration=0.3):
        """
        Trigger screen shake effect

        Args:
            intensity: Shake magnitude
            duration: Shake duration
        """
        self.screen_shake = ShakeAnimation(intensity, duration)

    def trigger_screen_flash(self, color=(255, 0, 0), alpha=80, duration=0.15):
        """
        Trigger screen flash effect

        Args:
            color: Flash color
            alpha: Maximum alpha
            duration: Flash duration
        """
        self.screen_flash = FlashAnimation(color, alpha, duration)

    def trigger_entity_flash(self, entity_id, color=(255, 255, 255), duration=0.15):
        """
        Trigger flash on a specific entity

        Args:
            entity_id: Identifier for the entity
            color: Flash color
            duration: Flash duration
        """
        self.entity_flashes[entity_id] = FlashAnimation(color, 150, duration)

    def get_screen_offset(self):
        """Get current screen shake offset"""
        if self.screen_shake and self.screen_shake.active:
            return self.screen_shake.get_offset()
        return (0, 0)

    def draw_screen_flash(self, surface, rect):
        """Draw screen flash if active"""
        if self.screen_flash and self.screen_flash.active:
            self.screen_flash.draw(surface, rect)

    def get_entity_flash(self, entity_id):
        """
        Get flash animation for an entity

        Args:
            entity_id: Entity identifier

        Returns:
            FlashAnimation or None
        """
        return self.entity_flashes.get(entity_id)

    def clear(self):
        """Clear all animations"""
        self.animations.clear()
        self.screen_shake = None
        self.screen_flash = None
        self.entity_flashes.clear()
