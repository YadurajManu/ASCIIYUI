#!/usr/bin/env python3
"""
Real-Time ASCII Camera
Converts live webcam feed into ASCII art in the terminal.

Developed by: Yaduraj Singh
"""

import sys
import os
import time
import curses
import argparse

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import cv2
import numpy as np

import config
from camera.capture import CameraCapture
from processing.converter import ImageConverter
from processing.mapper import AsciiMapper
from processing.glitch import GlitchProcessor
from rendering.renderer import AsciiRenderer
from rendering.export import GifExporter


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Real-Time ASCII Camera - Live webcam to ASCII art"
    )
    parser.add_argument(
        '-c', '--camera', 
        type=int, 
        default=0,
        help='Camera device ID (default: 0)'
    )
    parser.add_argument(
        '-r', '--ramp',
        choices=['standard', 'alpha', 'symbols', 'dense', 'block', 'minimal'],
        default='alpha',
        help='Character ramp to use (default: alpha)'
    )
    parser.add_argument(
        '--invert',
        action='store_true',
        help='Invert colors (for light terminals)'
    )
    parser.add_argument(
        '--no-enhance',
        action='store_true',
        help='Disable contrast enhancement'
    )
    parser.add_argument(
        '--version',
        action='store_true',
        help='Show version info'
    )
    return parser.parse_args()


def get_ramp(name: str) -> str:
    """Get character ramp by name"""
    ramps = {
        'standard': config.RAMP_STANDARD,
        'alpha': config.RAMP_ALPHA,
        'symbols': config.RAMP_SYMBOLS,
        'dense': config.RAMP_DENSE,
        'block': config.RAMP_BLOCK,
        'minimal': config.RAMP_MINIMAL,
    }
    return ramps.get(name, config.RAMP_ALPHA)


def run_camera(stdscr, args):
    """Main camera loop"""
    # Setup renderer
    renderer = AsciiRenderer()
    renderer.set_screen(stdscr)
    
    # Setup processing
    converter = ImageConverter()
    glitcher = GlitchProcessor()
    
    # Available ramps for live switching
    ramp_list = [
        ('1', 'alpha', config.RAMP_ALPHA),
        ('2', 'symbols', config.RAMP_SYMBOLS),
        ('3', 'dense', config.RAMP_DENSE),
        ('4', 'standard', config.RAMP_STANDARD),
        ('5', 'block', config.RAMP_BLOCK),
        ('6', 'minimal', config.RAMP_MINIMAL),
    ]
    current_ramp_idx = 0
    mapper = AsciiMapper(ramp_list[current_ramp_idx][2])
    current_ramp_name = ramp_list[current_ramp_idx][1]
    
    # State
    show_help = False
    zoom_level = config.DEFAULT_ZOOM
    recording = False
    recorded_frames = []
    
    # Open camera
    camera = CameraCapture(args.camera)
    if not camera.open():
        raise RuntimeError(f"Could not open camera {args.camera}")
    
    frame_time = 1.0 / config.TARGET_FPS
    fps = 0
    frame_count = 0
    fps_update_time = time.time()
    
    try:
        while True:
            current_time = time.time()
            term_width, term_height = renderer.get_dimensions()
            
            # Adjust dimensions for UI
            capture_height = int((term_height - 2) / config.ASPECT_CORRECTION)
            capture_width = term_width
            
            # 1. Capture and Process frame
            # Grayscale Mode
            gray = camera.read_grayscale(capture_width, capture_height, zoom_level, config.ENABLE_MIRROR)
            if gray is None: continue
            enhanced = converter.enhance(gray)
            ascii_lines = mapper.map_frame_fast(enhanced)
            
            # 2. Apply Glitch
            if config.ENABLE_GLITCH:
                ascii_lines = glitcher.apply(ascii_lines)
            
            # 3. Render
            renderer.render_frame(ascii_lines)
            
            # 4. Recording
            if recording:
                recorded_frames.append("\n".join(ascii_lines))
            
            # 5. UI and Status
            rec_status = "● REC" if recording else "     "
            glitch_status = "GLT" if config.ENABLE_GLITCH else "---"
            status = f" {rec_status} | {current_ramp_name} | {glitch_status} | Zoom:{zoom_level:.1f}x | h:Help q:Quit"
            renderer.render_status(status)
            
            if show_help:
                help_lines = [
                    "╔═══════════════════════════════════╗",
                    "║         CREATIVE CONTROLS         ║",
                    "╠═══════════════════════════════════╣",
                    "║  1-6 : Switch Character Ramp       ║",
                    "║  s   : Take Snapshot (.txt)       ║",
                    "║  r   : Start/Stop Recording       ║",
                    "║  g   : Toggle Glitch Effect       ║",
                    "║  + / - : Zoom In / Out            ║",
                    "║  0   : Reset Zoom                 ║",
                    "║  m   : Toggle Mirror Mode         ║",
                    "║  i   : Toggle Invert              ║",
                    "║  e   : Toggle Edge Sharpness      ║",
                    "║  h   : Hide Help                  ║",
                    "║  q   : Quit App                   ║",
                    "╚═══════════════════════════════════╝",
                ]
                sy = (term_height - len(help_lines)) // 2
                sx = (term_width - len(help_lines[0])) // 2
                for i, line in enumerate(help_lines):
                    try: stdscr.addstr(sy + i, sx, line, curses.A_REVERSE)
                    except: pass
                stdscr.refresh()
            
            # 6. Input Handling
            key = renderer.get_key()
            if key in (ord('q'), ord('Q'), 27): break
            elif key in (ord('h'), ord('H')): show_help = not show_help
            elif key in (ord('g'), ord('G')): config.ENABLE_GLITCH = not config.ENABLE_GLITCH
            elif key in (ord('m'), ord('M')): config.ENABLE_MIRROR = not config.ENABLE_MIRROR
            elif key in (ord('i'), ord('I')): config.ENABLE_INVERT = not config.ENABLE_INVERT
            elif key in (ord('e'), ord('E')): config.ENABLE_EDGE_BLEND = not config.ENABLE_EDGE_BLEND
            elif key == ord('+') or key == ord('='): 
                zoom_level = min(config.MAX_ZOOM, zoom_level + config.ZOOM_STEP)
            elif key == ord('-') or key == ord('_'):
                zoom_level = max(1.0, zoom_level - config.ZOOM_STEP)
            elif key == ord('0'): zoom_level = 1.0
            
            elif key in (ord('s'), ord('S')):
                # Snapshot
                return "snapshot", "\n".join(ascii_lines)
                
            elif key in (ord('r'), ord('R')):
                if not recording:
                    recording = True
                    recorded_frames = []
                else:
                    recording = False
                    # Signal to main that we have a recording to save
                    return "record_result", recorded_frames
            elif ord('1') <= key <= ord('6'):
                idx = key - ord('1')
                current_ramp_idx = idx
                current_ramp_name = ramp_list[idx][1]
                mapper.set_ramp(ramp_list[idx][2])
            
            # FPS Calculation
            frame_count += 1
            if current_time - fps_update_time >= 1.0:
                fps = frame_count / (current_time - fps_update_time)
                frame_count = 0
                fps_update_time = current_time
            
            # Sleep to match target FPS
            elapsed = time.time() - current_time
            if elapsed < frame_time: time.sleep(frame_time - elapsed)
            
    finally:
        camera.release()

def discover_cameras(max_cameras: int = 5) -> list:
    """Discover available camera devices"""
    import cv2
    available = []
    for i in range(max_cameras):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            ret, _ = cap.read()
            if ret:
                w, h = int(cap.get(3)), int(cap.get(4))
                available.append((i, f"Camera {i} ({w}x{h})"))
            cap.release()
    return available

def select_camera() -> int:
    """Interactive camera selection"""
    print("\n🎥 Scanning for cameras...")
    cameras = discover_cameras()
    if not cameras: 
        print("❌ No cameras found!")
        return -1
    
    print(f"\n✅ Found {len(cameras)} camera(s):\n")
    for idx, (cam_id, name) in enumerate(cameras):
        print(f"  [{idx + 1}] {name}")
    
    if len(cameras) == 1: return cameras[0][0]
    
    try:
        print("\nSelect a camera (1-{0}): ".format(len(cameras)), end="")
        choice = int(input().strip())
        if 1 <= choice <= len(cameras): return cameras[choice - 1][0]
    except: pass
    return cameras[0][0]

def save_snapshot(frame_text: str):
    """Save a single ASCII frame as a text file"""
    print("\n� Snapshot captured!")
    filename = input("Enter filename for snapshot (e.g., selfie.txt) [or press Enter for 'snapshot.txt']: ").strip()
    if not filename:
        filename = "snapshot.txt"
    if not filename.endswith(".txt"):
        filename += ".txt"
        
    try:
        with open(filename, "w") as f:
            f.write(frame_text)
        print(f"✅ Snapshot saved to {os.path.abspath(filename)}")
    except Exception as e:
        print(f"❌ Error saving snapshot: {e}")

def handle_recording(frames):
    """Handle saved ASCII frames - offers text and GIF export"""
    if not frames: return
    
    print(f"\n🔴 Recorded {len(frames)} frames.")
    choice = input("Save as [T]ext, [G]IF, [B]oth, or [N]one? (t/g/b/n): ").strip().lower()
    
    if choice == 'n' or not choice:
        print("Recording discarded.")
        return

    filename_base = input("Enter base filename (without extension): ").strip()
    if not filename_base:
        filename_base = "recording"

    if choice in ('t', 'b'):
        txt_name = filename_base + ".txt"
        try:
            with open(txt_name, "w") as f:
                f.write("\n\f\n".join(frames))
            print(f"✅ Text saved to {os.path.abspath(txt_name)}")
        except Exception as e:
            print(f"❌ Error saving text: {e}")

    if choice in ('g', 'b'):
        gif_name = filename_base + ".gif"
        exporter = GifExporter()
        exporter.export(frames, gif_name)

def main():
    """Entry point"""
    args = parse_args()
    
    # Camera selection
    if args.camera == 0:
        camera_id = select_camera()
        if camera_id == -1: sys.exit(1)
        args.camera = camera_id
    
    print(f"\n🚀 Starting ASCII Camera...")
    time.sleep(0.5)
    
    # Run loop
    try:
        while True:
            result = curses.wrapper(lambda stdscr: run_camera(stdscr, args))
            
            # 1. Handle Snapshot
            if isinstance(result, tuple) and result[0] == "snapshot":
                save_snapshot(result[1])
                input("\nPress Enter to return to camera...")
                continue # Go back to camera
                
            # 2. Handle Recording
            elif isinstance(result, tuple) and result[0] == "record_result":
                handle_recording(result[1])
                input("\nPress Enter to return to camera...")
                continue # Go back to camera
                
            # 3. Handle Quit
            break
            
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
