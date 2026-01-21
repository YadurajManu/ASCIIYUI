"""
Real-Time ASCII Camera - Export Utility
Handles converting ASCII frames to image and animated GIF.
"""

import os
from PIL import Image, ImageDraw, ImageFont
import config

class GifExporter:
    """Converts captured ASCII frames into an animated GIF"""
    
    def __init__(self):
        self.font_size = config.GIF_FONT_SIZE
        # Try to load a monospaced font
        try:
            # Common monospaced fonts on macOS
            self.font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Courier New.ttf", self.font_size)
        except:
            try:
                self.font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", self.font_size)
            except:
                self.font = ImageFont.load_default()

    def export(self, frames: list, filename: str):
        """
        Export a list of ASCII frame strings to an animated GIF.
        
        Args:
            frames: List of strings, each being a full ASCII frame
            filename: Output path (e.g., "output.gif")
        """
        if not frames:
            return False
            
        print(f"🎬 Exporting GIF ({len(frames)} frames)... This may take a moment.")
        
        # 1. Determine image size based on first frame
        lines = frames[0].split('\n')
        if not lines: return False
        
        # Character dimensions (approximate)
        bbox = self.font.getbbox("A")
        char_width = bbox[2] - bbox[0]
        char_height = bbox[3] - bbox[1] + 2 # Add some vertical padding
        
        img_width = char_width * len(lines[0])
        img_height = char_height * len(lines)
        
        gif_frames = []
        for i, frame_text in enumerate(frames):
            # Create a new image for each frame
            img = Image.new('RGB', (img_width, img_height), color=config.GIF_BG_COLOR)
            draw = ImageDraw.Draw(img)
            
            # Draw each line
            for y, line in enumerate(frame_text.split('\n')):
                draw.text((0, y * char_height), line, font=self.font, fill=config.GIF_TEXT_COLOR)
            
            gif_frames.append(img)
            
            if i % 10 == 0:
                print(f"   Processed {i}/{len(frames)} frames...")

        # 2. Save as animated GIF
        if not filename.endswith(".gif"):
            filename += ".gif"
            
        gif_frames[0].save(
            filename,
            save_all=True,
            append_images=gif_frames[1:],
            duration=config.GIF_DURATION,
            loop=0,
            optimize=True
        )
        
        print(f"✅ GIF saved to {os.path.abspath(filename)}")
        return True
