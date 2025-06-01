# Game dimensions and physics
import numpy as np

WIDTH, HEIGHT = 800, 400
INFO_HEIGHT = 50
FPS = 60
BALL_RADIUS = 15
POCKET_RADIUS = 30
FRICTION = 0.99
MAXIMUM_FORCE = 120
CUE_STRENGTH_COEFFICIENT = 0.05 # Factor for converting mouse drag to impulse

# Define pockets at global scope
POCKETS = [(0, 0), (WIDTH, 0), (0, HEIGHT), (WIDTH, HEIGHT)]

# Colors
GREEN = (0, 128, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
BROWN = (139, 69, 19)
PINK = (255, 192, 203)
GRAY = (128, 128, 128)

# Hit Spot Selector UI
HIT_SPOT_SELECTOR_CENTER_X = WIDTH - 50  # Position in the info panel
HIT_SPOT_SELECTOR_CENTER_Y = HEIGHT + INFO_HEIGHT // 2
HIT_SPOT_BG_RADIUS = 22
HIT_SPOT_BUTTON_RADIUS = 6
HIT_SPOT_BUTTON_OFFSET = 13 # Distance from center of selector to center of button

# Angle offset for side hits (in radians)
SIDE_ANGLE_OFFSET = np.deg2rad(7.0)  # Increased to 7.0 degrees

HIT_SPOT_EFFECTS = {
    # (relative_x_offset, relative_y_offset, label, angle_offset_rad)
    "TOP_LEFT":     (-1, -1, "TL", -SIDE_ANGLE_OFFSET),
    "TOP_CENTER":   ( 0, -1, "T",  0),
    "TOP_RIGHT":    ( 1, -1, "TR", SIDE_ANGLE_OFFSET),
    "MIDDLE_LEFT":  (-1,  0, "L",  -SIDE_ANGLE_OFFSET),
    "CENTER":       ( 0,  0, "C",  0),
    "MIDDLE_RIGHT": ( 1,  0, "R",  SIDE_ANGLE_OFFSET),
    "BOTTOM_LEFT":  (-1,  1, "BL", -SIDE_ANGLE_OFFSET),
    "BOTTOM_CENTER":( 0,  1, "B",  0),
    "BOTTOM_RIGHT": ( 1,  1, "BR", SIDE_ANGLE_OFFSET),
}

# Visualizations
INFO_FONT_SCALE = 1
VECTOR_SCALE = 1