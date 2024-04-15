import pygame

from components.shapes import convert_shape_format
from src.variables import (
    S_WIDTH, S_HEIGHT, PLAY_WIDTH, PLAY_HEIGHT, BLOCK_SIZE, TOP_LEFT_X, TOP_LEFT_Y)

# GRID CREATION
def create_grid(locked_pos=None):
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]

    for i, row in enumerate(grid):
        for j, _ in enumerate(row):
            if (j, i) in locked_pos:
                c = locked_pos[(j, i)]
                grid[i][j] = c
    return grid

# VALID SPACE
def valid_space(shape, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]
    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True

# CHECK LOST
def check_lost(positions):
    for pos in positions:
        _, y = pos
        if y < 1:
            return True
    return False

def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont("comicsans", size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(
        label, (
            TOP_LEFT_X + PLAY_WIDTH / 2 - (label.get_width() / 2),
            TOP_LEFT_Y + PLAY_HEIGHT / 2 - label.get_height() / 2
        )
    )

# GRID LINES
def draw_grid(surface, grid):
    sx = TOP_LEFT_X
    sy = TOP_LEFT_Y

    for i, row in enumerate(grid):
        pygame.draw.line(
            surface, (50, 50, 50),
            (sx, sy + i * BLOCK_SIZE),
            (sx + PLAY_WIDTH - 5, sy + i * BLOCK_SIZE),
            2
        )

        for j, _ in enumerate(row):
            pygame.draw.line(
                surface, (50, 50, 50),
                (sx + j * BLOCK_SIZE, sy),
                (sx + j * BLOCK_SIZE, sy + PLAY_HEIGHT - 3),
                2
            )

def clear_rows(grid, locked):
    inc = 0
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except KeyError:
                    continue

    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                new_key = (x, y + inc)
                locked[new_key] = locked.pop(key)

    return inc

# UPCOMING SHAPES PREVIEW
def draw_next_shapes(next_shapes, surface):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, (255, 255, 255))
    sx = TOP_LEFT_X + PLAY_WIDTH + 50
    sy = TOP_LEFT_Y + PLAY_HEIGHT / 2 - 100

    for k, shape in enumerate(next_shapes):
        formatted = shape.shape[shape.rotation % len(shape.shape)]

        for i, line in enumerate(formatted):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    pygame.draw.rect(
                        surface,
                        shape.color,
                        (sx + j * BLOCK_SIZE + k * 100, sy + i *
                        BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0
                    )
    surface.blit(label, (sx + 10, sy - 70))

# MAIN GAME WINDOW 
def draw_window(surface, grid, score=0, last_score=0):

    # Main Window
    surface.fill((31, 45, 86)) # Window Background
    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('Tetris', 1, (255, 255, 255))
    surface.blit(label, (TOP_LEFT_X + PLAY_WIDTH / 2 - (label.get_width() / 2), 15))

    # Score
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Score: ' + str(score), 1, (255, 255, 255))
    sx = TOP_LEFT_X + PLAY_WIDTH + 50
    sy = TOP_LEFT_Y + PLAY_HEIGHT / 2 - 100
    surface.blit(label, (sx + 20, sy + 160))

    # High Score
    label = font.render('High Score: ' + last_score, 1, (255, 255, 255))
    sx = TOP_LEFT_X - 250
    sy = TOP_LEFT_Y + 200
    surface.blit(label, (sx + 20, sy + 160)) 

    # Grid Background 
    bg  = pygame.image.load("components/play-area-grid.png")
    surface.blit(bg, (TOP_LEFT_X, TOP_LEFT_Y))

    # PLAY AREA
    for i, row in enumerate(grid):
        for j, color in enumerate(row):
            if color != (0, 0, 0):  # If cell is not empty
                pygame.draw.rect(
                    surface,
                    color,  # Draw the cell color
                    (TOP_LEFT_X + j * BLOCK_SIZE, TOP_LEFT_Y + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0
                )

    draw_grid(surface, grid) # GRID LINES
    pygame.draw.rect(surface, (255, 255, 255), (TOP_LEFT_X, TOP_LEFT_Y, PLAY_WIDTH, PLAY_HEIGHT), 5)
    


def draw_modal(surface):
    # Draw filled rectangle (modal)
    pygame.draw.rect(surface, (0, 0, 0), (TOP_LEFT_X + 50, TOP_LEFT_Y + 200, 200, 200))

    # Draw outline rectangle
    pygame.draw.rect(surface, (255, 255, 255), (TOP_LEFT_X + 50, TOP_LEFT_Y + 200, 200, 200), 3)

    # Render and blit labels
    font = pygame.font.SysFont('comicsans', 30)
    resume_label = font.render('Resume', 1, (255, 255, 255))
    restart_label = font.render('Restart', 1, (255, 255, 255))
    surface.blit(resume_label, (TOP_LEFT_X + 100, TOP_LEFT_Y + 250))
    surface.blit(restart_label, (TOP_LEFT_X + 100, TOP_LEFT_Y + 320))
