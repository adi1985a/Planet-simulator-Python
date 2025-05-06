import sys
import os

def check_dependencies():
    try:
        import pygame
        import OpenGL
        import numpy
        from PIL import Image
        return True
    except ImportError as e:
        print(f"Error: Missing dependency - {str(e)}")
        print("Please run: pip install pygame PyOpenGL numpy Pillow")
        return False

def check_texture_file():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    texture_path = os.path.join(script_dir, 'earth_texture.jpg')
    if not os.path.exists(texture_path):
        print(f"Error: Texture file not found at {texture_path}")
        print("Please add 'earth_texture.jpg' to the script directory")
        return False
    return True

if __name__ == "__main__":
    if not check_dependencies():
        sys.exit(1)
    if not check_texture_file():
        sys.exit(1)
        
    # Now import all required modules
    import pygame
    from pygame.locals import *
    from OpenGL.GL import *
    from OpenGL.GLU import *
    import numpy as np
    from PIL import Image

    class Button:
        def __init__(self, x, y, width, height, text):
            self.rect = pygame.Rect(x, y, width, height)
            self.text = text
            self.hovered = False
            
        def draw(self, surface, font):
            # Much brighter button colors
            color = (180, 180, 180) if self.hovered else (140, 140, 140)
            border_color = (255, 255, 255) if self.hovered else (220, 220, 220)
            
            pygame.draw.rect(surface, color, self.rect)
            pygame.draw.rect(surface, border_color, self.rect, 2)
            
            # Bright white text with shadow for better readability
            shadow = font.render(self.text, True, (80, 80, 80))
            text = font.render(self.text, True, (255, 255, 255))
            text_rect = text.get_rect(center=self.rect.center)
            surface.blit(shadow, (text_rect.x + 1, text_rect.y + 1))
            surface.blit(text, text_rect)

        def handle_event(self, event, menu_pos):
            if event.type == pygame.MOUSEMOTION:
                self.hovered = self.rect.collidepoint(event.pos[0] - menu_pos, event.pos[1])
            return self.hovered and event.type == pygame.MOUSEBUTTONDOWN

    class EarthSimulator:
        def __init__(self):
            pygame.init()
            self.display = (1280, 720)  # Increased window size
            pygame.display.set_caption('Earth Simulator by Adrian Lesniak')
            try:
                self.screen = pygame.display.set_mode(self.display, DOUBLEBUF | OPENGL)
            except pygame.error as e:
                print(f"Error initializing display: {e}")
                sys.exit(1)
            
            glEnable(GL_DEPTH_TEST)
            # Remove lighting effects
            # glEnable(GL_LIGHTING)
            # glEnable(GL_LIGHT0)
            # glEnable(GL_COLOR_MATERIAL)
            # glLight(GL_LIGHT0, GL_POSITION, (5, 5, 5, 1))
            
            self.fov = 45
            self.aspect = self.display[0]/self.display[1]
            self.near = 0.1
            self.far = 50.0
            self.distance = -5
            
            self.update_perspective()
            glTranslatef(0.0, 0.0, self.distance)
            
            self.rotation_x = 0
            self.rotation_y = 180  # Flip the initial orientation
            self.last_pos = None
            self.menu_opacity = 240  # Move this line up
            self.show_menu = False
            self.menu_width = 350
            self.menu_height = 500
            self.menu_position = self.display[0]  # Start hidden
            self.menu_y = 50  # Position below menu button
            self.current_section = None
            self.menu_font = pygame.font.Font(None, 32)
            self.text_font = pygame.font.Font(None, 24)
            
            # Create buttons
            self.buttons = {
                'main': [
                    Button(10, 50, 280, 40, "About"),
                    Button(10, 100, 280, 40, "Instructions"),
                    Button(10, 150, 280, 40, "Settings")
                ]
            }
            
            # Create menu content
            self.menu_sections = {
                'About': [
                    "Earth Simulator v1.0",
                    "by Adrian Lesniak",
                    "Created with PyOpenGL"
                ],
                'Instructions': [
                    "Mouse drag - Rotate globe",
                    "Mouse wheel - Zoom in/out",
                    "M - Toggle menu",
                    "ESC - Exit program"
                ],
                'Settings': [
                    "Resolution: 800x600",
                    "Quality: High",
                    "Rotation Speed: Normal"
                ]
            }
            
            # Menu button properties
            self.menu_btn = Button(self.display[0] - 100, 10, 90, 30, "Menu")
            
            self.create_menu_surface()
            
            # Add mouse control properties
            self.mouse_sensitivity = 0.2  # Adjusted for better feel
            self.zoom_sensitivity = 0.1   # Zoom speed multiplier
            self.min_zoom = -15
            self.max_zoom = -2
            self.rotation_momentum = 0.92  # For smooth deceleration
            self.rotation_velocity = [0, 0]  # [x, y] rotation velocity
            self.auto_rotate = True  # Gentle auto-rotation when not interacting
            self.auto_rotate_speed = 0.1
            
            # Save view matrix state
            self.modelview_matrix = glGetFloatv(GL_MODELVIEW_MATRIX)

            self.initial_rotation_x = 0
            self.initial_rotation_y = 180
            self.initial_distance = -5
            self.last_click_time = 0
            self.double_click_delay = 300  # milliseconds

            # Add texture handling
            self.texture_files = {
                'Default': 'earth_texture.jpg',
                'Political': 'earth_political.jpg',
                'Detailed': 'earth_detailed.jpg'
            }
            self.current_texture = 'Default'
            self.textures = {}
            
            # Add layer button
            self.layer_btn = Button(self.display[0] - 200, 10, 90, 30, "Layer")
            
            # Load all textures
            self.load_all_textures()
            
            # Update menu sections
            self.menu_sections['Settings'] = [
                "Resolution: 1280x720",
                "Quality: High",
                "Current Layer: " + self.current_texture,
                "",
                "Available Layers:",
                "- Default (Terrain)",
                "- Political (Countries)",
                "- Detailed (Terrain HD)"
            ]

            self.mouse_sensitivity = 0.2
            
            # Add zoom-dependent rotation
            self.base_rotation_speed = 0.2  # Base rotation speed
            self.min_rotation_speed = 0.05  # Minimum rotation speed when zoomed in

        def update_perspective(self):
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            gluPerspective(self.fov, self.aspect, self.near, self.far)
            glMatrixMode(GL_MODELVIEW)

        def load_all_textures(self):
            for name, file in self.texture_files.items():
                try:
                    self.textures[name] = self.load_texture(file)
                except Exception as e:
                    print(f"Error loading texture {file}: {e}")

        def load_texture(self, filename):
            try:
                script_dir = os.path.dirname(os.path.abspath(__file__))
                image_path = os.path.join(script_dir, filename)
                
                if not os.path.exists(image_path):
                    print(f"Error: Texture file not found at {image_path}")
                    return None
                    
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
                print(f"Error loading texture: {e}")
                return None

        def create_sphere(self, radius, segments):
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
        
        def draw(self):
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            
            # Restore saved modelview matrix
            glLoadMatrixf(self.modelview_matrix)
            
            # Draw the earth
            vertices, texture_coords, indices = self.create_sphere(2, 32)
            glEnable(GL_TEXTURE_2D)
            
            # Use the current texture from textures dictionary
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
            
            # Draw menu button always
            self.draw_menu_button()
            
            # Draw menu if shown
            if self.show_menu:
                self.draw_menu()
            
            # Single buffer swap
            pygame.display.flip()
        
        def create_menu_surface(self):
            self.menu_surface = pygame.Surface((self.menu_width, self.menu_height), pygame.SRCALPHA)
            self.update_menu_surface()

        def update_menu_surface(self):
            # Much brighter menu with higher contrast and fully opaque
            background = (120, 120, 120)  # Much lighter background, fully opaque
            header = (140, 140, 140)      # Lighter header, fully opaque
            
            self.menu_surface.fill(background)
            pygame.draw.rect(self.menu_surface, header, (0, 0, self.menu_width, 40))
            pygame.draw.rect(self.menu_surface, (0, 0, 0), (0, 0, self.menu_width, self.menu_height), 2)  # Thicker border
            pygame.draw.line(self.menu_surface, (0, 0, 0), (0, 40), (self.menu_width, 40), 3)  # Thicker line
            
            # Title with stronger shadow
            shadow_title = self.menu_font.render("Menu", True, (80, 80, 80))
            title = self.menu_font.render("Menu", True, (255, 255, 255))
            title_rect = title.get_rect(centerx=self.menu_width//2, centery=20)
            self.menu_surface.blit(shadow_title, (title_rect.x + 2, title_rect.y + 2))
            self.menu_surface.blit(title, title_rect)
            
            if self.current_section:
                # Draw back button
                back_btn = Button(10, 50, 280, 40, "Back")
                back_btn.draw(self.menu_surface, self.menu_font)
                
                # Draw section content with shadows for better contrast
                y = 100
                for line in self.menu_sections[self.current_section]:
                    shadow = self.text_font.render(line, True, (80, 80, 80))
                    text = self.text_font.render(line, True, (255, 255, 255))
                    self.menu_surface.blit(shadow, (21, y + 1))
                    self.menu_surface.blit(text, (20, y))
                    y += 30
            else:
                # Draw main menu buttons
                for button in self.buttons['main']:
                    button.draw(self.menu_surface, self.menu_font)

        def handle_menu(self, event):
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                menu_x = int(self.menu_position)
                
                # Check layer button click
                if self.layer_btn.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                    textures = list(self.textures.keys())
                    current_idx = textures.index(self.current_texture)
                    next_idx = (current_idx + 1) % len(textures)
                    self.current_texture = textures[next_idx]
                    
                    # Update settings menu
                    self.menu_sections['Settings'][2] = f"Current Layer: {self.current_texture}"
                    self.update_menu_surface()
                    return True
                    
                # Check menu button click
                if self.menu_btn.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                    self.show_menu = not self.show_menu
                    self.current_section = None
                    self.update_menu_surface()
                    return True
                
                # Handle menu items only if menu is shown
                if self.show_menu:
                    if self.current_section:
                        # Fix back button click detection
                        back_btn = Button(10, 50, 280, 40, "Back")
                        back_pos = (mouse_pos[0] - menu_x, mouse_pos[1] - self.menu_y)
                        if back_btn.rect.collidepoint(back_pos):
                            self.current_section = None
                            self.update_menu_surface()
                            return True
                    else:
                        # Fix main menu buttons click detection
                        adjusted_pos = (mouse_pos[0] - menu_x, mouse_pos[1] - self.menu_y)
                        for button in self.buttons['main']:
                            if button.rect.collidepoint(adjusted_pos):
                                self.current_section = button.text
                                self.update_menu_surface()
                                return True
            
            return False

        def draw_menu(self):
            if not self.show_menu:
                return
                
            # Make menu animation smoother and faster
            target = self.display[0] - self.menu_width if self.show_menu else self.display[0]
            self.menu_position += (target - self.menu_position) * 0.4
            
            if abs(self.menu_position - self.display[0]) > 1 or self.show_menu:
                glEnable(GL_BLEND)
                glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
                
                text_data = pygame.image.tostring(self.menu_surface, 'RGBA', True)
                glWindowPos2d(int(self.menu_position), self.display[1] - self.menu_height - self.menu_y)
                glDrawPixels(self.menu_width, self.menu_height, GL_RGBA, GL_UNSIGNED_BYTE, text_data)
                
                glDisable(GL_BLEND)

        def draw_menu_button(self):
            # Save current matrices and attributes
            glPushMatrix()
            glLoadIdentity()
            
            glMatrixMode(GL_PROJECTION)
            glPushMatrix()
            glLoadIdentity()
            glOrtho(0, self.display[0], self.display[1], 0, -1, 1)
            
            # Enable blending for transparency
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            
            # Draw menu button
            btn_surface = pygame.Surface((90, 30), pygame.SRCALPHA)
            self.menu_btn.draw(btn_surface, self.menu_font)
            # Add white glow/outline
            pygame.draw.rect(btn_surface, (255, 255, 255, 100), (0, 0, 90, 30), 1)
            btn_data = pygame.image.tostring(btn_surface, 'RGBA', True)
            glWindowPos2d(self.display[0] - 100, 10)
            glDrawPixels(90, 30, GL_RGBA, GL_UNSIGNED_BYTE, btn_data)
            
            # Draw layer button with same style
            btn_surface = pygame.Surface((90, 30), pygame.SRCALPHA)
            self.layer_btn.draw(btn_surface, self.menu_font)
            pygame.draw.rect(btn_surface, (255, 255, 255, 100), (0, 0, 90, 30), 1)
            btn_data = pygame.image.tostring(btn_surface, 'RGBA', True)
            glWindowPos2d(self.display[0] - 200, 10)
            glDrawPixels(90, 30, GL_RGBA, GL_UNSIGNED_BYTE, btn_data)
            
            # Restore OpenGL state
            glDisable(GL_BLEND)
            glPopMatrix()
            glMatrixMode(GL_MODELVIEW)
            glPopMatrix()

        def reset_view(self):
            """Reset view to initial position"""
            self.rotation_x = self.initial_rotation_x
            self.rotation_y = self.initial_rotation_y
            self.distance = self.initial_distance
            
            glLoadIdentity()
            glTranslatef(0.0, 0.0, self.distance)
            glRotatef(self.rotation_x, 1, 0, 0)
            glRotatef(self.rotation_y, 0, 1, 0)
            self.modelview_matrix = glGetFloatv(GL_MODELVIEW_MATRIX)

        def zoom_at_cursor(self, x, y, zoom_factor):
            try:
                viewport = glGetIntegerv(GL_VIEWPORT)
                
                # Ensure coordinates are within viewport
                x = max(0, min(x, viewport[2]))
                y = max(0, min(y, viewport[3]))
                window_y = viewport[3] - y
                
                # Normalize coordinates
                norm_x = (2.0 * x) / viewport[2] - 1.0
                norm_y = (2.0 * y) / viewport[3] - 1.0
                
                # Safer depth reading
                try:
                    z = glReadPixels(x, window_y, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT)
                    if z is None or len(z) == 0:
                        z = 0.5  # Use middle depth if reading fails
                    else:
                        z = z[0][0]
                except:
                    z = 0.5  # Fallback depth value
                
                # Calculate new distance with bounds checking
                zoom_amount = zoom_factor * self.zoom_sensitivity
                new_distance = self.distance + zoom_amount
                
                if self.min_zoom <= new_distance <= self.max_zoom:
                    self.distance = new_distance
                    
                    # Update view matrix
                    glLoadIdentity()
                    glTranslatef(0.0, 0.0, self.distance)
                    glRotatef(self.rotation_x, 1, 0, 0)
                    glRotatef(self.rotation_y, 0, 1, 0)
                    self.modelview_matrix = glGetFloatv(GL_MODELVIEW_MATRIX)
                    
            except Exception as e:
                print(f"Zoom error (non-fatal): {e}")
                # Continue without zooming if there's an error

        def update_rotation(self):
            if self.last_pos is not None:
                # When dragging, stop auto-rotation
                self.auto_rotate = False
            elif self.auto_rotate:
                # Apply gentle auto-rotation when not interacting
                self.rotation_y += self.auto_rotate_speed
            
            # Apply rotation with momentum
            self.rotation_x += self.rotation_velocity[0]
            self.rotation_y += self.rotation_velocity[1]
            
            # Apply momentum decay
            self.rotation_velocity[0] *= self.rotation_momentum
            self.rotation_velocity[1] *= self.rotation_momentum
            
            # Limit vertical rotation
            self.rotation_x = max(-85, min(85, self.rotation_x))
            
            # Update view matrix
            glLoadIdentity()
            glTranslatef(0.0, 0.0, self.distance)
            glRotatef(self.rotation_x, 1, 0, 0)
            glRotatef(self.rotation_y, 0, 1, 0)
            self.modelview_matrix = glGetFloatv(GL_MODELVIEW_MATRIX)

        def get_zoom_factor(self):
            """Calculate rotation speed modifier based on zoom level"""
            zoom_range = self.max_zoom - self.min_zoom
            current_zoom = self.distance - self.min_zoom
            zoom_factor = current_zoom / zoom_range
            return max(self.min_rotation_speed, self.base_rotation_speed * zoom_factor)

        def handle_mouse(self, event):
            if event.type == pygame.MOUSEBUTTONDOWN:
                current_time = pygame.time.get_ticks()
                
                if event.button == 1:  # Left mouse button
                    if current_time - self.last_click_time < self.double_click_delay:
                        self.reset_view()
                        self.auto_rotate = True
                    self.last_click_time = current_time
                    self.last_pos = pygame.mouse.get_pos()
                    # Reset velocity when starting drag
                    self.rotation_velocity = [0, 0]
                
                elif event.button in (4, 5):  # Mouse wheel
                    try:
                        zoom_factor = 1 if event.button == 4 else -1
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        self.zoom_at_cursor(mouse_x, mouse_y, zoom_factor)
                    except Exception as e:
                        print(f"Zoom handling error (non-fatal): {e}")
                
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    if self.last_pos is not None:
                        # Calculate final velocity for momentum
                        current_pos = pygame.mouse.get_pos()
                        dx = (current_pos[0] - self.last_pos[0]) * self.mouse_sensitivity
                        dy = (current_pos[1] - self.last_pos[1]) * self.mouse_sensitivity
                        self.rotation_velocity = [dy * 0.1, dx * 0.1]  # Scale down for smoother momentum
                    self.last_pos = None
                    
            elif event.type == pygame.MOUSEMOTION and self.last_pos is not None:
                x, y = pygame.mouse.get_pos()
                
                # Apply zoom-dependent rotation speed
                rotation_speed = self.get_zoom_factor()
                dx = (x - self.last_pos[0]) * self.mouse_sensitivity * rotation_speed
                dy = (y - self.last_pos[1]) * self.mouse_sensitivity * rotation_speed
                
                # Update rotation directly during drag
                self.rotation_y += dx
                self.rotation_x = max(-85, min(85, self.rotation_x + dy))
                
                # Update view matrix
                glLoadIdentity()
                glTranslatef(0.0, 0.0, self.distance)
                glRotatef(self.rotation_x, 1, 0, 0)
                glRotatef(self.rotation_y, 0, 1, 0)
                self.modelview_matrix = glGetFloatv(GL_MODELVIEW_MATRIX)
                
                self.last_pos = (x, y)
        
        def run(self):
            try:
                clock = pygame.time.Clock()
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            return
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            return
                        
                        if self.handle_menu(event):
                            continue
                            
                        self.handle_mouse(event)
                    
                    self.update_rotation()  # Add rotation update to main loop
                    self.draw()
                    clock.tick(60)
                    
            except Exception as e:
                print(f"Error during execution: {e}")
                pygame.quit()
                sys.exit(1)

    if __name__ == "__main__":
        try:
            simulator = EarthSimulator()
            simulator.run()
        except Exception as e:
            print(f"Fatal error: {e}")
            sys.exit(1)
