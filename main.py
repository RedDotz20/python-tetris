# import random
import pygame

from src.components.scores import update_score, max_score
from src.components.game_functions import (
    draw_text_middle,
    draw_subtext_low,
    create_grid,
    valid_space,
    convert_shape_format,
    clear_rows,
    draw_window,
    draw_next_shapes,
    draw_modal,
    check_lost,
)
from src.components.shapes import(get_shape)
from src.constants.global_variables import (
    S_WIDTH,
    S_HEIGHT,
    TOP_LEFT_X,
    TOP_LEFT_Y,
)

def main_menu(win):
    run = True
    while run:
        win.fill((0, 0, 0))
        draw_text_middle(win, "PRESS ANY KEY TO PLAY", 60, (255, 255, 255))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                update_score(0)  # reset score before starting new game
                main(win)
    pygame.display.quit()

def main(win):
    last_score = max_score()
    locked_positions = {}
    grid = create_grid(locked_positions)
    change_piece = False
    run = True
    current_piece = get_shape()
    next_pieces = [get_shape(), get_shape()]  # Get the next two pieces
    hold_piece = None
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    level_time = 0
    score = 0
    pause = False
    modal_open = False
    last_speed_update_score = 0
    hold_used = False
    turn_held = False

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick(60)

        # INCREASING SPEED PER MULTIPLE OF 20
        # Speed updates per 20 points && Max Fall Speed is achieved at 160
        if score // 20 > last_speed_update_score and score < 200:
            last_speed_update_score = score // 20  # Update the last speed update score
            if fall_speed > 0.05:  # Max Fall Speed Limit: 0.05
                fall_speed -= 0.02  # Rate of Fall Accelaration

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
                if event.key == pygame.K_LEFT or event.key == pygame.K_a and not pause:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d and not pause:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN or event.key == pygame.K_s and not pause:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                if event.key == pygame.K_UP or event.key == pygame.K_w and not pause:
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

                if event.key == pygame.K_LCTRL and not pause and not hold_used and not turn_held:
                    if hold_piece is None:
                        hold_piece = current_piece
                        current_piece = next_pieces.pop(0)
                        next_pieces.append(get_shape())
                        current_piece.x = 4
                        current_piece.y = 0
                    else:
                        temp_piece = current_piece
                        current_piece = hold_piece
                        hold_piece = temp_piece
                        current_piece.x = 4
                        current_piece.y = 0
                        turn_held = True
                        hold_used = True
                if event.key == pygame.K_LSHIFT and not pause and not turn_held:
                    if not hold_piece:
                        hold_piece = current_piece
                        current_piece = next_pieces.pop(0)
                        next_pieces.append(get_shape())
                    else:
                        temp_piece = hold_piece
                        hold_piece = current_piece
                        hold_piece.x = 6
                        hold_piece.y = 2
                        current_piece = temp_piece
                        current_piece.x = 6
                        current_piece.y = 2
                        if not valid_space(current_piece, grid):
                            run = False
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
            turn_held = False  # Reset the turn-held flag
            hold_used = False
            score += clear_rows(grid, locked_positions) * 10

        draw_window(win, grid, score, last_score)
        # draw_shadow(win, grid, current_piece)  # Draw the shadow
        draw_next_shapes(next_pieces, win)  # Pass the list of next pieces
        if pause:
            draw_modal(win)
        pygame.display.update()

        if check_lost(locked_positions):
            pygame.draw.rect(win, (0, 0, 0), pygame.Rect(0, 0, S_WIDTH, S_HEIGHT))
            pygame.draw.rect(win, (0, 0, 0), (TOP_LEFT_X + 50, TOP_LEFT_Y + 200, 200, 200))
            pygame.draw.rect(win,
                (255, 255, 255),
                (TOP_LEFT_X + 50, TOP_LEFT_Y + 200, 200, 200),
                3
            ) # Outline
            draw_text_middle(win, "YOU LOST!", 80, (175, 0, 0))
            draw_subtext_low(win,
                "Press ENTER to play again | Press ESC to quit",
                40,
                (255, 255, 255)
            )
            run = False
            update_score(score)
            pygame.display.update()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN :
                            main_menu(win)
                        elif event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            exit()
                    elif event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
window = pygame.display.set_mode((S_WIDTH, S_HEIGHT)) # Window Creation
pygame.display.set_caption("PYTHON TETRIS") # Window Title
main_menu(window) # Window Opening
