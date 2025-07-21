#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Funkcje pomocnicze dla Earth Simulator Enhanced
Autor: Adrian Lesniak
"""

import os
import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime

def create_config_directory():
    """Tworzy katalog konfiguracyjny jeśli nie istnieje"""
    config_dir = os.path.join(os.path.expanduser("~"), ".earth_simulator")
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    return config_dir

def get_config_path(filename: str) -> str:
    """Zwraca ścieżkę do pliku konfiguracyjnego"""
    config_dir = create_config_directory()
    return os.path.join(config_dir, filename)

def save_user_preferences(preferences: Dict[str, Any]) -> bool:
    """Zapisuje preferencje użytkownika"""
    try:
        config_path = get_config_path("user_preferences.json")
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(preferences, f, indent=2, ensure_ascii=False)
        logging.info("Preferencje użytkownika zapisane")
        return True
    except Exception as e:
        logging.error(f"Błąd zapisu preferencji: {e}")
        return False

def load_user_preferences() -> Dict[str, Any]:
    """Wczytuje preferencje użytkownika"""
    try:
        config_path = get_config_path("user_preferences.json")
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                preferences = json.load(f)
            logging.info("Preferencje użytkownika wczytane")
            return preferences
        else:
            return {}
    except Exception as e:
        logging.error(f"Błąd odczytu preferencji: {e}")
        return {}

def format_time(seconds: float) -> str:
    """Formatuje czas w sekundach na czytelny format"""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}min"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}h"

def validate_resolution(width: int, height: int) -> bool:
    """Sprawdza czy rozdzielczość jest poprawna"""
    min_width, min_height = 800, 600
    max_width, max_height = 2560, 1440
    
    return (min_width <= width <= max_width and 
            min_height <= height <= max_height)

def get_system_info() -> Dict[str, str]:
    """Zwraca informacje o systemie"""
    import platform
    import sys
    
    return {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "python_version": sys.version,
        "python_implementation": platform.python_implementation()
    }

def create_backup(filename: str) -> bool:
    """Tworzy kopię zapasową pliku"""
    try:
        if os.path.exists(filename):
            backup_name = f"{filename}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            import shutil
            shutil.copy2(filename, backup_name)
            logging.info(f"Utworzono kopię zapasową: {backup_name}")
            return True
        return False
    except Exception as e:
        logging.error(f"Błąd tworzenia kopii zapasowej: {e}")
        return False

def check_disk_space(path: str) -> Optional[int]:
    """Sprawdza dostępne miejsce na dysku w MB"""
    try:
        import shutil
        total, used, free = shutil.disk_usage(path)
        return free // (1024 * 1024)  # MB
    except Exception as e:
        logging.error(f"Błąd sprawdzania miejsca na dysku: {e}")
        return None

def sanitize_filename(filename: str) -> str:
    """Czyści nazwę pliku z niebezpiecznych znaków"""
    import re
    # Usuń niebezpieczne znaki
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Usuń spacje na początku i końcu
    filename = filename.strip()
    # Ogranicz długość
    if len(filename) > 255:
        filename = filename[:255]
    return filename

def get_file_size_mb(filepath: str) -> Optional[float]:
    """Zwraca rozmiar pliku w MB"""
    try:
        if os.path.exists(filepath):
            size_bytes = os.path.getsize(filepath)
            return size_bytes / (1024 * 1024)
        return None
    except Exception as e:
        logging.error(f"Błąd sprawdzania rozmiaru pliku: {e}")
        return None

def is_valid_image_file(filepath: str) -> bool:
    """Sprawdza czy plik jest poprawnym obrazem"""
    try:
        from PIL import Image
        with Image.open(filepath) as img:
            img.verify()
        return True
    except Exception:
        return False

def get_memory_usage() -> Dict[str, float]:
    """Zwraca informacje o użyciu pamięci w MB"""
    try:
        import psutil
        process = psutil.Process()
        memory_info = process.memory_info()
        
        return {
            "rss": memory_info.rss / (1024 * 1024),  # Resident Set Size
            "vms": memory_info.vms / (1024 * 1024),  # Virtual Memory Size
            "percent": process.memory_percent()
        }
    except ImportError:
        return {"error": "psutil nie jest zainstalowany"}
    except Exception as e:
        logging.error(f"Błąd sprawdzania pamięci: {e}")
        return {"error": str(e)}

def log_performance_metrics(func):
    """Dekorator do logowania metryk wydajności"""
    import time
    import functools
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        start_memory = get_memory_usage()
        
        try:
            result = func(*args, **kwargs)
            
            end_time = time.time()
            end_memory = get_memory_usage()
            
            execution_time = end_time - start_time
            memory_diff = end_memory.get("rss", 0) - start_memory.get("rss", 0)
            
            logging.info(f"Funkcja {func.__name__}: "
                        f"czas={execution_time:.3f}s, "
                        f"pamięć={memory_diff:.1f}MB")
            
            return result
            
        except Exception as e:
            logging.error(f"Błąd w funkcji {func.__name__}: {e}")
            raise
    
    return wrapper 