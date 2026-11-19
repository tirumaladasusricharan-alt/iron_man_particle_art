<div align="center">

# 🤖❤️‍🔥 Iron Man Neon Halftone Particle Art

**Live neon halftone dithering and person segmentation animation with seamless infinite replay and synchronized audio.**

![preview](preview.gif)

</div>

---

### ✨ Overview

This project transforms video footage into a stylized neon halftone / particle animation using **MediaPipe Selfie Segmentation** and **Bayer matrix dithering**. It isolates the subject (Iron Man / Tony Stark) and renders dynamic cyan and hot pink halftone dots in real-time.

### 🚀 What's New in This Version
- 🔄 **Infinite Seamless Replay**: Automatically rewinds and loops continuously without pausing or stopping.
- 🚫 **Autoplay (No Pause Button)**: Stripped out manual pause buttons for continuous playback.
- 🔊 **Synchronized Audio Playback**: Extracted audio loop that syncs directly with the animation replay.
- 🎬 **Offline Video Renderer (`render_output.py`)**: Export any video into a standalone **H.264 + AAC audio MP4** (`output.mp4`).
- 🌐 **Web Player (`index.html`)**: Clean browser player with zero control overlays, auto-looping, and a sound toggle.
- 🖼️ **Animated GIF Export (`output.gif` / `preview.gif`)**: High-quality GIF ready for GitHub previews and social media.

---

### 🎬 How It Works

1. **Person Segmentation**: Uses MediaPipe's Selfie Segmentation model to generate a mask of the person in each frame.
2. **Grayscale & Luminance Mapping**: The frame luminance is computed and masked to keep the background deep violet/black.
3. **Bayer 4×4 Halftone Dithering**: Applies an ordered Bayer matrix threshold to generate neon halftone dots.
4. **Cyberpunk Color Palette**:
   - Background: Deep Black-Violet `(10, 0, 18)`
   - Primary Particles: Hot Pink `(155, 20, 245)`
   - Highlights & Midtones: Vibrant Cyan `(255, 235, 65)`
   - Peak Highlights: Pale Cyan `(245, 255, 235)`

---

### 🛠️ Tech Stack & Requirements

- **Python 3.12**
- **OpenCV (`opencv-contrib-python`)**
- **MediaPipe (`mediapipe==0.10.21`)**
- **NumPy (`numpy<2`)**
- **FFmpeg** (for audio extraction and H.264 muxing)

---

### 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/tirumaladasusricharan-alt/iron_man_particle_art.git
   cd iron_man_particle_art
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

### 🎮 Usage

#### 1. Run Live Interactive Window
```bash
python tony2.py
```
- Plays the animation in a live window with synchronized looping audio.
- Continuously loops infinitely.
- Press `Esc` anytime to exit.

#### 2. Render Full Video with Audio
```bash
python render_output.py [input_video.mp4] [output_video.mp4]
```
- By default renders `video.mp4` to `output.mp4` with full H.264 compression and AAC audio.

#### 3. View in Web Browser
Open `index.html` in any web browser to view the clean autoplaying loop with no player bars.

---

### 📝 Credits & Note
Created and updated by [Charan](https://github.com/tirumaladasusricharan-alt).  
Original concept inspired by [Shravani](https://github.com/shraaaa17/ascii-IRONMAN).
