# Earth Simulator

## Overview
Earth Simulator is a 3D visualization tool built with PyOpenGL and Pygame, created by Adrian Lesniak. It renders a rotating Earth globe with multiple textures (terrain, political map, high-definition terrain). Users can interact with the globe through mouse controls, switch between texture layers, and access a menu for information and settings.

## Features
- **3D Globe Rendering**: Displays a textured Earth sphere using OpenGL.
- **Texture Layers**: Switch between Default (terrain), Political (countries), and Detailed (HD terrain) textures.
- **Interactive Controls**:
  - Drag with mouse to rotate the globe.
  - Scroll wheel to zoom in/out.
  - Double-click to reset view.
- **Menu System**: Includes About, Instructions, and Settings sections, toggled with a Menu button.
- **Smooth Animation**: Supports auto-rotation and momentum-based rotation for a natural feel.

## Requirements
- Python 3.6+
- Libraries:
  - `pygame`
  - `PyOpenGL`
  - `numpy`
  - `Pillow`
- Texture file: `earth_texture.jpg` (plus optional `earth_political.jpg`, `earth_detailed.jpg`) in the script directory.

Install dependencies using:
```bash
pip install pygame PyOpenGL numpy Pillow
```

## Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```
2. Install required libraries (see Requirements).
3. Place `earth_texture.jpg` (and optional texture files) in the script directory.
4. Run the application:
   ```bash
   python main.py
   ```

## Usage
1. Launch the simulator to view the rotating Earth globe.
2. **Controls**:
   - **Mouse Drag**: Rotate the globe.
   - **Mouse Wheel**: Zoom in/out.
   - **Double-Click**: Reset to initial view.
   - **M Key**: Toggle menu.
   - **Menu Button**: Access About, Instructions, or Settings.
   - **Layer Button**: Cycle through texture layers.
   - **ESC**: Exit the program.
3. Explore the menu for additional information or to view settings.

## File Structure
- `main.py`: Main script containing the simulator logic, OpenGL rendering, and UI.
- `earth_texture.jpg`: Default texture file (required).
- `earth_political.jpg`, `earth_detailed.jpg`: Optional texture files.
- `README.md`: This file, providing project documentation.

## Notes
- Ensure texture files are in the same directory as `main.py`. The simulator checks for `earth_texture.jpg` at startup and exits if missing.
- Optional textures (`earth_political.jpg`, `earth_detailed.jpg`) enhance layer options but are not required.
- The Settings menu displays static information (e.g., resolution, current layer) and is not fully interactive in this version.

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make changes and commit (`git commit -m "Add feature"`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact
For questions or feedback, open an issue on GitHub or contact the repository owner.