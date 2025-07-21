# 🔧 Instrukcje Naprawy Problemów - Krok po Kroku

## 🚨 Problem: Błąd kompatybilności numpy/OpenGL

Jeśli widzisz błąd:
```
Fatal error: ('numpy.dtype size changed, may indicate binary incompatibility...')
```

## 🛠️ Rozwiązanie Krok po Kroku

### Krok 1: Sprawdź wersję Python
```bash
python --version
```
**Wymagana wersja**: Python 3.8+

### Krok 2: Odinstaluj problematyczne pakiety
```bash
pip uninstall numpy -y
pip uninstall PyOpenGL -y
pip uninstall PyOpenGL-accelerate -y
```

### Krok 3: Zainstaluj kompatybilne wersje
```bash
pip install numpy==1.24.3
pip install PyOpenGL==3.1.6
pip install PyOpenGL-accelerate==3.1.6
```

### Krok 4: Sprawdź instalację
```bash
python -c "import numpy; import OpenGL; print('OK')"
```

### Krok 5: Uruchom program
```bash
python earth_simulator_enhanced.py
```

## 🔧 Alternatywne Rozwiązania

### Opcja 1: Użyj ulepszonej wersji
```bash
python earth_simulator_enhanced.py
```

### Opcja 2: Użyj oryginalnej wersji z naprawą
```bash
python earth_simulator.py
```

### Opcja 3: Środowisko wirtualne
```bash
# Utwórz nowe środowisko
python -m venv earth_env

# Aktywuj (Windows)
earth_env\Scripts\activate

# Zainstaluj zależności
pip install -r requirements.txt

# Uruchom program
python earth_simulator_enhanced.py
```

## 🧪 Test Po Naprawie

Uruchom test:
```bash
python test_enhanced.py
```

## 📋 Lista Kontrolna

- [ ] Python 3.8+ zainstalowany
- [ ] NumPy 1.24.3 zainstalowany
- [ ] PyOpenGL 3.1.6 zainstalowany
- [ ] Test importów przeszedł
- [ ] Program uruchamia się bez błędów

## 🆘 Jeśli Problem Nadal Występuje

### Sprawdź logi
```bash
cat earth_simulator.log
```

### Uruchom w trybie debug
```bash
python -u earth_simulator_enhanced.py
```

### Sprawdź wersje pakietów
```bash
pip list | grep -E "(numpy|OpenGL|pygame|Pillow)"
```

## 🎯 Autor

**Adrian Lesniak**  
Twórca Earth Simulator Enhanced v2.0

---

**🌟 Po wykonaniu tych kroków program powinien działać! 🌟** 