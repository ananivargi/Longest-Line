#Please Note: This was my attempt at using the minimax function to develop an AI for the game. The 4 x 4 grid had too big a number of permutations to run on a normal computer. This code will work on a super computer however I don't have access to one and am therefore, unable to run the project at any decent speed. 

import copy
import sys
import pygame
import random
import numpy as np
# ---------
# CONSTANTS
# ---------

# --- PIXELS ---

WIDTH = 800
HEIGHT = 800

ROWS = 7
COLS = 7
SQSIZE = WIDTH // COLS

LINE_WIDTH = 15
CIRC_WIDTH = 15
CIRCLE_RADIUS = SQSIZE // 3

WIN_LINE_WIDTH = 15
RADIUS = SQSIZE // 4

OFFSET = 50

# --- COLORS ---
RED = (255, 0, 0)
BG_COLOUR = (28, 170, 156)
LINE_COLOUR = (23, 145, 135)
CIRCLE1_COLOUR = (239, 231, 200)
CIRCLE2_COLOUR = (0, 0, 0)

# --- PYGAME SETUP ---

pygame.init()
screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
pygame.display.set_caption('Longest Line Game')
screen.fill( BG_COLOUR )

# --- CLASSES ---

class Board:

    def __init__(self):
        self.squares = np.zeros( (ROWS, COLS) )
        self.empty_sqrs = np.copy(self.squares) # [squares]
        self.marked_sqrs = 0

    def final_state(self, show=False):
        '''
            @return 0 if there is no win yet
            @return 1 if player 1 wins
            @return 2 if player 2 wins
        '''

        # vertical wins
    def final_state(self, show=False):

    # vertical wins
        for col in range(COLS):
            for row in range(ROWS - 5):  # Change from -4 to -5
                if self.squares[row][col] == self.squares[row + 1][col] == self.squares[row + 2][col] == self.squares[row + 3][col] == self.squares[row + 4][col] != 0:
                        start_x = col * SQSIZE + SQSIZE // 2
                        start_y = row * SQSIZE
                        end_x = col * SQSIZE + SQSIZE // 2
                        end_y = (row + ROWS) * SQSIZE
                        pygame.draw.line(screen, RED, (start_x, start_y), (end_x, end_y), WIN_LINE_WIDTH)
                        return self.squares[row][col]

    # Check for horizontal win
        for row in range(ROWS):
            for col in range(COLS - 5):  # Change from -4 to -5
                if self.squares[row][col] == self.squares[row][col + 1] == self.squares[row][col + 2] == self.squares[row][col + 3] == self.squares[row][col + 4] != 0:
                       start_x = col * SQSIZE
                       start_y = row * SQSIZE + SQSIZE // 2
                       end_x = (col + ROWS) * SQSIZE
                       end_y = row * SQSIZE + SQSIZE // 2
                       pygame.draw.line(screen, RED, (start_x, start_y), (end_x, end_y), WIN_LINE_WIDTH)
                       return self.squares[row][col]

    # Check for ascending diagonal win
        for row in range(5, ROWS):  # Change from 4 to 5
            for col in range(COLS - 5):  # Change from -4 to -5
                if self.squares[row][col] == self.squares[row - 1][col + 1] == self.squares[row - 2][col + 2] == self.squares[row - 3][col + 3] == self.squares[row - 4][col + 4] != 0:
                        start_x = col * SQSIZE
                        start_y = (row + 1) * SQSIZE
                        end_x = (col + 5) * SQSIZE
                        end_y = (row - 4) * SQSIZE
                        pygame.draw.line(screen, RED, (start_x, start_y), (end_x, end_y), WIN_LINE_WIDTH)  
                        return self.squares[row][col]

    # Check for descending diagonal win
        for row in range(ROWS - 5):  # Change from -4 to -5
            for col in range(COLS - 5):  # Change from -4 to -5
                if self.squares[row][col] == self.squares[row + 1][col + 1] == self.squares[row + 2][col + 2] == self.squares[row + 3][col + 3] == self.squares[row + 4][col + 4] != 0:
                        start_x = col * SQSIZE
                        start_y = row * SQSIZE
                        end_x = (col + 5) * SQSIZE
                        end_y = (row + 5) * SQSIZE
                        pygame.draw.line(screen, RED, (start_x, start_y), (end_x, end_y), WIN_LINE_WIDTH)  
                        return self.squares[row][col]

        return 0
    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1

    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0

    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(ROWS):
            for col in range(COLS): 
                if self.empty_sqr(row, col):
                    empty_sqrs.append( (row, col) )
        
        return empty_sqrs

    def isfull(self):
        return self.marked_sqrs == 49

    def isempty(self):
        return self.marked_sqrs == 0

class AI:

    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player

    # --- RANDOM ---

    def rnd(self, board):
        empty_sqrs = board.get_empty_sqrs()
        idx = random.randrange(0, len(empty_sqrs))

        return empty_sqrs[idx] # (row, col)

    # --- MINIMAX ---

    def minimax(self, board, maximizing, depth):
        depth += 1 
        print ("depth is:" + str(depth))
        print (board.squares)
        # terminal case
        case = board.final_state()

        # player 1 wins
        if case == 1:
            return 1, None # eval, move

        # player 2 wins
        if case == 2:
            return -1, None

        # draw
        elif board.isfull():
            return 0, None


        if maximizing:
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()
            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                #print ("max_eval = " + str(max_eval))
                #print (best_move)
                eval = self.minimax(temp_board, False, depth)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)
                    
            return max_eval, best_move

        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                eval = self.minimax(temp_board, True, depth)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move

    # --- MAIN EVAL ---

    def eval(self, main_board):
        if self.level == 0:
            # random choice
            eval = 'random'
            move = self.rnd(main_board)
        else:
            # minimax algo choice
            eval, move = self.minimax(main_board, False, 0)
            #print ("hello")

        print(f'AI has chosen to mark the square in pos {move} with an eval of: {eval}')

        return move # row, col

class Game:

    def __init__(self ):
        self.board = Board()
        self.ai = AI(level=2)
        self.player = 1
        self.gamemode = 'ai'
        self.running = False
    
    def reset(self):
        self.__init__()

    def set_gamemode(self, gamemode):
        self.gamemode = gamemode
        self.running = True

    # --- DRAW METHODS ---
    

    def show_lines(self):
    # Calculate square size based on the number of rows and columns
        SQSIZE = min(HEIGHT // ROWS, WIDTH // COLS)

        # bg
        screen.fill(BG_COLOUR)

        # Draw vertical lines
        for col in range(1, COLS):
            x = col * SQSIZE
            pygame.draw.line(screen, LINE_COLOUR, (x, 0), (x, HEIGHT), LINE_WIDTH)

        # Draw horizontal lines
        for row in range(1, ROWS):
            y = row * SQSIZE
            pygame.draw.line(screen, LINE_COLOUR, (0, y), (WIDTH, y), LINE_WIDTH)


    def draw_fig(self, row, col):
        if self.player == 1:
            pygame.draw.circle(screen, CIRCLE1_COLOUR, (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2), CIRCLE_RADIUS)
        
        elif self.player == 2:
            # draw circle
            pygame.draw.circle(screen, CIRCLE2_COLOUR, (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2), CIRCLE_RADIUS)

    # --- OTHER METHODS ---

    def make_move(self, row, col):
        self.board.mark_sqr(row, col, self.player)
        self.draw_fig(row, col)
        self.next_turn()
        pygame.display.update()
        
    def next_turn(self):
        self.player = self.player % 2 + 1

    def change_gamemode(self):
        self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'

    def isover(self):
        return self.board.final_state(show=True) != 0 or self.board.isfull()

    def reset(self):
        self.__init__()

def homepage():
    screen.fill(BG_COLOUR)
    font = pygame.font.Font(None, 50)
    text_pvp = font.render("PvP", True, (255, 255, 255))
    text_easy_ai = font.render("Easy AI", True, (255, 255, 255))
    text_hard_ai = font.render("Hard AI", True, (255, 255, 255))
    screen.blit(text_pvp, (WIDTH // 2 - text_pvp.get_width() // 2, HEIGHT // 2 - 100))
    screen.blit(text_easy_ai, (WIDTH // 2 - text_easy_ai.get_width() // 2, HEIGHT // 2))
    screen.blit(text_hard_ai, (WIDTH // 2 - text_hard_ai.get_width() // 2, HEIGHT // 2 + 100))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if WIDTH // 2 - 100 <= pos[0] <= WIDTH // 2 + 100:
                    if HEIGHT // 2 - 120 <= pos[1] <= HEIGHT // 2 - 80:
                        return 'pvp'
                    elif HEIGHT // 2 - 20 <= pos[1] <= HEIGHT // 2 + 20:
                        return 'easy_ai'
                    elif HEIGHT // 2 + 80 <= pos[1] <= HEIGHT // 2 + 120:
                        return 'hard_ai'



def main():
    # --- OBJECTS ---
    game = Game()
    board = game.board
    ai = game.ai

    # --- HOMEPAGE ---
    gamemode = homepage()
    if gamemode == 'easy_ai':
        ai.level = 0
    elif gamemode == 'hard_ai':
        ai.level = 1
        
    game.set_gamemode(gamemode)
    screen.fill(BG_COLOUR)
    game.show_lines()
    #board = game.board
    #pygame.display.update()

    # --- MAINLOOP ---
    while True:
        # pygame events
        for event in pygame.event.get():
            # quit event
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai
                
            pygame.display.update()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQSIZE
                col = pos[0] // SQSIZE
                # human mark sqr
                if board.empty_sqr(row, col) and game.running:
                    game.make_move(row, col)
                    if game.isover():
                        game.running = False
        # AI initial call
        if gamemode == 'easy_ai' and game.player == ai.player and game.running:
            # update the screen
            pygame.display.update()
            # eval
            row, col = ai.eval(board)
            print(row, col)
            game.make_move(row, col)
            if game.isover():
                game.running = False
        elif gamemode == 'hard_ai' and game.player == ai.player and game.running:
            # update the screen
            pygame.display.update()
            # eval
            row, col = ai.eval(board)
            print(row, col)
            game.make_move(row, col)
            if game.isover():
                game.running = False
        pygame.display.update()

main()