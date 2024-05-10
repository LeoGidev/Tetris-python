import pygame
import random
# Dimensiones de la pantalla
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
PLAY_WIDTH = 10
PLAY_HEIGHT = 20
TOP_LEFT_X = (SCREEN_WIDTH - PLAY_WIDTH * BLOCK_SIZE) // 2
TOP_LEFT_Y = SCREEN_HEIGHT - PLAY_HEIGHT * BLOCK_SIZE

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)

# Formas de las piezas
S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['0000.',
      '.....',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]
SHAPES = [S, Z, I, O, J, L, T]
SHAPES_COLORS = [GREEN, RED, CYAN, YELLOW, BLUE, ORANGE, PURPLE]

# Clase para las piezas
class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = SHAPES_COLORS[SHAPES.index(shape)]
        self.rotation = 0

# Función para crear una pieza aleatoria
def create_piece():
    return Piece(5, 0, random.choice(SHAPES))

# Función para convertir la posición de la matriz en posición en pantalla
def convert_shape_format(piece):
    positions = []
    format = piece.shape[piece.rotation % len(piece.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((piece.x + j, piece.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions

# Función para verificar colisión de una pieza
def valid_space(piece, grid):
    accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == BLACK] for i in range(20)]
    accepted_positions = [j for sub in accepted_positions for j in sub]

    formatted = convert_shape_format(piece)

    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
    return True

# Función para limpiar las líneas completadas
def clear_rows(grid, locked):
    inc = 0
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if BLACK not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue

    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)

    return inc

# Función para dibujar el próximo bloque
def draw_next_shape(shape, screen):
    font = pygame.font.SysFont('arial', 30)
    label = font.render('Next Shape', 1, WHITE)

    sx = TOP_LEFT_X + PLAY_WIDTH + 50
    sy = TOP_LEFT_Y + PLAY_HEIGHT/2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(screen, shape.color, (sx + j*BLOCK_SIZE, sy + i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    screen.blit(label, (sx + 10, sy - 30))


# Función para dibujar el borde del tablero
def draw_grid(screen, grid):
    for i in range(len(grid)):
        pygame.draw.line(screen, GRAY, (TOP_LEFT_X, TOP_LEFT_Y + i*BLOCK_SIZE), (TOP_LEFT_X + PLAY_WIDTH*BLOCK_SIZE, TOP_LEFT_Y + i*BLOCK_SIZE))
        for j in range(len(grid[i])):
            pygame.draw.line(screen, GRAY, (TOP_LEFT_X + j*BLOCK_SIZE, TOP_LEFT_Y), (TOP_LEFT_X + j*BLOCK_SIZE, TOP_LEFT_Y + PLAY_HEIGHT*BLOCK_SIZE))

# Función para dibujar el tablero
def draw_window(screen, grid):
    screen.fill(BLACK)
    font = pygame.font.SysFont('arial', 60)
    label = font.render('Tetris', 1, WHITE)
    screen.blit(label, (TOP_LEFT_X + PLAY_WIDTH/2 - (label.get_width()/2), 30))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(screen, grid[i][j], (TOP_LEFT_X + j*BLOCK_SIZE, TOP_LEFT_Y + i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    pygame.draw.rect(screen, RED, (TOP_LEFT_X, TOP_LEFT_Y, PLAY_WIDTH * BLOCK_SIZE, PLAY_HEIGHT * BLOCK_SIZE), 5)

    draw_grid(screen, grid)