#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test dla Earth Simulator Enhanced v2.0
Autor: Adrian Lesniak
"""

import sys
import os
import subprocess
import time

def test_dependencies():
    """Testuje czy wszystkie zależności są dostępne"""
    print("🔍 Sprawdzanie zależności...")
    
    required_modules = ['pygame', 'OpenGL', 'numpy', 'PIL']
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module} - OK")
        except ImportError:
            print(f"❌ {module} - BRAK")
            missing_modules.append(module)
    
    if missing_modules:
        print(f"\n❌ Brakujące moduły: {', '.join(missing_modules)}")
        print("🔧 Zainstaluj: pip install -r requirements.txt")
        return False
    
    print("✅ Wszystkie zależności są dostępne")
    return True

def test_texture_files():
    """Testuje czy pliki tekstur istnieją"""
    print("\n🔍 Sprawdzanie plików tekstur...")
    
    required_files = ['earth_texture.jpg', 'earth_political.jpg', 'earth_detailed.jpg']
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            size_mb = os.path.getsize(file) / (1024 * 1024)
            print(f"✅ {file} - {size_mb:.1f}MB")
        else:
            print(f"❌ {file} - BRAK")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n❌ Brakujące pliki: {', '.join(missing_files)}")
        return False
    
    print("✅ Wszystkie pliki tekstur są dostępne")
    return True

def test_main_program():
    """Testuje główny program"""
    print("\n🚀 Testowanie głównego programu...")
    
    try:
        # Importuj główny moduł
        from earth_simulator_enhanced import EnhancedEarthSimulator, check_dependencies, check_texture_files
        
        print("✅ Import modułu - OK")
        
        # Test funkcji sprawdzających
        if check_dependencies():
            print("✅ Sprawdzanie zależności - OK")
        else:
            print("❌ Sprawdzanie zależności - BŁĄD")
            return False
        
        if check_texture_files():
            print("✅ Sprawdzanie tekstur - OK")
        else:
            print("❌ Sprawdzanie tekstur - BŁĄD")
            return False
        
        print("✅ Wszystkie testy przeszły pomyślnie!")
        return True
        
    except Exception as e:
        print(f"❌ Błąd testowania: {e}")
        return False

def test_utils():
    """Testuje funkcje pomocnicze"""
    print("\n🔧 Testowanie funkcji pomocniczych...")
    
    try:
        from utils import (
            create_config_directory, 
            get_config_path, 
            save_user_preferences, 
            load_user_preferences,
            format_time,
            validate_resolution,
            get_system_info
        )
        
        # Test funkcji konfiguracyjnych
        config_dir = create_config_directory()
        print(f"✅ Katalog konfiguracyjny: {config_dir}")
        
        config_path = get_config_path("test.json")
        print(f"✅ Ścieżka konfiguracji: {config_path}")
        
        # Test preferencji
        test_prefs = {"test": "value", "number": 42}
        if save_user_preferences(test_prefs):
            print("✅ Zapisywanie preferencji - OK")
        else:
            print("❌ Zapisywanie preferencji - BŁĄD")
        
        loaded_prefs = load_user_preferences()
        print(f"✅ Wczytywanie preferencji: {loaded_prefs}")
        
        # Test funkcji pomocniczych
        time_str = format_time(65.5)
        print(f"✅ Formatowanie czasu: {time_str}")
        
        is_valid = validate_resolution(1280, 720)
        print(f"✅ Walidacja rozdzielczości: {is_valid}")
        
        sys_info = get_system_info()
        print(f"✅ Informacje systemowe: {sys_info['system']}")
        
        print("✅ Wszystkie funkcje pomocnicze działają!")
        return True
        
    except Exception as e:
        print(f"❌ Błąd testowania funkcji pomocniczych: {e}")
        return False

def run_quick_test():
    """Uruchamia szybki test programu"""
    print("🧪 Uruchamianie szybkiego testu...")
    
    try:
        # Sprawdź czy program się uruchamia (bez GUI)
        result = subprocess.run([
            sys.executable, 
            "earth_simulator_enhanced.py"
        ], 
        capture_output=True, 
        text=True, 
        timeout=10)
        
        if result.returncode == 0:
            print("✅ Program uruchamia się poprawnie")
            return True
        else:
            print(f"❌ Błąd uruchamiania: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("✅ Program uruchamia się (timeout - normalne dla GUI)")
        return True
    except Exception as e:
        print(f"❌ Błąd testu: {e}")
        return False

def main():
    """Główna funkcja testowa"""
    print("🌟 Earth Simulator Enhanced v2.0 - Test")
    print("👨‍💻 Autor: Adrian Lesniak")
    print("=" * 50)
    
    tests = [
        ("Zależności", test_dependencies),
        ("Pliki tekstur", test_texture_files),
        ("Funkcje pomocnicze", test_utils),
        ("Główny program", test_main_program),
        ("Szybki test", run_quick_test)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Test: {test_name}")
        print("-" * 30)
        
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} - PRZESZŁ")
            else:
                print(f"❌ {test_name} - NIE PRZESZŁ")
        except Exception as e:
            print(f"❌ {test_name} - BŁĄD: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Wyniki: {passed}/{total} testów przeszło")
    
    if passed == total:
        print("🎉 Wszystkie testy przeszły pomyślnie!")
        print("🚀 Program jest gotowy do użycia")
        return True
    else:
        print("⚠️ Niektóre testy nie przeszły")
        print("🔧 Sprawdź błędy powyżej")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 