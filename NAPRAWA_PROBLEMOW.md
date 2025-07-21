# 🔧 Naprawa Problemów - Earth Simulator Enhanced

## 🚨 Problem z Kompatybilnością numpy/OpenGL

Jeśli widzisz błąd:
```
Fatal error: ('numpy.dtype size changed, may indicate binary incompatibility...')
```

To oznacza problem z kompatybilnością wersji numpy i OpenGL.

## 🛠️ Rozwiązanie

### Krok 1: Uruchom Skrypt Naprawy

```bash
python fix_dependencies.py
```

### Krok 2: Alternatywne Rozwiązanie Ręczne

Jeśli skrypt nie działa, wykonaj kroki ręcznie:

```bash
# 1. Odinstaluj obecne wersje
pip uninstall numpy -y
pip uninstall PyOpenGL -y
pip uninstall PyOpenGL-accelerate -y

# 2. Zainstaluj kompatybilne wersje
pip install numpy==1.24.3
pip install PyOpenGL==3.1.6
pip install PyOpenGL-accelerate==3.1.6

# 3. Sprawdź instalację
python -c "import numpy; import OpenGL; print('OK')"
```

### Krok 3: Sprawdź Wersje

```bash
python -c "
import numpy as np
import pygame
from OpenGL.GL import *
print(f'NumPy: {np.__version__}')
print(f'Pygame: {pygame.version.ver}')
print('OpenGL: OK')
"
```

## 🔍 Inne Problemy

### Problem: "eaimport sys" w earth_simulator.py

**Rozwiązanie:** Naprawiono automatycznie. Jeśli nadal występuje:

```python
# Zmień pierwszą linię z:
eaimport sys
# Na:
import sys
```

### Problem: Błędy Lintera

**Rozwiązanie:** Błędy lintera nie wpływają na działanie programu. Możesz je zignorować lub użyć ulepszonej wersji:

```bash
python earth_simulator_enhanced.py
```

### Problem: Brak Plików Tekstur

**Rozwiązanie:** Upewnij się, że masz pliki:
- `earth_texture.jpg`
- `earth_political.jpg` 
- `earth_detailed.jpg`

### Problem: Błędy OpenGL na Windows

**Rozwiązanie:**
1. Zaktualizuj sterowniki karty graficznej
2. Uruchom jako administrator
3. Sprawdź czy karta obsługuje OpenGL 3.0+

## 🧪 Test Naprawy

Uruchom test po naprawie:

```bash
python test_enhanced.py
```

## 📋 Lista Kontrolna

- [ ] Uruchomiono `fix_dependencies.py`
- [ ] NumPy wersja 1.24.3 zainstalowana
- [ ] PyOpenGL wersja 3.1.6 zainstalowana
- [ ] Test importów przeszedł
- [ ] Program uruchamia się bez błędów
- [ ] Interfejs działa poprawnie

## 🆘 Jeśli Problem Nadal Występuje

### Opcja 1: Środowisko Wirtualne

```bash
# Utwórz nowe środowisko
python -m venv earth_simulator_env

# Aktywuj (Windows)
earth_simulator_env\Scripts\activate

# Aktywuj (Linux/macOS)
source earth_simulator_env/bin/activate

# Zainstaluj zależności
pip install -r requirements.txt

# Uruchom program
python earth_simulator_enhanced.py
```

### Opcja 2: Conda (Jeśli Masz Anaconda)

```bash
# Utwórz środowisko conda
conda create -n earth_simulator python=3.10

# Aktywuj
conda activate earth_simulator

# Zainstaluj zależności
pip install -r requirements.txt

# Uruchom program
python earth_simulator_enhanced.py
```

### Opcja 3: Docker (Zaawansowane)

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "earth_simulator_enhanced.py"]
```

## 📞 Wsparcie

Jeśli problem nadal występuje:

1. **Sprawdź logi**: `earth_simulator.log`
2. **Uruchom w trybie debug**: `python -u earth_simulator_enhanced.py`
3. **Sprawdź wersję Python**: `python --version`
4. **Sprawdź system**: Windows/Linux/macOS

## 🎯 Autor

**Adrian Lesniak**  
Twórca Earth Simulator Enhanced v2.0

---

**🌟 Po naprawie program powinien działać bez problemów! 🌟** 