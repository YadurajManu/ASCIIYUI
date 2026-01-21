"""
Real-Time ASCII Camera - Configuration
"""

# ============================================================================
# ASCII CHARACTER RAMPS
# ============================================================================
# Ordered from lightest (sparse) to darkest (dense)

# Standard 10-character ramp (balanced)
RAMP_STANDARD = " .:-=+*#%@"

# Rich alphanumeric ramp (recommended for faces/detail)
RAMP_ALPHA = " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

# Extended symbols ramp (artistic)
RAMP_SYMBOLS = " `.-':_,^=;><+!rc*/z?sLTv)J7(|Fi{C}fI31tlu[neoZ5Yxjya]2ESwqkP6h9d4VpOGbUAKXHm8RD#$Wg0MNQB%&@"

# Dense 70-character ramp (maximum detail)
RAMP_DENSE = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "[::-1]

# Block characters (stylized, high contrast)
RAMP_BLOCK = " ░▒▓█"

# Minimal (high contrast, simple)
RAMP_MINIMAL = " .:oO@"

# Default ramp to use (now using rich alphanumeric)
DEFAULT_RAMP = RAMP_ALPHA

# ============================================================================
# DISPLAY SETTINGS
# ============================================================================
TARGET_FPS = 30
ASPECT_CORRECTION = 0.55  # Terminal chars are ~2x taller than wide

# ============================================================================
# ENHANCEMENT SETTINGS
# ============================================================================
ENABLE_CLAHE = True           # Adaptive contrast enhancement
CLAHE_CLIP_LIMIT = 3.0        # Increased for sharper contrast
CLAHE_TILE_SIZE = (8, 8)

ENABLE_EDGE_BLEND = True      # Blend edges with grayscale for sharpness
EDGE_BLEND_ALPHA = 0.15       # Subtle edge enhancement

ENABLE_INVERT = False         # Light text on dark background

# Brightness/contrast adjustments
BRIGHTNESS_BOOST = 10         # Add slight brightness
CONTRAST_BOOST = 1.1          # Slight contrast multiplier

# Zoom settings
DEFAULT_ZOOM = 1.0            # 1.0 = no zoom
ZOOM_STEP = 0.1
MAX_ZOOM = 4.0

# Mirror mode
ENABLE_MIRROR = True

# Glitch Effect Settings
ENABLE_GLITCH = False         # Global glitch toggle
GLITCH_INTENSITY = 0.05       # Probability of a glitch event (0.0 to 1.0)
GLITCH_MAX_SHIFT = 5          # Max horizontal line shift

# GIF Export Settings
GIF_DURATION = 100            # Milliseconds per frame in GIF
GIF_FONT_SIZE = 12
GIF_BG_COLOR = (20, 20, 20)   # Dark grey background
GIF_TEXT_COLOR = (240, 240, 240) # Off-white text
