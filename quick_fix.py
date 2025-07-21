#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Szybka naprawa problemów z zależnościami
Autor: Adrian Lesniak
"""

import subprocess
import sys
import os

def run_pip_command(command):
    """Uruchamia komendę pip"""
    print(f"🔧 Wykonuję: {command}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {command} - SUKCES")
            return True
        else:
            print(f"❌ {command} - BŁĄD: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {command} - WYJĄTEK: {e}")
        return False

def main():
    print("🔧 Szybka naprawa problemów z zależnościami")
    print("👨‍💻 Autor: Adrian Lesniak")
    print("=" * 50)
    
    # Lista komend do wykonania
    commands = [
        "pip uninstall numpy -y",
        "pip uninstall PyOpenGL -y", 
        "pip uninstall PyOpenGL-accelerate -y",
        "pip install numpy==1.24.3",
        "pip install PyOpenGL==3.1.6",
        "pip install PyOpenGL-accelerate==3.1.6"
    ]
    
    success_count = 0
    total_commands = len(commands)
    
    for cmd in commands:
        if run_pip_command(cmd):
            success_count += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Wyniki: {success_count}/{total_commands} komend przeszło")
    
    if success_count == total_commands:
        print("✅ Wszystkie komendy przeszły pomyślnie!")
        print("🧪 Testowanie importów...")
        
        # Test importów
        test_code = """
import sys
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from PIL import Image

print("✅ Wszystkie importy działają poprawnie!")
print(f"NumPy wersja: {np.__version__}")
print("OpenGL: OK")
print("Pygame: OK")
print("PIL: OK")
"""
        
        try:
            result = subprocess.run([sys.executable, "-c", test_code], 
                                  capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                print(result.stdout)
                print("🎉 Naprawa zakończona pomyślnie!")
                print("🚀 Możesz teraz uruchomić program:")
                print("   python earth_simulator_enhanced.py")
                return True
            else:
                print(f"❌ Test importów nie przeszedł: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ Błąd testu: {e}")
            return False
    else:
        print("❌ Nie wszystkie komendy przeszły")
        print("🔧 Spróbuj uruchomić komendy ręcznie")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 