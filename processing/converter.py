"""
Real-Time ASCII Camera - Image Converter
Handles grayscale conversion, contrast enhancement, and edge detection.
"""

import cv2
import numpy as np

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


class ImageConverter:
    """Processes grayscale images for optimal ASCII conversion"""
    
    def __init__(self):
        # Initialize CLAHE (Contrast Limited Adaptive Histogram Equalization)
        self.clahe = cv2.createCLAHE(
            clipLimit=config.CLAHE_CLIP_LIMIT,
            tileGridSize=config.CLAHE_TILE_SIZE
        )
    
    def enhance(self, gray: np.ndarray) -> np.ndarray:
        """
        Apply enhancements to improve ASCII output quality.
        """
        result = gray.copy().astype(np.float32)
        
        # Apply brightness and contrast adjustments
        if hasattr(config, 'CONTRAST_BOOST'):
            result = result * config.CONTRAST_BOOST
        if hasattr(config, 'BRIGHTNESS_BOOST'):
            result = result + config.BRIGHTNESS_BOOST
        
        # Clip to valid range and convert back
        result = np.clip(result, 0, 255).astype(np.uint8)
        
        # Apply CLAHE for better local contrast
        if config.ENABLE_CLAHE:
            result = self.clahe.apply(result)
        
        # Blend with edge detection for sharper output
        if config.ENABLE_EDGE_BLEND:
            edges = self._detect_edges(result)
            alpha = config.EDGE_BLEND_ALPHA
            result = cv2.addWeighted(result, 1 - alpha, edges, alpha, 0)
        
        # Invert if needed (for light-on-dark terminals)
        if config.ENABLE_INVERT:
            result = 255 - result
        
        return result
    
    def _detect_edges(self, gray: np.ndarray) -> np.ndarray:
        """Detect edges using Sobel operator"""
        grad_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        magnitude = np.sqrt(grad_x**2 + grad_y**2)
        magnitude = np.clip(magnitude, 0, 255).astype(np.uint8)
        return magnitude
