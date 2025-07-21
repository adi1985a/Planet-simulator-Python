# 🌍✨ PyGlobe 3D: Interactive Earth Simulator 🛰️
_A 3D Earth visualization tool built with Python, PyOpenGL, and Pygame, featuring multiple texture layers, interactive mouse controls, and a menu system._

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.6%2B-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-Graphics%20%26%20Events-6495ED.svg?logo=pygame)](https://www.pygame.org/)
[![PyOpenGL](https://img.shields.io/badge/PyOpenGL-3D%20Rendering-5586A4.svg)]() <!-- No official PyOpenGL logo for shields.io -->
[![NumPy](https://img.shields.io/badge/NumPy-Array%20Manipulation-4D77CF.svg?logo=numpy)](https://numpy.org/)
[![Pillow](https://img.shields.io/badge/Pillow-Image%20Processing-9B59B6.svg)]() <!-- No official Pillow logo for shields.io -->

## 📋 Table of Contents
1.  [Overview](#-overview)
2.  [Key Features](#-key-features)
3.  [Screenshots (Conceptual)](#-screenshots-conceptual)
4.  [System Requirements & Dependencies](#-system-requirements--dependencies)
5.  [Texture File Requirements](#-texture-file-requirements)
6.  [Installation and Setup](#️-installation-and-setup)
7.  [Usage Guide & Controls](#️-usage-guide--controls)
8.  [File Structure (Expected)](#-file-structure-expected)
9.  [Technical Notes](#-technical-notes)
10. [Contributing](#-contributing)
11. [License](#-license)
12. [Contact](#-contact)

## 📄 Overview

**PyGlobe 3D: Interactive Earth Simulator**, developed by Adrian Lesniak, is a Python application that renders an interactive 3D model of the Earth. Built using **PyOpenGL** for 3D graphics rendering and **Pygame** for windowing, event handling, and texture loading (via **Pillow** and **NumPy** for processing), it allows users to explore our planet with multiple texture layers (terrain, political map, detailed terrain). Users can rotate and zoom the globe using mouse controls, switch between textures, and access an in-application menu for information and settings. The simulation aims for a smooth and natural feel with features like auto-rotation and momentum-based rotation.

<br> 
<p align="center">
  <img src="screenshots/1.gif" width="90%">
</p>
<br>


## ✨ Key Features

*   🌍 **3D Globe Rendering**:
    *   Displays a textured sphere representing the Earth using OpenGL primitives and texturing.
*   텍스처 **Multiple Texture Layers**:
    *   Allows users to switch between different visual representations of the Earth:
        *   **Default**: Standard terrain texture (`earth_texture.jpg`).
        *   **Political**: A map showing country borders (`earth_political.jpg`, optional).
        *   **Detailed**: A high-definition terrain texture (`earth_detailed.jpg`, optional).
*   🖱️ **Interactive Controls**:
    *   **Mouse Drag**: Click and drag the mouse to rotate the globe freely in any direction.
    *   **Mouse Scroll Wheel**: Zoom in and out for closer or wider views of the Earth.
    *   **Double-Click**: Resets the globe's orientation and zoom level to the initial default view.
*   ⚙️ **In-Application Menu System**:
    *   Toggled by a "Menu" button or the `M` key.
    *   Provides access to sections like "About," "Instructions," and "Settings."
*   🔄 **Smooth Animation & Rotation**:
    *   Supports optional auto-rotation of the globe.
    *   Implements momentum-based rotation, allowing the globe to continue spinning realistically after a mouse drag is released.
*   🖼️ **Texture Loading**: Uses Pillow (PIL Fork) to load image files for textures and NumPy to prepare them for OpenGL.

## 🖼️ Screenshots (Conceptual)

_Screenshots of the PyGlobe 3D application: the main view of the rotating Earth with the default texture, examples of the political and detailed textures applied, the menu interface, and demonstrations of zoom and rotation._

<p align="center">
  <img src="screenshots\1.jpg" width="300"/>
</p>


## ⚙️ System Requirements & Dependencies

### Software:
*   **Python**: Version 3.6 or higher.
*   **Libraries**:
    *   `pygame`: For window creation, event loop, and user input.
    *   `PyOpenGL`: The core OpenGL wrapper for Python, used for 3D rendering.
    *   `numpy`: For numerical operations, particularly array manipulation for textures.
    *   `Pillow` (PIL Fork): For loading and processing image files for textures.

### Installation of Dependencies:
*   All required libraries can be installed using `pip`.

## 🖼️ Texture File Requirements

*   **`earth_texture.jpg` (Required)**: The default terrain texture for the globe. The application will check for this file at startup and exit if it's missing.
*   **`earth_political.jpg` (Optional)**: A texture file for the political map layer. If present, it enables this view.
*   **`earth_detailed.jpg` (Optional)**: A texture file for a high-definition or alternative detailed terrain layer. If present, it enables this view.

*All texture files should be placed in the same directory as the main Python script (`main.py`).*

## 🛠️ Installation and Setup

1.  **Clone the Repository**:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```
    *(Replace `<repository-url>` and `<repository-directory>` with your specific details).*

2.  **Set Up a Virtual Environment (Recommended)**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Required Libraries**:
    ```bash
    pip install pygame PyOpenGL numpy Pillow
    # If a requirements.txt file is provided in the future:
    # pip install -r requirements.txt
    ```

4.  **Prepare Texture Files**:
    *   Ensure `earth_texture.jpg` is present in the root project directory (alongside `main.py`).
    *   Optionally, add `earth_political.jpg` and `earth_detailed.jpg` to the same directory if you want to use these texture layers.

5.  **Run the Application**:
    Open a terminal or command prompt in the project's root directory and execute:
    ```bash
    python main.py
    ```

## 💡 Usage Guide & Controls

1.  Launch the application by running `python main.py` after completing the setup.
2.  The main window will appear, displaying the 3D Earth globe, likely with auto-rotation active.
3.  **Controls**:
    *   **Rotate Globe**: Click and drag the **left mouse button** on the globe to manually rotate it.
    *   **Zoom In/Out**: Use the **mouse scroll wheel**.
    *   **Reset View**: **Double-click** the left mouse button anywhere on the globe to reset its orientation and zoom to the default initial state.
    *   **Toggle Menu**: Press the `M` key on your keyboard, or click a designated "Menu" button in the UI (if present).
    *   **Cycle Textures**: Click a designated "Layer" button in the UI (if present) to cycle through the available texture layers (Default, Political, Detailed - if the respective image files are present).
    *   **Exit Program**: Press the `ESC` key.
4.  **Menu Navigation**:
    *   When the menu is open, click on options like "About," "Instructions," or "Settings" to view relevant information.
    *   The "Settings" menu in the current version primarily displays static information (e.g., current resolution, active texture layer) and may not offer interactive configuration options.

## 🗂️ File Structure (Expected)

*   `main.py`: The main Python script containing all the application logic, including Pygame setup, OpenGL rendering calls, event handling, texture management, camera controls, and menu system.
*   `earth_texture.jpg`: The default Earth texture image file (required).
*   `earth_political.jpg`: (Optional) Texture file for the political map view.
*   `earth_detailed.jpg`: (Optional) Texture file for a detailed terrain view.
*   `README.md`: This documentation file.

*(No other external data files, log files, or separate modules are mentioned for this project in the provided description beyond the main script and image assets.)*

## 📝 Technical Notes

*   **Texture File Check**: The application performs a crucial check for `earth_texture.jpg` at startup. If this file is not found in the same directory as `main.py`, the program will exit.
*   **Optional Textures**: The availability of "Political" and "Detailed" texture layers depends on the presence of `earth_political.jpg` and `earth_detailed.jpg` respectively.
*   **OpenGL & Pygame Integration**: Pygame is used for creating the window, handling user input events (mouse, keyboard), and managing the main loop. PyOpenGL is used for all 3D rendering commands (creating the sphere, applying textures, setting up the camera/view).
*   **Settings Menu**: The current "Settings" menu is described as displaying static information rather than allowing interactive changes. This could be an area for future expansion.
*   **Performance**: Rendering a 3D textured sphere can be resource-intensive. Performance will depend on the user's hardware, the resolution of the textures, and the complexity of the OpenGL rendering pipeline.
*   **Error Logging**: The description mentions `logError` but notes it's "not fully implemented." Robust error logging (e.g., for OpenGL errors, file loading issues) would be beneficial.

## 🤝 Contributing

Contributions to **PyGlobe 3D: Interactive Earth Simulator** are highly encouraged! If you have ideas for:

*   Adding more celestial bodies (Moon, Mars, etc.).
*   Implementing interactive settings in the menu (e.g., toggle auto-rotation, change rotation speed, select specific textures).
*   Adding overlays for city lights, clouds, or real-time weather.
*   Improving rendering performance or visual quality.
*   Implementing more sophisticated camera controls or flight modes.
*   Adding educational information overlays or clickable points of interest on the globe.

1.  Fork the repository.
2.  Create a new branch for your feature (`git checkout -b feature/MoonSimulation`).
3.  Make your changes to `main.py` and add any new assets.
4.  Commit your changes (`git commit -m 'Feature: Add Moon rendering and texture'`).
5.  Push to the branch (`git push origin feature/MoonSimulation`).
6.  Open a Pull Request.

Please ensure your code is well-commented and follows Python best practices (e.g., PEP 8), including type hints where appropriate.

## 📃 License

This project is licensed under the **MIT License**.
(If you have a `LICENSE` file in your repository, refer to it: `See the LICENSE file for details.`)

## 📧 Contact

Project created by **Adrian Lesniak**.
For questions, feedback, or issues, please open an issue on the GitHub repository or contact the repository owner.

---
🌍 _Explore our planet in 3D with interactive controls and multiple visual layers!_
