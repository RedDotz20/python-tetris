import sys
import pygame

from src.components.point_system import (
    update_score, max_score, calculate_score, calculate_fall_speed,
)
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
def calculate_score(score, milestone):
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


def main(win):
    last_score = max_score()
    locked_positions = {}
    grid = create_grid(locked_positions)
    change_piece = False
    run = True
    current_piece = get_shape()
    next_pieces = [get_shape(), get_shape()]  # Get the next two pieces
    hold_piece = None
    score = 0
    pause = False
    modal_open = False
    hold_used = False
    turn_held = False

    milestone = 1  # Start at milestone 1
    last_speed_update_score = 0
    clock = pygame.time.Clock()
    level_time = 0
    fall_time = 0
    fall_speed = 0.27
    fall_speed = calculate_fall_speed(milestone)
    milestone_score = calculate_score(milestone)

    while run:
        grid = create_grid(locked_positions)

        # --------------------------------------
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick(60)

        #? INCREASING SPEED PER MULTIPLE OF 20
        #? Speed updates per 20 points && Max Fall Speed is achieved at 160
        if score // 20 > last_speed_update_score and score < 200:
            last_speed_update_score = score // 20   # Update the last speed update score
            if fall_speed > 0.05:                   # Max Fall Speed Limit: 0.05
                fall_speed -= 0.02                  # Rate of Fall Accelaration
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

        #? Update milestone, milestone score, and fall speed if necessary
        if (score >= 100) and (milestone == 1):
            milestone = 2
            milestone_score = calculate_score(milestone)
            fall_speed = calculate_fall_speed(milestone)
        elif (score >= 250) and (milestone == 2):
            milestone = 3
            milestone_score = calculate_score(milestone)
            fall_speed = calculate_fall_speed(milestone)
        elif (score >= 450) and (milestone == 3):
            milestone = 4
            milestone_score = calculate_score(milestone)
            fall_speed = calculate_fall_speed(milestone)
        elif (score >= 700) and (milestone == 4):
            milestone = 5
            milestone_score = calculate_score(milestone)
            fall_speed = calculate_fall_speed(milestone)

        # ------------------------------------------------------

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                #? Define Game Controls
                move_left = event.key in {pygame.K_LEFT, pygame.K_a}
                move_right = event.key in {pygame.K_RIGHT, pygame.K_d}
                move_down = event.key in {pygame.K_DOWN, pygame.K_s}
                rotate_piece = event.key in {pygame.K_UP, pygame.K_w}
                drop_piece = event.key in {pygame.K_SPACE}

                #? Game Settings
                is_toggle_restart =  event.key in {pygame.K_r} and modal_open


                if event.type == pygame.QUIT:
                    run = False
                    pygame.display.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pause = not pause
                        modal_open = pause
                    if move_left and not pause:
                        current_piece.x -= 1
                        if not valid_space(current_piece, grid):
                            current_piece.x += 1
                    if move_right and not pause:
                        current_piece.x += 1
                        if not valid_space(current_piece, grid):
                            current_piece.x -= 1
                    if move_down and not pause:
                        current_piece.y += 1
                        if not valid_space(current_piece, grid):
                            current_piece.y -= 1
                    if rotate_piece and not pause:
                        current_piece.rotation += 1
                        if not valid_space(current_piece, grid):
                            current_piece.rotation -= 1
                    if drop_piece and not pause:
                        while valid_space(current_piece, grid):
                            current_piece.y += 1
                        current_piece.y -= 1
                        change_piece = True
                    if is_toggle_restart:
                        main_menu(win)
                    if event.key == pygame.K_LCTRL and not (pause or hold_used or turn_held):
                        if hold_piece is None:
                            hold_piece = current_piece
                            current_piece = next_pieces.pop(0)
                            next_pieces.append(get_shape())
                            current_piece.x = 4
                            current_piece.y = 0
                        else:
                            current_piece, hold_piece = hold_piece, current_piece
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

        # ----------------------------------------------------------------

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
            score += clear_rows(grid, locked_positions) * milestone_score

        draw_window(win, grid, score, last_score, milestone, hold_piece)
        draw_window(win, grid, score, last_score, milestone, hold_shape=hold_piece)
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
                )  # Outline
            draw_text_middle(win, "YOU LOST!", 80, (175, 0, 0))
            draw_subtext_low(win,
                "Press ENTER to play again | Press ESC to quit",
                40,
                (255, 255, 255))
            run = False
            update_score(score)
            pygame.display.update()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            main_menu(win)
                        elif event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            exit()
                    elif event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

#? Initialize Program
pygame.init()

#? Set up Game Window
window = pygame.display.set_mode((S_WIDTH, S_HEIGHT))  # Window Creation
pygame.display.set_caption("PYTHON TETRIS")  # Window Title

def main_menu(win):
    is_game_running = True #? Flag variable to control the game loop
    try:
        while is_game_running:
            win.fill((0, 0, 0))
            draw_text_middle(win, "PRESS ANY KEY TO PLAY", 60, (255, 255, 255))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_game_running = False
                if event.type == pygame.KEYDOWN:
                    update_score(0)  #? reset score before starting new game
                    main(win)
            pygame.display.update()
        pygame.display.flip()
        pygame.display.quit()
    except SystemExit:
        pygame.display.quit()
        pygame.quit()
        sys.exit(0)

main_menu(window)
