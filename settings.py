# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GREY = (45, 45, 45)
LIGHT_GREY = (100, 100, 100)

# GAME CONSTANTS
# screen width
WIDTH = 800
# screen height
HEIGHT = 400
# rate at which our game will run
FPS = 30
# center of "map" screen portion
MAP_CENTER = (WIDTH / 4, HEIGHT / 2)
# list of border coords that stop actors
MAP_BORDER = [0, 375]
# middle of x axis
WIDTH_CENTER = (WIDTH / 2)
# middle of y axis
HEIGHT_CENTER = (HEIGHT / 2)
# center of "UI" screen portion
UI_CENTER = (((WIDTH / 4) * 3), HEIGHT / 2)
# title of the game will show up at top of window
TITLE = "Classic Crawler"
# background color for where it applies
BG_COLOR = DARK_GREY

# useful grid settings
# size of each tile
TILE_SIZE = 25
GRID_WIDTH = (WIDTH / TILE_SIZE)
GRID_HEIGHT = (HEIGHT / TILE_SIZE)
# used when placing tiles to the grid
TILE_TO_GRID = (WIDTH_CENTER / TILE_SIZE)
