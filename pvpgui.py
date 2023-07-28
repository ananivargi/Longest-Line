import pygame, sys
import numpy as np

pygame.init()

WIDTH = 800
HEIGHT = 800
LINE_WIDTH = 8
WIN_LINE_WIDTH = 15
ROWS = int(7)
COLS = int(7)
SQSIZE = WIDTH // COLS
CIRCLE_RADIUS = SQSIZE // 3
CIRCLE_WIDTH = 15
SPACE = 55
RED = (255, 0, 0)
BG_COLOR = (20, 160, 130)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR_PLAYER1 = (239, 231, 200)
CIRCLE_COLOR_PLAYER2 = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Longest Line Game!')
screen.fill(BG_COLOR)

board = np.zeros((ROWS, COLS))

def draw_lines():
    for row in range(ROWS):
        line_pos = row * SQSIZE
        pygame.draw.line(screen, LINE_COLOR, (0, line_pos), (WIDTH, line_pos), LINE_WIDTH)

    for col in range(COLS):
        line_pos = col * SQSIZE
        pygame.draw.line(screen, LINE_COLOR, (line_pos, 0), (line_pos, HEIGHT), LINE_WIDTH)

def draw_figures():
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == 1:
                pygame.draw.circle(screen, CIRCLE_COLOR_PLAYER1, (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2), CIRCLE_RADIUS)
            elif board[row][col] == 2:
                pygame.draw.circle(screen, CIRCLE_COLOR_PLAYER2, (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2), CIRCLE_RADIUS)
                pygame.draw.circle(screen, CIRCLE_COLOR_PLAYER2, (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2), CIRCLE_RADIUS // 2)

def mark_square(row, col, player):
    board[row][col] = player

def available_square(row, col):
    return board[row][col] == 0

def is_board_full():
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == 0:
                return False
    return True

def check_win(player):
    #Check for vertical win
        for col in range(COLS):
            for row in range(ROWS - 4):
                if board[row][col] == player and board[row+1][col] == player and board[row+2][col] == player and board[row+3][col] == player and board[row+4][col] == player:
                    draw_vertical_winning_line(row, col, player)
                    return True

    # Check for horizontal win
        for row in range(ROWS):
            for col in range(COLS - 4):
                if board[row][col] == player and board[row][col+1] == player and board[row][col+2] == player and board[row][col+3] == player and board[row][col+4] == player:
                    draw_horizontal_winning_line(row, col, player)
                    return True

    # Check for ascending diagonal win
        for row in range(4, ROWS):
            for col in range(COLS - 4):
                if board[row][col] == player and board[row-1][col+1] == player and board[row-2][col+2] == player and board[row-3][col+3] == player and board[row-4][col+4] == player:
                    draw_asc_diagonal(row, col, player)
                    return True

    # Check for descending diagonal win
        for row in range(ROWS - 4):
            for col in range(COLS - 4):
                if board[row][col] == player and board[row+1][col+1] == player and board[row+2][col+2] == player and board[row+3][col+3] == player and board[row+4][col+4] == player:
                    draw_desc_diagonal(row, col, player)
                    return True

        return False
def draw_vertical_winning_line(row, col, player):
    start_x = col * SQSIZE + SQSIZE // 2
    start_y = row * SQSIZE
    end_x = col * SQSIZE + SQSIZE // 2
    end_y = (row + 5) * SQSIZE
    pygame.draw.line(screen, RED, (start_x, start_y), (end_x, end_y), WIN_LINE_WIDTH)

def draw_horizontal_winning_line(row, col, player):
    start_x = col * SQSIZE
    start_y = row * SQSIZE + SQSIZE // 2
    end_x = (col + 5) * SQSIZE
    end_y = row * SQSIZE + SQSIZE // 2
    pygame.draw.line(screen, RED, (start_x, start_y), (end_x, end_y), WIN_LINE_WIDTH)

def draw_asc_diagonal(row, col, player):
    start_x = col * SQSIZE
    start_y = (row + 1) * SQSIZE
    end_x = (col + 5) * SQSIZE
    end_y = (row - 4) * SQSIZE
    pygame.draw.line(screen, RED, (start_x, start_y), (end_x, end_y), WIN_LINE_WIDTH)


def draw_desc_diagonal(row, col, player):
    start_x = col * SQSIZE
    start_y = row * SQSIZE
    end_x = (col + 5) * SQSIZE
    end_y = (row + 5) * SQSIZE
    pygame.draw.line(screen, RED, (start_x, start_y), (end_x, end_y), WIN_LINE_WIDTH)

def restart():
    screen.fill(BG_COLOR)
    draw_lines()
    for row in range(ROWS):
        for col in range(COLS):
            board[row][col] = 0

# Variables
player1_score = 0
player2_score = 0
player = 1
game_over = False

# Main Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if not game_over:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX = event.pos[0]  # x
                mouseY = event.pos[1]  # y

                clicked_row = int(mouseY // SQSIZE)
                clicked_col = int(mouseX // SQSIZE)

                if available_square(clicked_row, clicked_col):
                    mark_square(clicked_row, clicked_col, player)
                    if check_win(player):
                        game_over = True

                    if is_board_full() and not game_over:
                        # If the board is full and no one wins, it's a draw
                        game_over = True

                    player = player % 2 + 1

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart()
                    player = 1
                    game_over = False

    draw_lines()
    draw_figures()

    # Display the scores
    font = pygame.font.Font(None, 40)
    score_text = font.render(f"Player 1: {player1_score}  Player 2: {player2_score}", True, (255, 255, 255))
    score_rect = score_text.get_rect(topleft=(10, 10))
    screen.blit(score_text, score_rect)

    pygame.display.update()

    if game_over:
        if check_win(player % 2 + 1):
            # Display the winning message and update the scores
            winner = player % 2 + 1
            message = "Player " + str(winner) + " wins!"
            if winner == 1:
                player1_score += 1
            else:
                player2_score += 1
        else:
            message = "It's a draw!"

        # Display the winning message
        font = pygame.font.Font(None, 74)
        text = font.render(message, True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
        screen.blit(text, text_rect)
        pygame.display.update()

        pygame.time.wait(3000)  # Wait for 3 seconds before resetting the game

        restart()
        player = 1
        game_over = False
