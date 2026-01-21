"""
Real-Time ASCII Camera - Camera Capture Module
"""

import cv2
import numpy as np
from typing import Optional, Tuple


class CameraCapture:
    """Handles webcam capture and frame preprocessing"""
    
    def __init__(self, camera_id: int = 0):
        self.camera_id = camera_id
        self.cap: Optional[cv2.VideoCapture] = None
        self._width = 0
        self._height = 0
    
    def open(self) -> bool:
        """Open the camera"""
        self.cap = cv2.VideoCapture(self.camera_id)
        if not self.cap.isOpened():
            return False
        
        # Get native resolution
        self._width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self._height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Optimize for speed
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        
        return True
    
    def read(self) -> Tuple[bool, Optional[np.ndarray]]:
        """Read a frame from the camera"""
        if self.cap is None:
            return False, None
        return self.cap.read()
    
    def read_grayscale(self, target_width: int, target_height: int, zoom: float = 1.0, mirror: bool = False) -> Optional[np.ndarray]:
        """
        Read a frame, apply zoom/mirror, resize it, and convert to grayscale.
        """
        ret, frame = self.read()
        if not ret or frame is None:
            return None
        
        # Mirroring
        if mirror:
            frame = cv2.flip(frame, 1)
            
        # Zoom (Cropping)
        if zoom > 1.0:
            h, w = frame.shape[:2]
            new_h, new_w = int(h / zoom), int(w / zoom)
            start_y, start_x = (h - new_h) // 2, (w - new_w) // 2
            frame = frame[start_y:start_y+new_h, start_x:start_x+new_w]
            
        # Resize to target dimensions
        resized = cv2.resize(frame, (target_width, target_height), interpolation=cv2.INTER_AREA)
        
        # Convert to grayscale
        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        
        return gray

    def release(self):
        """Release the camera"""
        if self.cap is not None:
            self.cap.release()
            self.cap = None
    
    @property
    def native_resolution(self) -> Tuple[int, int]:
        """Get native camera resolution (width, height)"""
        return self._width, self._height
    
    def __enter__(self):
        self.open()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()
