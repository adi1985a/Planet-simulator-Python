import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

def test_opengl():
    pygame.init()
    display = (400, 300)
    try:
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
        print("OpenGL initialization successful!")
        print(f"OpenGL version: {glGetString(GL_VERSION).decode()}")
        pygame.quit()
        return True
    except Exception as e:
        print(f"OpenGL initialization failed: {e}")
        pygame.quit()
        return False

if __name__ == "__main__":
    test_opengl()
