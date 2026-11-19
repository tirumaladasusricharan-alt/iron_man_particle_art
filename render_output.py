import cv2
import time
import numpy as np
import mediapipe as mp
import os
import sys
import subprocess
from tony2 import get_person_mask, render_halftone, PROCESS_WIDTH

def find_ffmpeg():
    # Check bundled imageio_ffmpeg
    try:
        import imageio_ffmpeg
        exe = imageio_ffmpeg.get_ffmpeg_exe()
        if os.path.exists(exe):
            return exe
    except Exception:
        pass
    
    # Common Windows path for imageio_ffmpeg binary
    fallback = os.path.expandvars(r"%APPDATA%\Python\Python314\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v9.0.2.exe")
    if os.path.exists(fallback):
        return fallback

    return "ffmpeg"

def render_video(input_video="video.mp4", output_video="output_with_audio.mp4"):
    cap = cv2.VideoCapture(input_video)
    if not cap.isOpened():
        print(f"Error: Cannot open {input_video}")
        return

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    temp_video = "temp_render.mp4"
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(temp_video, fourcc, fps, (width, height))

    mp_selfie = mp.solutions.selfie_segmentation
    t0 = time.time()
    print(f"Rendering {total_frames} frames from '{input_video}'...")

    with mp_selfie.SelfieSegmentation(model_selection=1) as segmenter:
        count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            if width > PROCESS_WIDTH:
                process_height = max(1, round(height * PROCESS_WIDTH / width))
                process_frame = cv2.resize(frame, (PROCESS_WIDTH, process_height), interpolation=cv2.INTER_AREA)
            else:
                process_frame = frame

            mask = get_person_mask(segmenter, process_frame)
            canvas = render_halftone(process_frame, mask)
            if canvas.shape[:2] != (height, width):
                canvas = cv2.resize(canvas, (width, height), interpolation=cv2.INTER_NEAREST)
            
            out.write(canvas)
            count += 1
            if count % 50 == 0 or count == total_frames:
                print(f"Rendered {count}/{total_frames} frames...")

    cap.release()
    out.release()
    print(f"Frames rendered in {time.time()-t0:.2f}s.")

    # Mux audio with ffmpeg if available
    ffmpeg_exe = find_ffmpeg()
    print(f"Muxing audio using {ffmpeg_exe}...")
    try:
        subprocess.run(
            [
                ffmpeg_exe, "-y",
                "-i", temp_video,
                "-i", input_video,
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                "-c:a", "aac",
                "-map", "0:v:0",
                "-map", "1:a:0",
                "-shortest",
                output_video
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        if os.path.exists(temp_video):
            os.remove(temp_video)
        print(f"Successfully created '{output_video}' with audio!")
    except Exception as e:
        print(f"Muxing audio failed ({e}). Renaming temp video to {output_video}")
        if os.path.exists(output_video):
            os.remove(output_video)
        os.rename(temp_video, output_video)

if __name__ == "__main__":
    inp = sys.argv[1] if len(sys.argv) > 1 else "video.mp4"
    out = sys.argv[2] if len(sys.argv) > 2 else "output_with_audio.mp4"
    render_video(inp, out)
