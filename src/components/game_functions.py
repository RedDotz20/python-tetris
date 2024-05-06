import pygame

from src.components.shapes import convert_shape_format

# from components.shapes import convert_shape_format
from src.constants.global_variables import (
    # S_WIDTH, S_HEIGHT,
    PLAY_WIDTH, PLAY_HEIGHT, BLOCK_SIZE, TOP_LEFT_X, TOP_LEFT_Y)

pygame.font.init()
pygame.mixer.init()

GAME_FONT = "assets/fonts/Lexend.ttf"

font = pygame.font.Font(GAME_FONT, 30)
clear = pygame.mixer.Sound("assets/sounds/clear.ogg")
place = pygame.mixer.Sound("assets/sounds/place.ogg")

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

# RENDERING CENTERED TEXT
def draw_text_middle(surface, text, _size, color):
    label = font.render(text, 1, color)
    surface.blit(
        label, (
            TOP_LEFT_X + PLAY_WIDTH / 2 - (label.get_width() / 2),
            TOP_LEFT_Y + PLAY_HEIGHT / 2 - label.get_height() / 2
        )
    )

# RENDER CENTERED LOW SUBTEXT
def draw_subtext_low(surface, text, _size, color):
    label = font.render(text, 1, color)
    surface.blit(
        label, (
            TOP_LEFT_X + PLAY_WIDTH / 2 - (label.get_width() / 2),
            TOP_LEFT_Y + PLAY_HEIGHT + 20 / 2 - label.get_height() / 2
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

# CLEAR ROWS
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
        clear.play()
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                new_key = (x, y + inc)
                locked[new_key] = locked.pop(key)

    place.play()
    return inc

# UPCOMING SHAPES PREVIEW
def draw_next_shapes(next_shapes, surface):
    label = font.render('NEXT SHAPE', 1, (224, 209, 99))
    sx = TOP_LEFT_X + PLAY_WIDTH + 30
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
    
def draw_hold_shape_area(surface, screen, hold_used=0):
    
    label = font.render('HOLD', 1, (224, 209, 99))
    sx = TOP_LEFT_X + 250
    sy = TOP_LEFT_Y + 25
    surface.blit(label, (sx + 20, sy + 160))
    surface.blit(hold_used, (sx + 20, sy + 220))

# MAIN GAME WINDOW
def draw_window(surface, grid, score=0, last_score=0, milestone=1,hold_shape=None,):

    # Whole Window
    surface.fill((31, 45, 86)) # Window Background
    title = pygame.font.Font(GAME_FONT, 60)
    label = title.render('TETRIS', 1, (224, 209, 99))
    surface.blit(label, (15, 15))

    # Current Score
    label = font.render('SCORE', 1, (224, 209, 99))
    score_text = font.render(str(score), 1, (255, 255, 255))
    sx = TOP_LEFT_X + PLAY_WIDTH + 30
    sy = TOP_LEFT_Y + PLAY_HEIGHT / 2 - 100
    surface.blit(label, (sx + 20, sy + 160))
    surface.blit(score_text, (sx + 20, sy + 200))
    
    # HOLD
    label = font.render('HOLD', 1, (224, 209, 99))
    high_score = font.render(last_score, 1, (255, 255, 255))
    sx = TOP_LEFT_X - 250
    sy = TOP_LEFT_Y - 50
    surface.blit(label, (sx + 20, sy + 160))
    
    fixed_position = (1, 1)  # Adjust these values as needed
    if hold_shape:
        
        sx = TOP_LEFT_X
        sy = TOP_LEFT_Y
        # Render the hold shape
        shape_pos = convert_shape_format(hold_shape)
        # Set a fixed position for the hold piece
        for _, (x, y) in enumerate(shape_pos):
            if y > -1:
                # Calculate the position for drawing the hold piece
                hold_piece_x = TOP_LEFT_X - 150
                hold_piece_y = TOP_LEFT_Y + 200
                pygame.draw.rect(
                    surface,
                    hold_shape.color,
                    (
                        hold_piece_x,
                        hold_piece_y,
                        BLOCK_SIZE,
                        BLOCK_SIZE
                    ), 0
                )

    # High Score
    label = font.render('HIGH SCORE', 1, (224, 209, 99))
    high_score = font.render(last_score, 1, (255, 255, 255))
    sx = TOP_LEFT_X - 250
    sy = TOP_LEFT_Y + 275
    surface.blit(label, (sx + 20, sy + 160))
    surface.blit(high_score, (sx + 20, sy + 220))

    # Milestone / Level
    label = font.render("LEVEL", 1, (255, 255, 255))
    current_level = font.render(str(milestone), 1, (255, 255, 255))
    sx = TOP_LEFT_X - 250
    sy = TOP_LEFT_Y + 150
    surface.blit(label, (sx + 20, sy + 160))
    surface.blit(current_level, (sx + 20, sy + 220))

    # Patterned Background
    bg  = pygame.image.load("assets/images/play-area-grid.png")
    surface.blit(bg, (TOP_LEFT_X, TOP_LEFT_Y))

    # Play Area Rendering
    for i, row in enumerate(grid):
        for j, color in enumerate(row):
            if color != (0, 0, 0):
                pygame.draw.rect(
                    surface,
                    color,
                    (
                        TOP_LEFT_X + j * BLOCK_SIZE,
                        TOP_LEFT_Y + i * BLOCK_SIZE,
                        BLOCK_SIZE,
                        BLOCK_SIZE
                    ), 0
                )

    draw_grid(surface, grid) # Grid Lines
    pygame.draw.rect(
        surface,
        (255, 255, 255),
        (TOP_LEFT_X, TOP_LEFT_Y, PLAY_WIDTH, PLAY_HEIGHT),
        5
    ) # Play Area Outline

def draw_modal(surface):
    # Modal Screen
    pygame.draw.rect(surface, (0, 0, 0), (TOP_LEFT_X + 50, TOP_LEFT_Y + 200, 200, 200))
    pygame.draw.rect(surface,
        (255, 255, 255),
        (TOP_LEFT_X + 50, TOP_LEFT_Y + 200, 200, 200),
        3
    ) # Outline

    # Content and Rendering
    resume_label = font.render('RESUME', 1, (255, 255, 255))
    restart_label = font.render('RESTART', 1, (255, 255, 255))
    surface.blit(resume_label, (TOP_LEFT_X + 85, TOP_LEFT_Y + 250))
    surface.blit(restart_label, (TOP_LEFT_X + 85, TOP_LEFT_Y + 320))

# Scores per Milestones
def calculate_score(_score, milestone):
    if milestone == 1:
        return 10
    elif milestone == 2:
        return 20
    elif milestone == 3:
        return 30
    elif milestone == 4:
        return 40
    else:
        return 50

# Fall Speed per Milestones
def calculate_fall_speed(_score, milestone):
    if milestone == 1:
        return 0.2
    elif milestone == 2:
        return 0.18
    elif milestone == 3:
        return 0.12
    elif milestone == 4:
        return 0.1
    else:
        return 0.08
