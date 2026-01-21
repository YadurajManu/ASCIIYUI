# 🎥 AsciiCam

A real-time ASCII Camera for your terminal! Converts live webcam feed into high-quality ASCII art with creative filters and recording capabilities.

## ✨ Features
- **Live ASCII Feed**: Real-time conversion with high-quality mapping.
- **Creative Controls**: Live switching between different character ramps.
- **Glitch Mode**: Cyberpunk-style digital noise filter.
- **Zoom & Mirror**: 1x to 4x zoom and horizontal flip.
- **Recording**: Capture your ASCII stream to a `.txt` file or an animated **GIF**.
- **Snapshot**: Instantly save a frame as ASCII art.

## 🚀 Installation

### Using Homebrew (Recommended)
```bash
brew tap YadurajManu/homebrew-tap
brew install asciicam
```

### Manual Installation
```bash
git clone https://github.com/YaduEnc/AsciiCam.git
cd AsciiCam
pip install -r requirements.txt
python main.py
```

## ⌨️ Controls
| Key | Action |
|-----|--------|
| `1-6` | Switch character ramps |
| `s` | Take Snapshot (.txt) |
| `r` | Start/Stop Recording |
| `g` | Toggle Glitch Effect |
| `+` / `-` | Zoom In / Out |
| `m` | Toggle Mirror Mode |
| `h` | Toggle Help |
| `q` | Quit |

## 🛠 Project Structure
- `main.py`: Entry point and live loop.
- `camera/`: Webcam capture and processing logic.
- `processing/`: Image enhancement and ASCII mapping.
- `rendering/`: Terminal output and export utilities.

---
Developed by **Yaduraj Singh**
