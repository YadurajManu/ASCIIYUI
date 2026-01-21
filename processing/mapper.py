"""
Real-Time ASCII Camera - ASCII Mapper
Converts pixel intensity values to ASCII characters.
"""

import numpy as np
from typing import List

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


class AsciiMapper:
    """Maps grayscale pixel values to ASCII characters"""
    
    def __init__(self, ramp: str = None):
        self.ramp = ramp if ramp else config.DEFAULT_RAMP
        self._ramp_len = len(self.ramp)
        self._lookup = self._build_lookup_table()
    
    def _build_lookup_table(self) -> List[str]:
        """Build a 256-entry lookup table for O(1) character mapping"""
        lookup = []
        for i in range(256):
            index = int(i / 256 * self._ramp_len)
            index = min(index, self._ramp_len - 1)
            lookup.append(self.ramp[index])
        return lookup
    
    def set_ramp(self, ramp: str):
        """Change the character ramp"""
        self.ramp = ramp
        self._ramp_len = len(ramp)
        self._lookup = self._build_lookup_table()
    
    def map_frame_fast(self, gray: np.ndarray) -> List[str]:
        """Optimized version using numpy vectorization."""
        indices = (gray.astype(np.float32) / 256 * self._ramp_len).astype(np.int32)
        indices = np.clip(indices, 0, self._ramp_len - 1)
        ramp_array = np.array(list(self.ramp))
        char_frame = ramp_array[indices]
        return [''.join(row) for row in char_frame]

