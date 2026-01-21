"""
Real-Time ASCII Camera - Glitch Processor
Adds "cyberpunk" digital noise and character shifts.
"""

import random
import numpy as np
from typing import List
import config

class GlitchProcessor:
    """Applies digital glitch effects to ASCII frames"""
    
    def __init__(self):
        self.intensity = config.GLITCH_INTENSITY
        self.max_shift = config.GLITCH_MAX_SHIFT

    def apply(self, frames: List[str]) -> List[str]:
        """Apply glitch effects to a list of ASCII lines"""
        if not config.ENABLE_GLITCH or not frames:
            return frames
            
        glitched_frames = []
        for line in frames:
            # 1. Random horizontal shift
            if random.random() < self.intensity:
                shift = random.randint(-self.max_shift, self.max_shift)
                line = self._shift_line(line, shift)
            
            # 2. Character noise (digital static)
            if random.random() < self.intensity * 0.5:
                line = self._add_noise(line)
                
            glitched_frames.append(line)
            
        return glitched_frames

    def _shift_line(self, line: str, shift: int) -> str:
        """Cyclically shift a string"""
        if not line: return line
        shift = shift % len(line)
        return line[-shift:] + line[:-shift]

    def _add_noise(self, line: str) -> str:
        """Replace some characters with high-density noise"""
        chars = list(line)
        noise_chars = "!@#$%^&*()_+{}[]|\\<>?"
        for i in range(len(chars)):
            if random.random() < 0.02: # 2% per-character noise
                chars[i] = random.choice(noise_chars)
        return "".join(chars)
