# 🌍 Earth Simulator Enhanced v2.0

## 📋 Opis Programu

**Earth Simulator Enhanced** to zaawansowany symulator 3D Ziemi stworzony przez **Adriana Lesniaka**. Program oferuje interaktywną wizualizację globu ziemskiego z wieloma funkcjami zaawansowanymi.

### ✨ Główne Funkcje

- **Interaktywna rotacja 3D** - płynne obracanie globu myszą
- **Wielokrotne tekstury** - różne widoki Ziemi (terrain, political, detailed)
- **System zapisu/odczytu** - zapisywanie ulubionych pozycji
- **Zaawansowany interfejs** - nowoczesny UI z animacjami
- **Auto-rotacja** - automatyczne obracanie gdy użytkownik nie interaguje
- **System logowania** - szczegółowe logi błędów i wydajności
- **Wieloplatformowa kompatybilność** - działa na Windows, Linux, macOS
- **Pasek menu u góry** - szybki dostęp do 10 nowych funkcji
- **10 nowych funkcji** - zaawansowane możliwości symulatora

## 🚀 Instalacja

### Wymagania Systemowe

- Python 3.8+
- OpenGL 3.0+
- 2GB RAM
- Karta graficzna z obsługą OpenGL

### Instalacja Zależności

```bash
pip install -r requirements.txt
```

### Uruchomienie

```bash
python earth_simulator_enhanced.py
```

## 🎮 Sterowanie

### Mysz
- **Przeciągnij** - obróć glob
- **Kółko** - przybliż/oddal
- **Podwójne kliknięcie** - reset widoku

### Klawiatura
- **M** - menu główne
- **L** - zmień warstwę
- **R** - reset widoku
- **V** - zmień tryb widoku
- **A** - włącz/wyłącz animacje
- **S** - włącz/wyłącz statystyki
- **E** - włącz/wyłącz efekty
- **T** - zrób screenshot
- **ESC** - wyjście z programu

### Pasek Menu (Góra)
- **🌍 Widok** - zmień tryb wyświetlania (Normal/Wireframe/Points/Night)
- **🎬 Animacja** - włącz/wyłącz animacje
- **📊 Statystyki** - wyświetl informacje o programie
- **🎨 Efekty** - włącz/wyłącz efekty wizualne
- **🌙 Atmosfera** - symulacja atmosfery i chmur
- **📸 Screenshot** - zrób zrzut ekranu
- **🎵 Dźwięk** - włącz/wyłącz dźwięk
- **⚙️ Ustawienia** - konfiguracja programu
- **❓ Pomoc** - instrukcje i pomoc
- **❌ Wyjście** - zamknij program

### Menu Główne
- **ℹ️ O Programie** - informacje o symulatorze
- **🎮 Instrukcje** - szczegółowe instrukcje
- **⚙️ Ustawienia** - konfiguracja programu
- **💾 Zapisz Stan** - zapisz obecną pozycję
- **📂 Wczytaj Stan** - wczytaj zapisaną pozycję
- **🔄 Reset Widoku** - przywróć domyślny widok
- **❌ Wyjście** - zamknij program

## 🌟 10 Nowych Funkcji

### 1. 🌍 Tryby Widoku
- **Normal** - standardowy widok z teksturami
- **Wireframe** - siatka 3D bez tekstur
- **Points** - punkty zamiast powierzchni
- **Night** - nocny widok z oświetleniem

### 2. 🎬 Animacje
- **Rotacja** - automatyczne obracanie
- **Orbit** - ruch orbitalny
- **Zoom** - animowane przybliżanie
- **Flyby** - przelot nad globem

### 3. 📊 Statystyki
- **FPS** - klatki na sekundę
- **Tryb widoku** - aktualny tryb
- **Pozycja** - współrzędne rotacji
- **Zoom** - poziom przybliżenia
- **Status funkcji** - włączone/wyłączone

### 4. 🎨 Efekty Wizualne
- **Blending** - przezroczystość
- **Depth testing** - test głębi
- **Wireframe mode** - tryb siatki
- **Points mode** - tryb punktów

### 5. 🌙 Atmosfera
- **Symulacja chmur** - animowane chmury
- **Efekty atmosferyczne** - mgła, pył
- **Oświetlenie** - symulacja światła słonecznego
- **Gradient nieba** - kolor nieba

### 6. 📸 Screenshot
- **Automatyczne nazewnictwo** - data i czas
- **Format PNG** - wysokiej jakości
- **Lokalizacja** - katalog programu
- **Licznik** - numerowanie plików

### 7. 🎵 Dźwięk
- **Włączanie/wyłączanie** - kontrola dźwięku
- **Głośność** - regulacja poziomu
- **Efekty dźwiękowe** - dźwięki interfejsu
- **Muzyka w tle** - opcjonalna

### 8. ⚙️ Ustawienia
- **Konfiguracja** - wszystkie opcje
- **Zapisywanie** - automatyczny zapis
- **Wczytywanie** - przywracanie ustawień
- **Reset** - domyślne wartości

### 9. ❓ Pomoc
- **Instrukcje** - szczegółowe opisy
- **Skróty klawiszowe** - lista skrótów
- **Funkcje** - opis możliwości
- **Autor** - informacje o twórcy

### 10. ❌ Wyjście
- **Bezpieczne zamknięcie** - zapis stanu
- **Czyszczenie zasobów** - zwolnienie pamięci
- **Logowanie** - zapis logów
- **Potwierdzenie** - bezpieczne wyjście

## 🎨 Funkcje Graficzne

### Interfejs Użytkownika
- **Jasne kolory** - nowoczesny schemat kolorów
- **Animacje** - płynne przejścia i efekty hover
- **Ikony** - emoji i symbole dla lepszej UX
- **Tooltips** - podpowiedzi dla przycisków
- **Nagłówek** - informacje o programie i autorze
- **Pasek menu** - szybki dostęp do funkcji

### Tekstury Ziemi
- **Default** - standardowa tekstura terenu
- **Political** - mapa polityczna z granicami państw
- **Detailed** - wysokiej rozdzielczości tekstura terenu

## 📁 Struktura Plików

```
Planet simulator/
├── earth_simulator_enhanced.py  # Główny program
├── utils.py                     # Funkcje pomocnicze
├── requirements.txt             # Zależności
├── README_ENHANCED.md          # Dokumentacja
├── earth_texture.jpg           # Tekstura domyślna
├── earth_political.jpg         # Tekstura polityczna
├── earth_detailed.jpg          # Tekstura szczegółowa
└── earth_simulator.log         # Plik logów
```

## 🔧 Konfiguracja

### Pliki Konfiguracyjne
- `simulator_config.json` - główna konfiguracja
- `user_preferences.json` - preferencje użytkownika
- `earth_simulator.log` - logi programu

### Zmienne Konfiguracyjne
```json
{
  "resolution": [1280, 720],
  "texture": "Default",
  "auto_rotate": true,
  "mouse_sensitivity": 0.2,
  "zoom_sensitivity": 0.1,
  "view_mode": "Normal",
  "animation_enabled": false,
  "effects_enabled": true,
  "sound_enabled": true,
  "atmosphere_enabled": false,
  "last_position": {
    "x": 0,
    "y": 180,
    "distance": -5
  }
}
```

## 🐛 Rozwiązywanie Problemów

### Błędy Instalacji
```bash
# Sprawdź wersję Python
python --version

# Zaktualizuj pip
pip install --upgrade pip

# Zainstaluj zależności
pip install -r requirements.txt
```

### Problemy z OpenGL
- Sprawdź czy karta graficzna obsługuje OpenGL 3.0+
- Zaktualizuj sterowniki karty graficznej
- Sprawdź logi w `earth_simulator.log`

### Problemy z Teksturami
- Upewnij się, że pliki tekstur są w katalogu programu
- Sprawdź czy pliki nie są uszkodzone
- Użyj funkcji `check_texture_files()` w programie

## 📊 Metryki Wydajności

Program loguje następujące metryki:
- Czas wykonania funkcji
- Użycie pamięci
- FPS (klatki na sekundę)
- Błędy i wyjątki

## 🔄 Historia Wersji

### v2.0 (Aktualna)
- ✅ Nowoczesny interfejs z animacjami
- ✅ System zapisu/odczytu konfiguracji
- ✅ Zaawansowane logowanie błędów
- ✅ Wieloplatformowa kompatybilność
- ✅ Dokumentacja kodu
- ✅ Funkcje pomocnicze
- ✅ Optymalizacja wydajności
- ✅ Pasek menu u góry
- ✅ 10 nowych funkcji
- ✅ Tryby widoku
- ✅ Animacje
- ✅ Statystyki
- ✅ Efekty wizualne
- ✅ Atmosfera
- ✅ Screenshot
- ✅ Dźwięk
- ✅ Ustawienia
- ✅ Pomoc
- ✅ Bezpieczne wyjście

### v1.0 (Poprzednia)
- Podstawowa funkcjonalność 3D
- Proste menu
- Podstawowe tekstury

## 👨‍💻 Autor

**Adrian Lesniak**
- Programista Python
- Entuzjasta grafiki 3D
- Twórca Earth Simulator Enhanced

## 📄 Licencja

Program jest udostępniony na licencji MIT. Zobacz plik `LICENSE` dla szczegółów.

## 🤝 Wsparcie

Jeśli napotkasz problemy lub masz sugestie:
1. Sprawdź logi w `earth_simulator.log`
2. Przejrzyj dokumentację
3. Sprawdź wymagania systemowe
4. Zgłoś błąd z szczegółami

## 🎯 Funkcje Przyszłości

- [ ] Dodanie atmosfery i chmur 3D
- [ ] Animacje dzien/noc
- [ ] Więcej tekstur (satelitarne, historyczne)
- [ ] Eksport wideo
- [ ] Tryb VR
- [ ] Wsparcie dla kontrolerów
- [ ] Multiplayer (synchronizacja widoku)
- [ ] Efekty cząsteczkowe
- [ ] Symulacja pogody
- [ ] Integracja z API pogodowym

---

**🌟 Dziękujemy za korzystanie z Earth Simulator Enhanced! 🌟** 