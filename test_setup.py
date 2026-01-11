#!/usr/bin/env python3
"""
Test script to verify the project setup
Run this to make sure everything is configured correctly
"""

import sys

def test_imports():
    """Test that all required imports work"""
    print("Testing imports...")
    
    try:
        import pygame
        print("✓ pygame imported successfully")
    except ImportError:
        print("✗ pygame not found - run: pip install pygame==2.5.2")
        return False
    
    try:
        import numpy
        print("✓ numpy imported successfully")
    except ImportError:
        print("✗ numpy not found - run: pip install numpy==1.24.3")
        return False
    
    # These can be installed later for Phase 2
    try:
        import gymnasium
        print("✓ gymnasium imported successfully")
    except ImportError:
        print("⚠ gymnasium not found (needed for Phase 2) - run: pip install gymnasium==0.29.1")
    
    try:
        import stable_baselines3
        print("✓ stable-baselines3 imported successfully")
    except ImportError:
        print("⚠ stable-baselines3 not found (needed for Phase 2) - run: pip install stable-baselines3==2.1.0")
    
    try:
        import torch
        print("✓ torch imported successfully")
    except ImportError:
        print("⚠ torch not found (needed for Phase 2) - run: pip install torch==2.1.0")
    
    return True

def test_config():
    """Test config imports"""
    print("\nTesting configuration...")
    
    try:
        from config import (
            WINDOW_WIDTH, WINDOW_HEIGHT, FPS,
            WEAPONS, ARMORS, ENEMIES
        )
        print(f"✓ Config loaded successfully")
        print(f"  - Window: {WINDOW_WIDTH}x{WINDOW_HEIGHT} @ {FPS} FPS")
        print(f"  - Weapons: {len(WEAPONS)} types")
        print(f"  - Armors: {len(ARMORS)} types")
        print(f"  - Enemies: {len(ENEMIES)} types")
        return True
    except Exception as e:
        print(f"✗ Config import failed: {e}")
        return False

def test_game_classes():
    """Test game class imports"""
    print("\nTesting game classes...")
    
    try:
        from game import Player, spawn_enemy
        print("✓ Game classes imported successfully")
        
        # Create test instances
        player = Player(100, 100, weapon='sword', armor='heavy')
        print(f"  - Player created: {player.weapon} + {player.armor}")
        print(f"  - HP: {player.hp}/{player.max_hp}, Speed: {player.speed}")
        
        goblin = spawn_enemy('goblin', 200, 200)
        print(f"  - Enemy spawned: {goblin.name}")
        print(f"  - HP: {goblin.hp}, Damage: {goblin.damage}")
        
        return True
    except Exception as e:
        print(f"✗ Game class import failed: {e}")
        return False

def test_pygame_window():
    """Test pygame window creation"""
    print("\nTesting pygame window...")
    
    try:
        import pygame
        from config import WINDOW_WIDTH, WINDOW_HEIGHT, TITLE
        
        pygame.init()
        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(TITLE)
        
        print(f"✓ Pygame window created successfully")
        print(f"  - Title: {TITLE}")
        print(f"  - Size: {WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        
        pygame.quit()
        return True
    except Exception as e:
        print(f"✗ Pygame window test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("AI Dungeon Crawler - Setup Test")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_config,
        test_game_classes,
        test_pygame_window
    ]
    
    results = [test() for test in tests]
    
    print("\n" + "=" * 50)
    if all(results):
        print("✓ All tests passed! You're ready to start development.")
        print("\nNext steps:")
        print("1. Run 'python main.py' to see the basic window")
        print("2. Start implementing dungeon generation")
        print("3. Add combat system and manual controls")
    else:
        print("✗ Some tests failed. Please install missing dependencies.")
        print("\nRun: pip install -r requirements.txt")
    print("=" * 50)

if __name__ == "__main__":
    main()
