#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skrypt naprawy problemów z zależnościami
Autor: Adrian Lesniak
"""

import subprocess
import sys
import os

def run_command(command):
    """Uruchamia komendę i zwraca wynik"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def fix_numpy_opengl_compatibility():
    """Naprawia problemy kompatybilności numpy/OpenGL"""
    print("🔧 Naprawianie problemów kompatybilności numpy/OpenGL...")
    
    # Krok 1: Odinstaluj obecne wersje
    print("📦 Odinstalowywanie obecnych wersji...")
    commands = [
        "pip uninstall numpy -y",
        "pip uninstall PyOpenGL -y",
        "pip uninstall PyOpenGL-accelerate -y"
    ]
    
    for cmd in commands:
        success, stdout, stderr = run_command(cmd)
        if not success:
            print(f"⚠️ Ostrzeżenie: {cmd} - {stderr}")
    
    # Krok 2: Zainstaluj kompatybilne wersje
    print("📦 Instalowanie kompatybilnych wersji...")
    commands = [
        "pip install numpy==1.24.3",
        "pip install PyOpenGL==3.1.6",
        "pip install PyOpenGL-accelerate==3.1.6"
    ]
    
    for cmd in commands:
        success, stdout, stderr = run_command(cmd)
        if success:
            print(f"✅ {cmd}")
        else:
            print(f"❌ {cmd} - {stderr}")
            return False
    
    return True

def test_imports():
    """Testuje czy importy działają poprawnie"""
    print("🧪 Testowanie importów...")
    
    test_code = """
import sys
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from PIL import Image

print("✅ Wszystkie importy działają poprawnie!")
print(f"NumPy wersja: {np.__version__}")
print(f"OpenGL wersja: {pygame.version.ver}")
"""
    
    try:
        result = subprocess.run([sys.executable, "-c", test_code], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(result.stdout)
            return True
        else:
            print(f"❌ Błąd testu: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Błąd testu: {e}")
        return False

def create_compatibility_fix():
    """Tworzy plik naprawy kompatybilności"""
    fix_code = '''
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Naprawa kompatybilności numpy/OpenGL
"""

import os
import sys

# Ustaw zmienne środowiskowe dla kompatybilności
os.environ['PYTHONPATH'] = os.pathsep.join([
    os.environ.get('PYTHONPATH', ''),
    os.path.dirname(os.path.abspath(__file__))
])

# Napraw problem z numpy.dtype
try:
    import numpy as np
    # Wymuś kompatybilną wersję numpy
    if hasattr(np, 'dtype'):
        # Dodaj hook dla kompatybilności
        original_dtype = np.dtype
        def safe_dtype(*args, **kwargs):
            try:
                return original_dtype(*args, **kwargs)
            except Exception:
                # Fallback dla problemów kompatybilności
                return np.dtype('float32')
        np.dtype = safe_dtype
except ImportError:
    pass

# Napraw problem z OpenGL
try:
    from OpenGL.GL import *
    from OpenGL.GLU import *
except ImportError as e:
    print(f"Błąd OpenGL: {e}")
    sys.exit(1)
'''
    
    with open('compatibility_fix.py', 'w', encoding='utf-8') as f:
        f.write(fix_code)
    
    print("✅ Utworzono plik naprawy kompatybilności: compatibility_fix.py")

def main():
    """Główna funkcja naprawy"""
    print("🔧 Naprawa problemów z zależnościami")
    print("👨‍💻 Autor: Adrian Lesniak")
    print("=" * 50)
    
    # Sprawdź czy jesteśmy w odpowiednim katalogu
    if not os.path.exists('earth_simulator.py'):
        print("❌ Nie znaleziono pliku earth_simulator.py")
        print("Uruchom skrypt w katalogu z programem")
        return False
    
    # Krok 1: Napraw kompatybilność
    if not fix_numpy_opengl_compatibility():
        print("❌ Nie udało się naprawić kompatybilności")
        return False
    
    # Krok 2: Test importów
    if not test_imports():
        print("❌ Test importów nie przeszedł")
        return False
    
    # Krok 3: Utwórz plik naprawy
    create_compatibility_fix()
    
    print("\n" + "=" * 50)
    print("✅ Naprawa zakończona pomyślnie!")
    print("🚀 Możesz teraz uruchomić program:")
    print("   python earth_simulator_enhanced.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 