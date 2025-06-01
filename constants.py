# Game dimensions and physics
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