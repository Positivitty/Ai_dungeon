"""
Graphics utilities for modern visual effects
Provides rounded rectangles, gradients, shadows, and glow effects
"""

import pygame
import math


def interpolate_color(color1, color2, t):
    """
    Interpolate between two colors

    Args:
        color1: Starting color (R, G, B)
        color2: Ending color (R, G, B)
        t: Interpolation factor (0.0 to 1.0)

    Returns:
        tuple: Interpolated color (R, G, B)
    """
    t = max(0.0, min(1.0, t))
    return (
        int(color1[0] + (color2[0] - color1[0]) * t),
        int(color1[1] + (color2[1] - color1[1]) * t),
        int(color1[2] + (color2[2] - color1[2]) * t)
    )


def draw_rounded_rect(surface, color, rect, radius, border=0, border_color=None):
    """
    Draw a rectangle with rounded corners

    Args:
        surface: pygame Surface to draw on
        color: Fill color (R, G, B) or (R, G, B, A)
        rect: pygame.Rect or (x, y, width, height)
        radius: Corner radius in pixels
        border: Border thickness (0 for no border)
        border_color: Border color (defaults to darker version of fill)
    """
    if not isinstance(rect, pygame.Rect):
        rect = pygame.Rect(rect)

    # Clamp radius to half the smallest dimension
    radius = min(radius, rect.width // 2, rect.height // 2)

    if radius <= 0:
        pygame.draw.rect(surface, color, rect)
        if border > 0:
            border_color = border_color or tuple(max(0, c - 50) for c in color[:3])
            pygame.draw.rect(surface, border_color, rect, border)
        return

    # Create a surface with per-pixel alpha for the rounded rect
    if len(color) == 4:
        temp_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    else:
        temp_surface = pygame.Surface((rect.width, rect.height))
        temp_surface.set_colorkey((0, 0, 0))

    # Draw the rounded rectangle using circles and rects
    pygame.draw.rect(temp_surface, color, (radius, 0, rect.width - 2 * radius, rect.height))
    pygame.draw.rect(temp_surface, color, (0, radius, rect.width, rect.height - 2 * radius))
    pygame.draw.circle(temp_surface, color, (radius, radius), radius)
    pygame.draw.circle(temp_surface, color, (rect.width - radius, radius), radius)
    pygame.draw.circle(temp_surface, color, (radius, rect.height - radius), radius)
    pygame.draw.circle(temp_surface, color, (rect.width - radius, rect.height - radius), radius)

    surface.blit(temp_surface, rect.topleft)

    # Draw border if specified
    if border > 0:
        border_color = border_color or tuple(max(0, c - 50) for c in color[:3])
        # Draw rounded border using arcs and lines
        pygame.draw.arc(surface, border_color, (rect.x, rect.y, radius * 2, radius * 2),
                       math.pi / 2, math.pi, border)
        pygame.draw.arc(surface, border_color, (rect.right - radius * 2, rect.y, radius * 2, radius * 2),
                       0, math.pi / 2, border)
        pygame.draw.arc(surface, border_color, (rect.x, rect.bottom - radius * 2, radius * 2, radius * 2),
                       math.pi, 3 * math.pi / 2, border)
        pygame.draw.arc(surface, border_color, (rect.right - radius * 2, rect.bottom - radius * 2, radius * 2, radius * 2),
                       3 * math.pi / 2, 2 * math.pi, border)
        # Lines
        pygame.draw.line(surface, border_color, (rect.x + radius, rect.y), (rect.right - radius, rect.y), border)
        pygame.draw.line(surface, border_color, (rect.x + radius, rect.bottom - 1), (rect.right - radius, rect.bottom - 1), border)
        pygame.draw.line(surface, border_color, (rect.x, rect.y + radius), (rect.x, rect.bottom - radius), border)
        pygame.draw.line(surface, border_color, (rect.right - 1, rect.y + radius), (rect.right - 1, rect.bottom - radius), border)


def draw_gradient_rect(surface, color_top, color_bottom, rect, radius=0):
    """
    Draw a rectangle with a vertical gradient fill

    Args:
        surface: pygame Surface to draw on
        color_top: Top color (R, G, B)
        color_bottom: Bottom color (R, G, B)
        rect: pygame.Rect or (x, y, width, height)
        radius: Corner radius (0 for sharp corners)
    """
    if not isinstance(rect, pygame.Rect):
        rect = pygame.Rect(rect)

    # Create gradient surface
    gradient_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)

    for y in range(rect.height):
        t = y / max(1, rect.height - 1)
        color = interpolate_color(color_top, color_bottom, t)
        pygame.draw.line(gradient_surface, color, (0, y), (rect.width, y))

    if radius > 0:
        # Apply rounded mask
        mask_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        draw_rounded_rect(mask_surface, (255, 255, 255, 255), (0, 0, rect.width, rect.height), radius)
        gradient_surface.blit(mask_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    surface.blit(gradient_surface, rect.topleft)


def draw_shadow(surface, rect, offset=(4, 4), blur_radius=8, alpha=100):
    """
    Draw a drop shadow behind an element

    Args:
        surface: pygame Surface to draw on
        rect: pygame.Rect or (x, y, width, height) - the element casting the shadow
        offset: (x, y) shadow offset
        blur_radius: Size of the blur effect
        alpha: Shadow opacity (0-255)
    """
    if not isinstance(rect, pygame.Rect):
        rect = pygame.Rect(rect)

    # Create shadow surface larger than rect for blur
    shadow_width = rect.width + blur_radius * 2
    shadow_height = rect.height + blur_radius * 2
    shadow_surface = pygame.Surface((shadow_width, shadow_height), pygame.SRCALPHA)

    # Draw multiple layers for blur effect
    layers = blur_radius // 2 + 1
    for i in range(layers):
        layer_alpha = alpha // layers
        layer_expand = (layers - i) * 2
        layer_rect = pygame.Rect(
            blur_radius - layer_expand // 2,
            blur_radius - layer_expand // 2,
            rect.width + layer_expand,
            rect.height + layer_expand
        )
        pygame.draw.rect(shadow_surface, (0, 0, 0, layer_alpha), layer_rect, border_radius=4)

    # Blit shadow with offset
    shadow_x = rect.x + offset[0] - blur_radius
    shadow_y = rect.y + offset[1] - blur_radius
    surface.blit(shadow_surface, (shadow_x, shadow_y))


def draw_glow(surface, rect, color, intensity=30, radius=10):
    """
    Draw a glow effect around an element

    Args:
        surface: pygame Surface to draw on
        rect: pygame.Rect or (x, y, width, height)
        color: Glow color (R, G, B)
        intensity: Glow brightness (0-255)
        radius: How far the glow extends
    """
    if not isinstance(rect, pygame.Rect):
        rect = pygame.Rect(rect)

    # Create glow surface
    glow_width = rect.width + radius * 2
    glow_height = rect.height + radius * 2
    glow_surface = pygame.Surface((glow_width, glow_height), pygame.SRCALPHA)

    # Draw concentric rectangles with decreasing alpha
    layers = radius // 2 + 1
    for i in range(layers):
        layer_alpha = int(intensity * (1 - i / layers))
        expand = i * 2
        layer_rect = pygame.Rect(
            radius - expand // 2 - i,
            radius - expand // 2 - i,
            rect.width + expand + i * 2,
            rect.height + expand + i * 2
        )
        glow_color = (*color, layer_alpha)
        pygame.draw.rect(glow_surface, glow_color, layer_rect, border_radius=6)

    # Blit glow centered on element
    glow_x = rect.x - radius
    glow_y = rect.y - radius
    surface.blit(glow_surface, (glow_x, glow_y))


def draw_health_bar(surface, x, y, width, height, current, maximum,
                    bar_color_full=(0, 255, 100), bar_color_empty=(255, 50, 50),
                    bg_color=(40, 40, 40), border_color=(80, 80, 80), radius=4):
    """
    Draw a modern health bar with gradient fill

    Args:
        surface: pygame Surface to draw on
        x, y: Position
        width, height: Dimensions
        current: Current health value
        maximum: Maximum health value
        bar_color_full: Color when health is full
        bar_color_empty: Color when health is low
        bg_color: Background color
        border_color: Border color
        radius: Corner radius
    """
    # Draw background
    draw_rounded_rect(surface, bg_color, (x, y, width, height), radius)

    # Calculate fill width
    health_ratio = max(0, min(1, current / max(1, maximum)))
    fill_width = int((width - 4) * health_ratio)

    if fill_width > 0:
        # Interpolate color based on health
        bar_color = interpolate_color(bar_color_empty, bar_color_full, health_ratio)

        # Draw gradient fill
        highlight_color = tuple(min(255, c + 50) for c in bar_color)
        draw_gradient_rect(surface, highlight_color, bar_color,
                          (x + 2, y + 2, fill_width, height - 4), radius - 1)

    # Draw border
    draw_rounded_rect(surface, (0, 0, 0, 0), (x, y, width, height), radius,
                     border=2, border_color=border_color)


def draw_text_with_shadow(surface, text, font, color, pos, shadow_color=(0, 0, 0), shadow_offset=(2, 2)):
    """
    Draw text with a drop shadow

    Args:
        surface: pygame Surface to draw on
        text: Text string to render
        font: pygame.Font object
        color: Text color
        pos: (x, y) position
        shadow_color: Shadow color
        shadow_offset: (x, y) shadow offset
    """
    # Draw shadow
    shadow_surface = font.render(text, True, shadow_color)
    surface.blit(shadow_surface, (pos[0] + shadow_offset[0], pos[1] + shadow_offset[1]))

    # Draw text
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, pos)
