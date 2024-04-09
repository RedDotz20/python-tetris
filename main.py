import random
import pygame
from src.constants import shapes, shape_colors

pygame.font.init()

# Global variables
S_WIDTH = 800
S_HEIGHT = 700
PLAY_WIDTH = 300
PLAY_HEIGHT = 600
BLOCK_SIZE = 30
TOP_LEFT_X = (S_WIDTH - PLAY_WIDTH) // 2
TOP_LEFT_Y = S_HEIGHT - PLAY_HEIGHT

class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0

def create_grid(locked_pos=None):
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]

    for i, row in enumerate(grid):
        for j, _ in enumerate(row):
            if (j, i) in locked_pos:
                c = locked_pos[(j, i)]
                grid[i][j] = c
    return grid


def convert_shape_format(shape):
    positions = []
    shape_format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(shape_format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions

def valid_space(shape, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]
    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True

def check_lost(positions):
    for pos in positions:
        _, y = pos
        if y < 1:
            return True
    return False

def get_shape():
    return Piece(5, 0, random.choice(shapes))


def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont("comicsans", size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(
        label, (
            TOP_LEFT_X + PLAY_WIDTH / 2 - (label.get_width() / 2),
            TOP_LEFT_Y + PLAY_HEIGHT / 2 - label.get_height() / 2
        )
    )

def draw_grid(surface, grid):
    sx = TOP_LEFT_X
    sy = TOP_LEFT_Y

    for i, row in enumerate(grid):
        pygame.draw.line(
            surface, (128, 128, 128),
            (sx, sy + i * BLOCK_SIZE),
            (sx + PLAY_WIDTH, sy + i * BLOCK_SIZE)
        )

        for j, _ in enumerate(row):
            pygame.draw.line(
                surface, (128, 128, 128),
                (sx + j * BLOCK_SIZE, sy),
                (sx + j * BLOCK_SIZE, sy + PLAY_HEIGHT)
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
    surface.blit(label, (sx + 10, sy - 30))


def update_score(nscore):
    score = max_score()
    with open('scores.txt', 'w', encoding="utf=8") as f:
        if int(score) > nscore:
            f.write(str(score))
        else:
            f.write(str(nscore))

def max_score():
    with open('scores.txt', 'r', encoding="utf-8") as f:
        lines = f.readlines()
        score = lines[0].strip()
    return score

def draw_window(surface, grid, score=0, last_score=0):
    surface.fill((0, 0, 0))
    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('Tetris', 1, (255, 255, 255))
    surface.blit(label, (TOP_LEFT_X + PLAY_WIDTH / 2 - (label.get_width() / 2), 30))

    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Score: ' + str(score), 1, (255, 255, 255))
    sx = TOP_LEFT_X + PLAY_WIDTH + 50
    sy = TOP_LEFT_Y + PLAY_HEIGHT / 2 - 100
    surface.blit(label, (sx + 20, sy + 160))

    label = font.render('High Score: ' + last_score, 1, (255, 255, 255))
    sx = TOP_LEFT_X - 200
    sy = TOP_LEFT_Y + 200
    surface.blit(label, (sx + 20, sy + 160))

    for i, row in enumerate(grid):
        for j, _ in enumerate(row):
            pygame.draw.rect(
                surface,
                grid[i][j],
                (TOP_LEFT_X + j * BLOCK_SIZE, TOP_LEFT_Y + i *
                BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0
            )

    pygame.draw.rect(surface, (255, 0, 0), (TOP_LEFT_X, TOP_LEFT_Y, PLAY_WIDTH, PLAY_HEIGHT), 5)
    draw_grid(surface, grid)


def draw_modal(surface):
    pygame.draw.rect(surface, (0, 0, 0), (TOP_LEFT_X + 50, TOP_LEFT_Y + 200, 200, 200))
    font = pygame.font.SysFont('comicsans', 30)
    resume_label = font.render('Resume', 1, (255, 255, 255))
    restart_label = font.render('Restart', 1, (255, 255, 255))
    surface.blit(resume_label, (TOP_LEFT_X + 100, TOP_LEFT_Y + 250))
    surface.blit(restart_label, (TOP_LEFT_X + 100, TOP_LEFT_Y + 320))

def main(win):
    last_score = max_score()
    locked_positions = {}
    grid = create_grid(locked_positions)
    change_piece = False
    run = True
    current_piece = get_shape()
    next_pieces = [get_shape(), get_shape()]  # Get the next two pieces
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    level_time = 0
    score = 0
    pause = False
    modal_open = False

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time / 1000 > 5:
            level_time = 0
            if level_time > 0.12:
                level_time -= 0.005

        if fall_time / 1000 > fall_speed:
            fall_time = 0
            if not pause:
                current_piece.y += 1
                if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                    current_piece.y -= 1
                    change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause = not pause
                    modal_open = pause
                if event.key == pygame.K_LEFT and not pause:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT and not pause:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN and not pause:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                if event.key == pygame.K_UP and not pause:
                    current_piece.rotation += 1
                    if not valid_space(current_piece, grid):
                        current_piece.rotation -= 1
                if event.key == pygame.K_SPACE and not pause:
                    while valid_space(current_piece, grid):
                        current_piece.y += 1
                    current_piece.y -= 1
                    change_piece = True
                if event.key == pygame.K_r and modal_open:
                    main_menu(win)

            if event.type == pygame.MOUSEBUTTONDOWN and modal_open:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if TOP_LEFT_X + 50 < mouse_x < TOP_LEFT_X + 250:
                    if TOP_LEFT_Y + 250 < mouse_y < TOP_LEFT_Y + 290:
                        pause = False
                        modal_open = False
                    elif TOP_LEFT_Y + 320 < mouse_y < TOP_LEFT_Y + 360:
                        main_menu(win)

        shape_pos = convert_shape_format(current_piece)

        for _, (x, y) in enumerate(shape_pos):
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_pieces.pop(0)  # Get the next piece from the list
            next_pieces.append(get_shape())  # Add a new piece to the end of the list
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10

        draw_window(win, grid, score, last_score)
        draw_next_shapes(next_pieces, win)  # Pass the list of next pieces
        if pause:
            draw_modal(win)
        pygame.display.update()

        if check_lost(locked_positions):
            draw_text_middle(win, "YOU LOST!", 80, (255, 255, 255))
            pygame.display.update()
            pygame.time.delay(1500)
            run = False
            update_score(score)

def main_menu(win):
    run = True
    while run:
        win.fill((0, 0, 0))
        draw_text_middle(win, 'Press Any Key To Play', 60, (255, 255, 255))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(win)
    pygame.display.quit()


window = pygame.display.set_mode((S_WIDTH, S_HEIGHT))
pygame.display.set_caption('PYTHON TETRIS')
main_menu(window)
