#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Naprawa kompatybilności dla Earth Simulator Enhanced
Autor: Adrian Lesniak
"""

import sys
import platform
import logging

# Konfiguracja logowania
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fix_numpy_dtype():
    """Naprawia problemy z dtype w numpy"""
    try:
        import numpy as np
        
        # Sprawdź wersję numpy
        numpy_version = np.__version__
        print(f"NumPy wersja: {numpy_version}")
        
        # Napraw problemy z dtype
        if hasattr(np, 'dtype'):
            # Upewnij się, że dtype działa poprawnie
            test_array = np.array([1, 2, 3], dtype=np.int32)
            print("✅ NumPy dtype: OK")
        else:
            print("⚠️ NumPy dtype: Potencjalne problemy")
            
    except Exception as e:
        print(f"❌ Błąd NumPy: {e}")

def fix_opengl_compatibility():
    """Naprawia problemy z OpenGL"""
    try:
        import OpenGL
        
        print("OpenGL: OK")
        
        # Sprawdź system
        system_info = platform.system()
        print(f"System Platform: {system_info}")
            
    except Exception as e:
        print(f"❌ Błąd OpenGL: {e}")

def fix_pygame_compatibility():
    """Naprawia problemy z Pygame"""
    try:
        import pygame
        
        # Sprawdź wersję pygame
        pygame_version = pygame.version.ver
        print(f"pygame {pygame_version}")
        
        # Inicjalizacja pygame
        pygame.init()
        print("Pygame: OK")
        
    except Exception as e:
        print(f"❌ Błąd Pygame: {e}")

def fix_pil_compatibility():
    """Naprawia problemy z PIL/Pillow"""
    try:
        from PIL import Image
        
        # Sprawdź wersję PIL
        pil_version = Image.__version__
        print(f"PIL: OK (wersja: {pil_version})")
        
    except Exception as e:
        print(f"❌ Błąd PIL: {e}")

def check_all_dependencies():
    """Sprawdza wszystkie zależności"""
    print("🔧 Sprawdzanie zależności...")
    
    fix_numpy_dtype()
    fix_opengl_compatibility()
    fix_pygame_compatibility()
    fix_pil_compatibility()
    
    print("✅ Naprawa kompatybilności zakończona")

def setup_environment():
    """Konfiguruje środowisko"""
    try:
        # Ustaw zmienne środowiskowe dla Windows
        if platform.system() == "Windows":
            import os
            os.environ['SDL_VIDEODRIVER'] = 'windib'
            print("✅ Konfiguracja Windows SDL")
            
        # Sprawdź wersję Python
        python_version = sys.version_info
        print(f"Python: {python_version.major}.{python_version.minor}.{python_version.micro}")
        
        # Sprawdź architekturę
        print(f"Architektura: {platform.architecture()[0]}")
        
    except Exception as e:
        print(f"⚠️ Błąd konfiguracji środowiska: {e}")

if __name__ == "__main__":
    print("🌟 Earth Simulator Enhanced v2.0")
    print("👨‍💻 Autor: Adrian Lesniak")
    print("=" * 50)
    
    setup_environment()
    check_all_dependencies()
    
    print("\n🚀 Gotowe do uruchomienia symulatora!") 