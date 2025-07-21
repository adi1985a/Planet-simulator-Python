#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Earth Simulator Enhanced v2.0
Autor: Adrian Lesniak
Opis: Zaawansowany symulator 3D Ziemi z interaktywnym interfejsem
Funkcje: Rotacja globu, zmiana tekstur, menu interaktywne, system zapisu/odczytu
"""

# Import naprawy kompatybilności na początku
try:
    import compatibility_fix
except ImportError:
    print("Ostrzeżenie: Nie znaleziono pliku compatibility_fix.py")

import sys
import os
import json
import logging
import platform
import time
import math
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

# Import Pygame i OpenGL po sprawdzeniu zależności
import pygame
from pygame.locals import DOUBLEBUF, OPENGL
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from PIL import Image

# Konfiguracja logowania
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('earth_simulator.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TextureType(Enum):
    """Enum dla typów tekstur"""
    DEFAULT = "Default"
    POLITICAL = "Political"
    DETAILED = "Detailed"

class ViewMode(Enum):
    """Enum dla trybów widoku"""
    NORMAL = "Normal"
    WIREFRAME = "Wireframe"
    POINTS = "Points"
    NIGHT = "Night"

class AnimationType(Enum):
    """Enum dla typów animacji"""
    ROTATION = "Rotation"
    ORBIT = "Orbit"
    ZOOM = "Zoom"
    FLYBY = "Flyby"

@dataclass
class SimulationConfig:
    """Klasa konfiguracji symulacji"""
    resolution: Tuple[int, int] = (1280, 720)
    fov: float = 45.0
    mouse_sensitivity: float = 0.2
    zoom_sensitivity: float = 0.1
    auto_rotate_speed: float = 0.1
    rotation_momentum: float = 0.92

class ColorScheme:
    """Schemat kolorów dla interfejsu"""
    # Jasne kolory dla lepszej widoczności
    BACKGROUND = (240, 240, 245)
    MENU_BG = (255, 255, 255)
    MENU_HEADER = (100, 150, 255)
    BUTTON_NORMAL = (180, 200, 255)
    BUTTON_HOVER = (150, 180, 255)
    BUTTON_BORDER = (100, 130, 200)
    TEXT_PRIMARY = (50, 50, 50)
    TEXT_SECONDARY = (80, 80, 80)
    TEXT_ACCENT = (255, 255, 255)
    SUCCESS = (100, 200, 100)
    WARNING = (255, 200, 100)
    ERROR = (255, 100, 100)
    INFO = (100, 150, 255)
    # Nowe kolory dla paska menu
    TOPBAR_BG = (70, 130, 180)
    TOPBAR_TEXT = (255, 255, 255)
    TOPBAR_BUTTON = (90, 150, 200)
    TOPBAR_BUTTON_HOVER = (110, 170, 220)

class TopMenuBar:
    """Pasek menu u góry z nowymi funkcjami"""
    
    def __init__(self, display_width: int):
        self.display_width = display_width
        self.height = 40
        self.buttons = []
        self.font = pygame.font.Font(None, 24)
        self.setup_buttons()
    
    def setup_buttons(self):
        """Konfiguruje przyciski paska menu"""
        button_width = 120
        spacing = 10
        x = 10
        
        # Przyciski paska menu
        self.buttons = [
            {"text": "🌍 Widok", "action": "view_mode", "x": x},
            {"text": "🎬 Animacja", "action": "animation", "x": x + button_width + spacing},
            {"text": "📊 Statystyki", "action": "stats", "x": x + (button_width + spacing) * 2},
            {"text": "🎨 Efekty", "action": "effects", "x": x + (button_width + spacing) * 3},
            {"text": "🌙 Atmosfera", "action": "atmosphere", "x": x + (button_width + spacing) * 4},
            {"text": "📸 Screenshot", "action": "screenshot", "x": x + (button_width + spacing) * 5},
            {"text": "🎵 Dźwięk", "action": "sound", "x": x + (button_width + spacing) * 6},
            {"text": "⚙️ Ustawienia", "action": "settings", "x": x + (button_width + spacing) * 7},
            {"text": "❓ Pomoc", "action": "help", "x": x + (button_width + spacing) * 8},
            {"text": "❌ Wyjście", "action": "exit", "x": x + (button_width + spacing) * 9}
        ]
    
    def draw(self, surface, colors: ColorScheme):
        """Rysuje pasek menu u góry"""
        # Tło paska menu
        topbar_rect = pygame.Rect(0, 0, self.display_width, self.height)
        pygame.draw.rect(surface, colors.TOPBAR_BG, topbar_rect)
        
        # Linia oddzielająca
        pygame.draw.line(surface, colors.BUTTON_BORDER, 
                        (0, self.height), (self.display_width, self.height), 2)
        
        # Przyciski paska menu
        for button in self.buttons:
            button_rect = pygame.Rect(button["x"], 5, 120, 30)
            
            # Sprawdź hover
            mouse_pos = pygame.mouse.get_pos()
            hovered = button_rect.collidepoint(mouse_pos[0], mouse_pos[1])
            
            # Kolor przycisku
            color = colors.TOPBAR_BUTTON_HOVER if hovered else colors.TOPBAR_BUTTON
            pygame.draw.rect(surface, color, button_rect)
            pygame.draw.rect(surface, colors.TEXT_ACCENT, button_rect, 1)
            
            # Tekst przycisku
            text_surface = self.font.render(button["text"], True, colors.TEXT_ACCENT)
            text_rect = text_surface.get_rect(center=button_rect.center)
            surface.blit(text_surface, text_rect)
    
    def handle_click(self, pos: Tuple[int, int]) -> Optional[str]:
        """Obsługuje kliknięcia w pasek menu"""
        for button in self.buttons:
            button_rect = pygame.Rect(button["x"], 5, 120, 30)
            if button_rect.collidepoint(pos[0], pos[1]):
                return button["action"]
        return None

class EnhancedButton:
    """Ulepszona klasa przycisku z animacjami"""
    
    def __init__(self, x: int, y: int, width: int, height: int, text: str, 
                 icon: Optional[str] = None, tooltip: Optional[str] = None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.icon = icon
        self.tooltip = tooltip
        self.hovered = False
        self.clicked = False
        self.animation_time = 0
        self.original_y = y
        
    def draw(self, surface, font, colors: ColorScheme):
        # Animacja hover
        if self.hovered:
            self.animation_time = min(self.animation_time + 0.2, 1.0)
            y_offset = int(5 * self.animation_time)
        else:
            self.animation_time = max(self.animation_time - 0.2, 0.0)
            y_offset = int(5 * self.animation_time)
        
        # Rysowanie przycisku z gradientem
        color = colors.BUTTON_HOVER if self.hovered else colors.BUTTON_NORMAL
        border_color = colors.BUTTON_BORDER
        
        # Główny prostokąt
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, border_color, self.rect, 2)
        
        # Efekt cienia
        shadow_rect = self.rect.copy()
        shadow_rect.y += 2
        pygame.draw.rect(surface, (200, 200, 200, 100), shadow_rect)
        
        # Tekst z cieniem
        text_surface = font.render(self.text, True, colors.TEXT_PRIMARY)
        shadow_surface = font.render(self.text, True, colors.TEXT_SECONDARY)
        
        text_rect = text_surface.get_rect(center=self.rect.center)
        text_rect.y -= y_offset  # Animacja
        
        surface.blit(shadow_surface, (text_rect.x + 1, text_rect.y + 1))
        surface.blit(text_surface, text_rect)
        
        # Tooltip
        if self.hovered and self.tooltip:
            self.draw_tooltip(surface, font, colors)
    
    def draw_tooltip(self, surface, font, colors):
        tooltip_surface = font.render(self.tooltip, True, colors.TEXT_ACCENT)
        tooltip_bg = pygame.Surface((tooltip_surface.get_width() + 10, 
                                   tooltip_surface.get_height() + 6))
        tooltip_bg.fill(colors.TEXT_PRIMARY)
        tooltip_bg.set_alpha(200)
        
        tooltip_rect = tooltip_bg.get_rect()
        tooltip_rect.centerx = self.rect.centerx
        tooltip_rect.bottom = self.rect.top - 5
        
        surface.blit(tooltip_bg, tooltip_rect)
        surface.blit(tooltip_surface, (tooltip_rect.x + 5, tooltip_rect.y + 3))

    def handle_event(self, event, menu_pos: Tuple[int, int] = (0, 0)) -> bool:
        adjusted_pos = (event.pos[0] - menu_pos[0], event.pos[1] - menu_pos[1])
        
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(adjusted_pos)
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(adjusted_pos):
                self.clicked = True
                return True
                
        elif event.type == pygame.MOUSEBUTTONUP:
            self.clicked = False
            
        return False

class DataManager:
    """Menedżer danych - zapis/odczyt konfiguracji"""
    
    def __init__(self, config_file: str = "simulator_config.json"):
        self.config_file = config_file
        self.default_config = {
            "resolution": [1280, 720],
            "texture": "Default",
            "auto_rotate": True,
            "mouse_sensitivity": 0.2,
            "zoom_sensitivity": 0.1,
            "last_position": {"x": 0, "y": 180, "distance": -5},
            "view_mode": "Normal",
            "animation_enabled": False,
            "sound_enabled": True,
            "effects_enabled": True
        }
    
    def save_config(self, config: Dict) -> bool:
        """Zapisuje konfigurację do pliku"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            logger.info(f"Konfiguracja zapisana do {self.config_file}")
            return True
        except Exception as e:
            logger.error(f"Błąd zapisu konfiguracji: {e}")
            return False
    
    def load_config(self) -> Dict:
        """Wczytuje konfigurację z pliku"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                logger.info(f"Konfiguracja wczytana z {self.config_file}")
                return config
            else:
                logger.info("Brak pliku konfiguracyjnego, używam domyślnych ustawień")
                return self.default_config.copy()
        except Exception as e:
            logger.error(f"Błąd odczytu konfiguracji: {e}")
            return self.default_config.copy()

class EnhancedEarthSimulator:
    """Ulepszony symulator Ziemi z zaawansowanymi funkcjami"""
    
    def __init__(self):
        """Inicjalizacja symulatora"""
        self.setup_pygame()
        self.setup_opengl()
        self.setup_variables()
        self.setup_ui()
        self.setup_textures()
        self.setup_new_features()
        self.data_manager = DataManager()
        self.load_saved_config()
        
        logger.info("Symulator Ziemi zainicjalizowany pomyślnie")
    
    def setup_pygame(self):
        """Konfiguracja Pygame"""
        try:
            pygame.init()
            pygame.mixer.init()
            
            # Sprawdzenie kompatybilności platformy
            try:
                if platform.system() == "Windows":
                    os.environ['SDL_VIDEODRIVER'] = 'windib'
            except Exception as e:
                logger.warning(f"Nie udało się ustawić SDL_VIDEODRIVER: {e}")
            
            self.display = (1280, 720)
            pygame.display.set_caption('Earth Simulator Enhanced v2.0 - Adrian Lesniak')
            
            # Ustawienie ikony (jeśli istnieje)
            try:
                icon = pygame.image.load('earth_icon.png')
                pygame.display.set_icon(icon)
            except:
                pass
                
            self.screen = pygame.display.set_mode(self.display, DOUBLEBUF | OPENGL)
            
        except Exception as e:
            logger.error(f"Błąd inicjalizacji Pygame: {e}")
            raise
    
    def setup_opengl(self):
        """Konfiguracja OpenGL"""
        try:
            glEnable(GL_DEPTH_TEST)
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            
            self.fov = 45
            self.aspect = self.display[0] / self.display[1]
            self.near = 0.1
            self.far = 50.0
            
            self.update_perspective()
            
        except Exception as e:
            logger.error(f"Błąd konfiguracji OpenGL: {e}")
            raise
    
    def setup_variables(self):
        """Inicjalizacja zmiennych symulacji"""
        self.distance = -5
        self.rotation_x = 0
        self.rotation_y = 180
        self.last_pos = None
        self.rotation_velocity = [0.0, 0.0]
        self.auto_rotate = True
        self.auto_rotate_speed = 0.1
        self.mouse_sensitivity = 0.2
        self.zoom_sensitivity = 0.1
        self.rotation_momentum = 0.92
        self.min_zoom = -15
        self.max_zoom = -2
        self.last_click_time = 0
        self.double_click_delay = 300
        
        # Stan menu
        self.show_menu = False
        self.current_section = None
        self.menu_position = self.display[0]
        self.menu_width = 400
        self.menu_height = 600
        self.menu_y = 120  # Przesunięte w dół dla paska menu
        
        # Kolory
        self.colors = ColorScheme()
        
        # Tekstury - inicjalizacja wcześnie
        self.current_texture = 'Default'
        self.texture_files = {
            'Default': 'earth_texture.jpg',
            'Political': 'earth_political.jpg',
            'Detailed': 'earth_detailed.jpg'
        }
        self.textures = {}
        
        # Nowe funkcje - inicjalizacja wcześnie
        self.view_mode = ViewMode.NORMAL
        self.animation_enabled = False
        self.effects_enabled = True
        self.sound_enabled = True
        self.atmosphere_enabled = False
        self.stats_enabled = False
        
        # Zapisz początkową macierz widoku
        self.modelview_matrix = glGetFloatv(GL_MODELVIEW_MATRIX)
    
    def setup_ui(self):
        """Konfiguracja interfejsu użytkownika"""
        # Czcionki
        self.title_font = pygame.font.Font(None, 48)
        self.menu_font = pygame.font.Font(None, 36)
        self.text_font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 20)
        
        # Pasek menu u góry
        self.top_menu = TopMenuBar(self.display[0])
        
        # Przyciski menu
        self.buttons = {
            'main': [
                EnhancedButton(20, 140, 360, 50, "ℹ️ O Programie", 
                             tooltip="Informacje o symulatorze"),
                EnhancedButton(20, 200, 360, 50, "🎮 Instrukcje", 
                             tooltip="Jak korzystać z programu"),
                EnhancedButton(20, 260, 360, 50, "⚙️ Ustawienia", 
                             tooltip="Konfiguracja symulatora"),
                EnhancedButton(20, 320, 360, 50, "💾 Zapisz Stan", 
                             tooltip="Zapisz obecną pozycję"),
                EnhancedButton(20, 380, 360, 50, "📂 Wczytaj Stan", 
                             tooltip="Wczytaj zapisaną pozycję"),
                EnhancedButton(20, 440, 360, 50, "🔄 Reset Widoku", 
                             tooltip="Przywróć domyślny widok"),
                EnhancedButton(20, 500, 360, 50, "❌ Wyjście", 
                             tooltip="Zamknij program")
            ]
        }
        
        # Przyciski górne
        self.menu_btn = EnhancedButton(self.display[0] - 120, 50, 100, 40, "📋 Menu",
                                      tooltip="Otwórz menu główne")
        self.layer_btn = EnhancedButton(self.display[0] - 240, 50, 100, 40, "🌍 Warstwa",
                                       tooltip="Zmień teksturę Ziemi")
        
        # Sekcje menu
        self.menu_sections = {
            'ℹ️ O Programie': [
                "🌟 Earth Simulator Enhanced v2.0",
                "👨‍💻 Autor: Adrian Lesniak",
                "📅 Data: 2024",
                "",
                "✨ Funkcje:",
                "• Interaktywna rotacja 3D",
                "• Różne tekstury Ziemi",
                "• System zapisu/odczytu",
                "• Zaawansowany interfejs",
                "• Animacje i efekty",
                "• Pasek menu u góry",
                "• 10 nowych funkcji"
            ],
            '🎮 Instrukcje': [
                "🖱️ Sterowanie myszą:",
                "• Przeciągnij - obróć glob",
                "• Kółko - przybliż/oddal",
                "• Podwójne kliknięcie - reset",
                "",
                "⌨️ Klawisze:",
                "• M - menu główne",
                "• L - zmień warstwę",
                "• ESC - wyjście",
                "• R - reset widoku",
                "",
                "📋 Pasek menu:",
                "• Widok - zmień tryb wyświetlania",
                "• Animacja - włącz animacje",
                "• Statystyki - informacje o programie",
                "• Efekty - efekty wizualne",
                "• Atmosfera - symulacja atmosfery",
                "• Screenshot - zrób zdjęcie",
                "• Dźwięk - włącz/wyłącz dźwięk",
                "• Ustawienia - konfiguracja",
                "• Pomoc - instrukcje",
                "• Wyjście - zamknij program"
            ],
            '⚙️ Ustawienia': [
                "📊 Aktualne ustawienia:",
                f"• Rozdzielczość: {self.display[0]}x{self.display[1]}",
                f"• Warstwa: {self.current_texture}",
                f"• Tryb widoku: {self.view_mode}",
                f"• Auto-rotacja: {'Włączona' if self.auto_rotate else 'Wyłączona'}",
                f"• Animacje: {'Włączone' if self.animation_enabled else 'Wyłączone'}",
                f"• Efekty: {'Włączone' if self.effects_enabled else 'Wyłączone'}",
                f"• Dźwięk: {'Włączony' if self.sound_enabled else 'Wyłączony'}",
                "",
                "🔧 Dostępne opcje:",
                "• Zmień rozdzielczość",
                "• Dostosuj czułość",
                "• Włącz/wyłącz funkcje",
                "• Zapisz ustawienia"
            ]
        }
        
        self.create_menu_surface()
    
    def setup_textures(self):
        """Konfiguracja tekstur"""
        self.load_all_textures()
    
    def setup_new_features(self):
        """Konfiguracja nowych funkcji"""
        # Animacje
        self.animation_type = AnimationType.ROTATION
        self.animation_speed = 1.0
        self.animation_time = 0
        
        # Efekty
        self.wireframe_mode = False
        self.points_mode = False
        self.night_mode = False
        
        # Statystyki
        self.fps_counter = 0
        self.frame_count = 0
        self.start_time = time.time()
        
        # Screenshot
        self.screenshot_counter = 0
        
        # Dźwięk
        self.sound_volume = 0.5
        
        # Atmosfera
        self.atmosphere_density = 0.1
        self.clouds_enabled = False
    
    def load_saved_config(self):
        """Wczytuje zapisaną konfigurację"""
        config = self.data_manager.load_config()
        
        # Zastosuj zapisane ustawienia
        if 'last_position' in config:
            pos = config['last_position']
            self.rotation_x = pos.get('x', 0)
            self.rotation_y = pos.get('y', 180)
            self.distance = pos.get('distance', -5)
        
        if 'texture' in config:
            self.current_texture = config['texture']
        
        if 'auto_rotate' in config:
            self.auto_rotate = config['auto_rotate']
        
        if 'mouse_sensitivity' in config:
            self.mouse_sensitivity = config['mouse_sensitivity']
        
        if 'view_mode' in config:
            self.view_mode = ViewMode(config['view_mode'])
        if 'animation_enabled' in config:
            self.animation_enabled = config['animation_enabled']
        if 'effects_enabled' in config:
            self.effects_enabled = config['effects_enabled']
        if 'sound_enabled' in config:
            self.sound_enabled = config['sound_enabled']
        if 'atmosphere_enabled' in config:
            self.atmosphere_enabled = config['atmosphere_enabled']
        
        self.update_view_matrix()
    
    def update_perspective(self):
        """Aktualizuje perspektywę OpenGL"""
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(self.fov, self.aspect, self.near, self.far)
        glMatrixMode(GL_MODELVIEW)
    
    def update_view_matrix(self):
        """Aktualizuje macierz widoku"""
        glLoadIdentity()
        glTranslatef(0.0, 0.0, self.distance)
        glRotatef(self.rotation_x, 1, 0, 0)
        glRotatef(self.rotation_y, 0, 1, 0)
        self.modelview_matrix = glGetFloatv(GL_MODELVIEW_MATRIX)
    
    def load_all_textures(self):
        """Ładuje wszystkie tekstury"""
        for name, file in self.texture_files.items():
            try:
                self.textures[name] = self.load_texture(file)
                logger.info(f"Tekstura {name} załadowana pomyślnie")
            except Exception as e:
                logger.error(f"Błąd ładowania tekstury {file}: {e}")
    
    def load_texture(self, filename: str):
        """Ładuje pojedynczą teksturę"""
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(script_dir, filename)
            
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Plik tekstury nie istnieje: {image_path}")
            
            image = Image.open(image_path)
            if image.mode != 'RGBA':
                image = image.convert('RGBA')
            
            image_data = image.tobytes("raw", "RGBA", 0, -1)
            
            texture_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texture_id)
            
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
            
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height,
                        0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
            
            return texture_id
            
        except Exception as e:
            logger.error(f"Błąd ładowania tekstury {filename}: {e}")
            raise
    
    def create_sphere(self, radius: float, segments: int) -> Tuple[List, List, List]:
        """Tworzy sferę z teksturami"""
        vertices = []
        texture_coords = []
        indices = []
        
        for i in range(segments + 1):
            lat = np.pi * (-0.5 + float(i) / segments)
            for j in range(segments + 1):
                lon = 2 * np.pi * float(j) / segments
                x = np.cos(lat) * np.cos(lon)
                y = np.sin(lat)
                z = np.cos(lat) * np.sin(lon)
                
                vertices.append([x * radius, y * radius, z * radius])
                texture_coords.append([1.0 - float(j) / segments, float(i) / segments])
                
        for i in range(segments):
            for j in range(segments):
                indices.append([i * (segments + 1) + j,
                              (i + 1) * (segments + 1) + j,
                              (i + 1) * (segments + 1) + j + 1])
                indices.append([i * (segments + 1) + j,
                              (i + 1) * (segments + 1) + j + 1,
                              i * (segments + 1) + j + 1])
                
        return vertices, texture_coords, indices
    
    def draw_header(self):
        """Rysuje nagłówek z informacjami o programie"""
        # Tło nagłówka
        header_rect = pygame.Rect(0, 0, self.display[0], 70)
        pygame.draw.rect(self.screen, self.colors.MENU_HEADER, header_rect)
        
        # Linia oddzielająca
        pygame.draw.line(self.screen, self.colors.BUTTON_BORDER, 
                        (0, 70), (self.display[0], 70), 3)
        
        # Tytuł programu
        title_text = self.title_font.render("🌟 Earth Simulator Enhanced v2.0", 
                                          True, self.colors.TEXT_ACCENT)
        title_rect = title_text.get_rect(midleft=(20, 35))
        self.screen.blit(title_text, title_rect)
        
        # Autor
        author_text = self.text_font.render("👨‍💻 Autor: Adrian Lesniak", 
                                          True, self.colors.TEXT_ACCENT)
        author_rect = author_text.get_rect(midright=(self.display[0] - 20, 35))
        self.screen.blit(author_text, author_rect)
        
        # Gwiazdki dekoracyjne
        for i in range(5):
            star_x = 400 + i * 80
            star_text = self.small_font.render("⭐", True, self.colors.TEXT_ACCENT)
            star_rect = star_text.get_rect(center=(star_x, 35))
            self.screen.blit(star_text, star_rect)
    
    def draw(self):
        """Główna funkcja rysowania"""
        glClear(int(GL_COLOR_BUFFER_BIT) | int(GL_DEPTH_BUFFER_BIT))
        
        # Przywróć zapisaną macierz widoku
        glLoadMatrixf(self.modelview_matrix)
        
        # Rysuj Ziemię
        self.draw_earth()
        
        # Przełącz na 2D dla interfejsu
        self.setup_2d_mode()
        
        # Rysuj interfejs
        self.draw_header()
        self.draw_menu_button()
        self.top_menu.draw(self.screen, self.colors)
        
        if self.show_menu:
            self.draw_menu()
        
        # Przywróć 3D
        self.setup_3d_mode()
        
        pygame.display.flip()
    
    def draw_earth(self):
        """Rysuje model Ziemi"""
        vertices, texture_coords, indices = self.create_sphere(2, 32)
        glEnable(GL_TEXTURE_2D)
        
        current_tex = self.textures.get(self.current_texture)
        if current_tex:
            glBindTexture(GL_TEXTURE_2D, current_tex)
        
        glPushMatrix()
        glRotatef(self.rotation_x, 1, 0, 0)
        glRotatef(self.rotation_y, 0, 1, 0)
        
        glBegin(GL_TRIANGLES)
        for triangle in indices:
            for vertex_id in triangle:
                glTexCoord2fv(texture_coords[vertex_id])
                glVertex3fv(vertices[vertex_id])
        glEnd()
        
        glPopMatrix()
        glDisable(GL_TEXTURE_2D)
    
    def setup_2d_mode(self):
        """Przełącza na tryb 2D dla interfejsu"""
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, self.display[0], self.display[1], 0, -1, 1)
        
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    def setup_3d_mode(self):
        """Przełącza z powrotem na tryb 3D"""
        glDisable(GL_BLEND)
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
    
    def create_menu_surface(self):
        """Tworzy powierzchnię menu"""
        self.menu_surface = pygame.Surface((self.menu_width, self.menu_height), 
                                          pygame.SRCALPHA)
        self.update_menu_surface()
    
    def update_menu_surface(self):
        """Aktualizuje powierzchnię menu"""
        # Tło menu
        self.menu_surface.fill(self.colors.MENU_BG)
        
        # Nagłówek menu
        header_rect = pygame.Rect(0, 0, self.menu_width, 60)
        pygame.draw.rect(self.menu_surface, self.colors.MENU_HEADER, header_rect)
        
        # Ramka
        pygame.draw.rect(self.menu_surface, self.colors.BUTTON_BORDER, 
                        (0, 0, self.menu_width, self.menu_height), 3)
        
        # Tytuł menu
        title_text = self.menu_font.render("📋 Menu Główne", True, self.colors.TEXT_ACCENT)
        title_rect = title_text.get_rect(center=(self.menu_width//2, 30))
        self.menu_surface.blit(title_text, title_rect)
        
        if self.current_section:
            # Przycisk powrotu
            back_btn = EnhancedButton(20, 80, 360, 50, "⬅️ Powrót")
            back_btn.draw(self.menu_surface, self.menu_font, self.colors)
            
            # Zawartość sekcji
            y = 150
            for line in self.menu_sections[self.current_section]:
                if line.strip():
                    text_surface = self.text_font.render(line, True, self.colors.TEXT_PRIMARY)
                    self.menu_surface.blit(text_surface, (20, y))
                y += 35
        else:
            # Przyciski głównego menu
            for button in self.buttons['main']:
                button.draw(self.menu_surface, self.menu_font, self.colors)
    
    def draw_menu_button(self):
        """Rysuje przyciski górne"""
        self.menu_btn.draw(self.screen, self.menu_font, self.colors)
        self.layer_btn.draw(self.screen, self.menu_font, self.colors)
    
    def draw_menu(self):
        """Rysuje menu"""
        if not self.show_menu:
            return
        
        # Animacja menu
        target = self.display[0] - self.menu_width if self.show_menu else self.display[0]
        self.menu_position += (target - self.menu_position) * 0.3
        
        if abs(self.menu_position - self.display[0]) > 1 or self.show_menu:
            # Konwertuj powierzchnię na dane OpenGL
            text_data = pygame.image.tostring(self.menu_surface, 'RGBA', True)
            glWindowPos2d(int(self.menu_position), self.display[1] - self.menu_height - self.menu_y)
            glDrawPixels(self.menu_width, self.menu_height, GL_RGBA, GL_UNSIGNED_BYTE, text_data)
    
    def handle_menu(self, event) -> bool:
        """Obsługuje zdarzenia menu"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            menu_x = int(self.menu_position)
            
            # Sprawdź przycisk warstwy
            if self.layer_btn.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                self.cycle_texture()
                return True
            
            # Sprawdź przycisk menu
            if self.menu_btn.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                self.show_menu = not self.show_menu
                self.current_section = None
                self.update_menu_surface()
                return True
            
            # Obsługa elementów menu
            if self.show_menu:
                if self.current_section:
                    # Przycisk powrotu
                    back_btn = EnhancedButton(20, 80, 360, 50, "⬅️ Powrót")
                    back_pos = (mouse_pos[0] - menu_x, mouse_pos[1] - self.menu_y)
                    if back_btn.rect.collidepoint(back_pos):
                        self.current_section = None
                        self.update_menu_surface()
                        return True
                else:
                    # Przyciski głównego menu
                    adjusted_pos = (mouse_pos[0] - menu_x, mouse_pos[1] - self.menu_y)
                    for i, button in enumerate(self.buttons['main']):
                        if button.rect.collidepoint(adjusted_pos):
                            self.handle_menu_action(i)
                            return True
        
        return False
    
    def handle_menu_action(self, button_index: int):
        """Obsługuje akcje menu"""
        actions = [
            self.show_about,
            self.show_instructions,
            self.show_settings,
            self.save_state,
            self.load_state,
            self.reset_view,
            self.quit_program
        ]
        
        if 0 <= button_index < len(actions):
            actions[button_index]()
    
    def cycle_texture(self):
        """Zmienia teksturę Ziemi"""
        textures = list(self.textures.keys())
        if textures:
            current_idx = textures.index(self.current_texture)
            next_idx = (current_idx + 1) % len(textures)
            self.current_texture = textures[next_idx]
            
            # Aktualizuj menu
            self.menu_sections['⚙️ Ustawienia'][2] = f"• Warstwa: {self.current_texture}"
            self.update_menu_surface()
            
            logger.info(f"Zmieniono teksturę na: {self.current_texture}")
    
    def show_about(self):
        """Pokazuje informacje o programie"""
        self.current_section = 'ℹ️ O Programie'
        self.update_menu_surface()
        self.show_message("ℹ️ O Programie", "Naciśnij dowolny klawisz, aby wrócić do menu")
    
    def show_instructions(self):
        """Pokazuje instrukcje"""
        self.current_section = '🎮 Instrukcje'
        self.update_menu_surface()
        self.show_message("🎮 Instrukcje", "Naciśnij dowolny klawisz, aby wrócić do menu")
    
    def show_settings(self):
        """Pokazuje ustawienia"""
        self.current_section = '⚙️ Ustawienia'
        self.update_menu_surface()
        self.show_message("⚙️ Ustawienia", "Naciśnij dowolny klawisz, aby wrócić do menu")
    
    def save_state(self):
        """Zapisuje obecny stan"""
        config = {
            "last_position": {
                "x": self.rotation_x,
                "y": self.rotation_y,
                "distance": self.distance
            },
            "texture": self.current_texture,
            "auto_rotate": self.auto_rotate,
            "mouse_sensitivity": self.mouse_sensitivity,
            "view_mode": self.view_mode.value,
            "animation_enabled": self.animation_enabled,
            "effects_enabled": self.effects_enabled,
            "sound_enabled": self.sound_enabled,
            "atmosphere_enabled": self.atmosphere_enabled
        }
        
        if self.data_manager.save_config(config):
            self.show_message("💾 Zapisano", "Stan został zapisany pomyślnie!")
        else:
            self.show_message("❌ Błąd", "Nie udało się zapisać stanu!")
    
    def load_state(self):
        """Wczytuje zapisany stan"""
        config = self.data_manager.load_config()
        
        if 'last_position' in config:
            pos = config['last_position']
            self.rotation_x = pos.get('x', 0)
            self.rotation_y = pos.get('y', 180)
            self.distance = pos.get('distance', -5)
            self.update_view_matrix()
            
            self.show_message("📂 Wczytano", "Stan został wczytany pomyślnie!")
        else:
            self.show_message("❌ Błąd", "Brak zapisanego stanu!")
    
    def reset_view(self):
        """Resetuje widok do pozycji domyślnej"""
        self.rotation_x = 0
        self.rotation_y = 180
        self.distance = -5
        self.auto_rotate = True
        self.update_view_matrix()
        
        self.show_message("🔄 Reset", "Widok został zresetowany!")
    
    def quit_program(self):
        """Zamyka program"""
        self.save_state()  # Zapisz stan przed wyjściem
        pygame.quit()
        sys.exit(0)
    
    def show_message(self, title: str, message: str):
        """Pokazuje komunikat użytkownikowi"""
        self.current_section = None
        self.update_menu_surface()
        
        # Czekaj na naciśnięcie klawisza
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False
                    break
            
            self.draw()
            pygame.time.wait(16)  # ~60 FPS
    
    def handle_top_menu_click(self, action: str):
        """Obsługuje kliknięcia w pasek menu u góry"""
        if action == "view_mode":
            self.toggle_view_mode()
        elif action == "animation":
            self.toggle_animation()
        elif action == "stats":
            self.toggle_stats()
        elif action == "effects":
            self.toggle_effects()
        elif action == "atmosphere":
            self.toggle_atmosphere()
        elif action == "screenshot":
            self.take_screenshot()
        elif action == "sound":
            self.toggle_sound()
        elif action == "settings":
            self.show_settings_menu()
        elif action == "help":
            self.show_help_menu()
        elif action == "exit":
            self.exit_program()
    
    # 1. Funkcja zmiany trybu widoku
    def toggle_view_mode(self):
        """Zmienia tryb widoku (Normal/Wireframe/Points/Night)"""
        modes = [ViewMode.NORMAL, ViewMode.WIREFRAME, ViewMode.POINTS, ViewMode.NIGHT]
        current_index = modes.index(self.view_mode)
        next_index = (current_index + 1) % len(modes)
        self.view_mode = modes[next_index]
        
        # Zastosuj tryb
        if self.view_mode == ViewMode.WIREFRAME:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        elif self.view_mode == ViewMode.POINTS:
            glPolygonMode(GL_FRONT_AND_BACK, GL_POINT)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        
        self.show_message("🌍 Tryb Widoku", f"Zmieniono na: {self.view_mode.value}")
        logger.info(f"Zmieniono tryb widoku na: {self.view_mode.value}")
    
    # 2. Funkcja animacji
    def toggle_animation(self):
        """Włącza/wyłącza animacje"""
        self.animation_enabled = not self.animation_enabled
        
        if self.animation_enabled:
            self.animation_time = 0
            self.show_message("🎬 Animacja", "Animacje włączone!")
        else:
            self.show_message("🎬 Animacja", "Animacje wyłączone!")
        
        logger.info(f"Animacje: {'włączone' if self.animation_enabled else 'wyłączone'}")
    
    # 3. Funkcja statystyk
    def toggle_stats(self):
        """Włącza/wyłącza wyświetlanie statystyk"""
        self.stats_enabled = not self.stats_enabled
        
        if self.stats_enabled:
            self.show_message("📊 Statystyki", "Statystyki włączone!")
        else:
            self.show_message("📊 Statystyki", "Statystyki wyłączone!")
        
        logger.info(f"Statystyki: {'włączone' if self.stats_enabled else 'wyłączone'}")
    
    # 4. Funkcja efektów
    def toggle_effects(self):
        """Włącza/wyłącza efekty wizualne"""
        self.effects_enabled = not self.effects_enabled
        
        if self.effects_enabled:
            glEnable(GL_BLEND)
            glEnable(GL_DEPTH_TEST)
            self.show_message("🎨 Efekty", "Efekty wizualne włączone!")
        else:
            glDisable(GL_BLEND)
            self.show_message("🎨 Efekty", "Efekty wizualne wyłączone!")
        
        logger.info(f"Efekty: {'włączone' if self.effects_enabled else 'wyłączone'}")
    
    # 5. Funkcja atmosfery
    def toggle_atmosphere(self):
        """Włącza/wyłącza symulację atmosfery"""
        self.atmosphere_enabled = not self.atmosphere_enabled
        
        if self.atmosphere_enabled:
            self.clouds_enabled = True
            self.show_message("🌙 Atmosfera", "Symulacja atmosfery włączona!")
        else:
            self.clouds_enabled = False
            self.show_message("🌙 Atmosfera", "Symulacja atmosfery wyłączona!")
        
        logger.info(f"Atmosfera: {'włączona' if self.atmosphere_enabled else 'wyłączona'}")
    
    # 6. Funkcja screenshot
    def take_screenshot(self):
        """Robi zrzut ekranu"""
        try:
            self.screenshot_counter += 1
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}_{self.screenshot_counter}.png"
            
            # Zrób screenshot
            pygame.image.save(self.screen, filename)
            
            self.show_message("📸 Screenshot", f"Zapisano jako: {filename}")
            logger.info(f"Zrobiono screenshot: {filename}")
            
        except Exception as e:
            self.show_message("❌ Błąd", f"Nie udało się zrobić screenshot: {e}")
            logger.error(f"Błąd screenshot: {e}")
    
    # 7. Funkcja dźwięku
    def toggle_sound(self):
        """Włącza/wyłącza dźwięk"""
        self.sound_enabled = not self.sound_enabled
        
        if self.sound_enabled:
            pygame.mixer.unpause()
            self.show_message("🎵 Dźwięk", "Dźwięk włączony!")
        else:
            pygame.mixer.pause()
            self.show_message("🎵 Dźwięk", "Dźwięk wyłączony!")
        
        logger.info(f"Dźwięk: {'włączony' if self.sound_enabled else 'wyłączony'}")
    
    # 8. Funkcja ustawień
    def show_settings_menu(self):
        """Pokazuje ustawienia"""
        self.current_section = '⚙️ Ustawienia'
        self.update_menu_surface()
        self.show_message("⚙️ Ustawienia", "Naciśnij dowolny klawisz, aby wrócić do menu")
    
    # 9. Funkcja pomocy
    def show_help_menu(self):
        """Pokazuje pomoc"""
        help_text = [
            "❓ Pomoc - Earth Simulator Enhanced",
            "",
            "🎮 Sterowanie:",
            "• Mysz - obracanie i zoom",
            "• Klawiatura - skróty",
            "• Pasek menu - nowe funkcje",
            "",
            "🌍 Funkcje:",
            "• Widok - różne tryby wyświetlania",
            "• Animacja - efekty animacji",
            "• Statystyki - informacje o programie",
            "• Efekty - efekty wizualne",
            "• Atmosfera - symulacja atmosfery",
            "• Screenshot - zrzut ekranu",
            "• Dźwięk - włącz/wyłącz dźwięk",
            "• Ustawienia - konfiguracja",
            "• Pomoc - ta instrukcja",
            "",
            "👨‍💻 Autor: Adrian Lesniak"
        ]
        
        self.show_message("❓ Pomoc", "Naciśnij dowolny klawisz, aby wrócić do menu")
    
    # 10. Funkcja wyjścia
    def exit_program(self):
        """Zamyka program"""
        self.save_state()  # Zapisz stan przed wyjściem
        pygame.quit()
        sys.exit(0)
    
    def update_animation(self):
        """Aktualizuje animacje"""
        if self.animation_enabled:
            self.animation_time += 0.016  # ~60 FPS
            
            if self.animation_type == AnimationType.ROTATION:
                self.rotation_y += self.animation_speed * 0.5
            elif self.animation_type == AnimationType.ORBIT:
                orbit_radius = 3.0
                self.rotation_x = math.sin(self.animation_time) * 30
                self.rotation_y += self.animation_speed * 0.3
            elif self.animation_type == AnimationType.ZOOM:
                zoom_factor = math.sin(self.animation_time * 0.5) * 2
                self.distance = -5 + zoom_factor
            elif self.animation_type == AnimationType.FLYBY:
                self.rotation_x = math.sin(self.animation_time * 0.3) * 45
                self.rotation_y += self.animation_speed * 0.4
                zoom_factor = math.sin(self.animation_time * 0.2) * 3
                self.distance = -5 + zoom_factor
            
            self.update_view_matrix()
    
    def draw_stats(self):
        """Rysuje statystyki"""
        if not self.stats_enabled:
            return
        
        # Oblicz FPS
        self.frame_count += 1
        current_time = time.time()
        if current_time - self.start_time >= 1.0:
            self.fps_counter = self.frame_count
            self.frame_count = 0
            self.start_time = current_time
        
        # Przygotuj tekst statystyk
        stats_text = [
            f"FPS: {self.fps_counter}",
            f"Tryb: {self.view_mode.value}",
            f"Animacja: {'ON' if self.animation_enabled else 'OFF'}",
            f"Efekty: {'ON' if self.effects_enabled else 'OFF'}",
            f"Atmosfera: {'ON' if self.atmosphere_enabled else 'OFF'}",
            f"Pozycja: X={self.rotation_x:.1f}° Y={self.rotation_y:.1f}°",
            f"Zoom: {abs(self.distance):.1f}"
        ]
        
        # Rysuj statystyki w prawym górnym rogu
        y_offset = 50
        for i, text in enumerate(stats_text):
            text_surface = self.small_font.render(text, True, self.colors.TEXT_ACCENT)
            text_rect = text_surface.get_rect()
            text_rect.topright = (self.display[0] - 10, y_offset + i * 20)
            
            # Tło dla tekstu
            bg_rect = text_rect.inflate(10, 5)
            pygame.draw.rect(self.screen, (0, 0, 0, 150), bg_rect)
            self.screen.blit(text_surface, text_rect)
    
    def draw_atmosphere(self):
        """Rysuje efekty atmosfery"""
        if not self.atmosphere_enabled:
            return
        
        # Symulacja chmur (proste kółka)
        if self.clouds_enabled:
            for i in range(5):
                cloud_x = (math.sin(time.time() * 0.1 + i) * 100) + self.display[0] // 2
                cloud_y = 50 + i * 30
                cloud_size = 20 + i * 5
                
                pygame.draw.circle(self.screen, (255, 255, 255, 100), 
                                 (int(cloud_x), cloud_y), cloud_size)
    
    def handle_mouse(self, event):
        """Obsługuje zdarzenia myszy"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            current_time = pygame.time.get_ticks()
            
            # Sprawdź kliknięcie w pasek menu
            if event.pos[1] < 40:  # Pasek menu
                action = self.top_menu.handle_click(event.pos)
                if action:
                    self.handle_top_menu_click(action)
                    return
            
            if event.button == 1:  # Lewy przycisk myszy
                if current_time - self.last_click_time < self.double_click_delay:
                    self.reset_view()
                    self.auto_rotate = True
                self.last_click_time = current_time
                self.last_pos = pygame.mouse.get_pos()
                self.rotation_velocity = [0.0, 0.0]
            
            elif event.button in (4, 5):  # Kółko myszy
                try:
                    zoom_factor = 1 if event.button == 4 else -1
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    self.zoom_at_cursor(mouse_x, mouse_y, zoom_factor)
                except Exception as e:
                    logger.error(f"Błąd obsługi zoom: {e}")
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.last_pos is not None:
                    current_pos = pygame.mouse.get_pos()
                    dx = (current_pos[0] - self.last_pos[0]) * self.mouse_sensitivity
                    dy = (current_pos[1] - self.last_pos[1]) * self.mouse_sensitivity
                    self.rotation_velocity = [float(dy * 0.1), float(dx * 0.1)]
                self.last_pos = None
        
        elif event.type == pygame.MOUSEMOTION and self.last_pos is not None:
            x, y = pygame.mouse.get_pos()
            
            rotation_speed = self.get_zoom_factor()
            dx = (x - self.last_pos[0]) * self.mouse_sensitivity * rotation_speed
            dy = (y - self.last_pos[1]) * self.mouse_sensitivity * rotation_speed
            
            self.rotation_y += dx
            self.rotation_x = max(-85, min(85, self.rotation_x + dy))
            
            self.update_view_matrix()
            self.last_pos = (x, y)
    
    def zoom_at_cursor(self, x: int, y: int, zoom_factor: int):
        """Przybliża/oddala widok w punkcie kursora"""
        try:
            zoom_amount = zoom_factor * self.zoom_sensitivity
            new_distance = self.distance + zoom_amount
            
            if self.min_zoom <= new_distance <= self.max_zoom:
                self.distance = new_distance
                self.update_view_matrix()
                
        except Exception as e:
            logger.error(f"Błąd zoom: {e}")
    
    def update_rotation(self):
        """Aktualizuje rotację"""
        if self.last_pos is not None:
            self.auto_rotate = False
        elif self.auto_rotate:
            self.rotation_y += self.auto_rotate_speed
        
        # Zastosuj pęd
        self.rotation_x += float(self.rotation_velocity[0])
        self.rotation_y += float(self.rotation_velocity[1])
        
        # Tłumienie pędu
        self.rotation_velocity[0] *= self.rotation_momentum
        self.rotation_velocity[1] *= self.rotation_momentum
        
        # Ograniczenie rotacji pionowej
        self.rotation_x = max(-85, min(85, self.rotation_x))
        
        self.update_view_matrix()
    
    def get_zoom_factor(self) -> float:
        """Oblicza współczynnik prędkości rotacji na podstawie zoom"""
        zoom_range = self.max_zoom - self.min_zoom
        current_zoom = self.distance - self.min_zoom
        zoom_factor = current_zoom / zoom_range
        return max(0.05, 0.2 * zoom_factor)
    
    def run(self):
        """Główna pętla programu"""
        try:
            clock = pygame.time.Clock()
            logger.info("Rozpoczęto symulację")
            
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.quit_program()
                    
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.quit_program()
                        elif event.key == pygame.K_m:
                            self.show_menu = not self.show_menu
                            self.current_section = None
                            self.update_menu_surface()
                        elif event.key == pygame.K_l:
                            self.cycle_texture()
                        elif event.key == pygame.K_r:
                            self.reset_view()
                        elif event.key == pygame.K_v:
                            self.toggle_view_mode()
                        elif event.key == pygame.K_a:
                            self.toggle_animation()
                        elif event.key == pygame.K_s:
                            self.toggle_stats()
                        elif event.key == pygame.K_e:
                            self.toggle_effects()
                        elif event.key == pygame.K_t:
                            self.take_screenshot()
                    
                    if self.handle_menu(event):
                        continue
                    
                    self.handle_mouse(event)
                
                self.update_rotation()
                self.update_animation()
                self.draw()
                self.draw_stats()
                self.draw_atmosphere()
                clock.tick(60)
                
        except Exception as e:
            logger.error(f"Błąd krytyczny: {e}")
            pygame.quit()
            sys.exit(1)

def check_dependencies():
    """Sprawdza wymagane zależności"""
    required_modules = ['pygame', 'OpenGL', 'numpy', 'PIL']
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError as e:
            print(f"❌ Błąd: Brak modułu {module}")
            print(f"Szczegóły: {e}")
            print("🔧 Zainstaluj zależności: pip install pygame PyOpenGL numpy Pillow")
            return False
    
    print("✅ Wszystkie zależności są dostępne")
    return True

def check_texture_files():
    """Sprawdza pliki tekstur"""
    required_files = ['earth_texture.jpg', 'earth_political.jpg', 'earth_detailed.jpg']
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    missing_files = []
    for file in required_files:
        file_path = os.path.join(script_dir, file)
        if not os.path.exists(file_path):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Brakujące pliki tekstur: {', '.join(missing_files)}")
        print("📁 Upewnij się, że pliki tekstur są w katalogu programu")
        return False
    
    print("✅ Wszystkie pliki tekstur są dostępne")
    return True

def main():
    """Główna funkcja programu"""
    print("🌟 Earth Simulator Enhanced v2.0")
    print("👨‍💻 Autor: Adrian Lesniak")
    print("=" * 50)
    
    # Sprawdź zależności
    if not check_dependencies():
        sys.exit(1)
    
    # Sprawdź pliki tekstur
    if not check_texture_files():
        sys.exit(1)
    
    try:
        # Uruchom symulator
        simulator = EnhancedEarthSimulator()
        simulator.run()
        
    except Exception as e:
        logger.error(f"Błąd fatalny: {e}")
        print(f"❌ Błąd: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 