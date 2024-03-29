import copy
import sys
import pygame
import random
import numpy as np

#from constants import *

# ---------
# CONSTANTS
# ---------

INF = 1

# --- PIXELS ---

WIDTH = 600
HEIGHT = 600

ROWS = 5
COLS = 5
SQSIZE = WIDTH // COLS

LINE_WIDTH = 15
CIRC_WIDTH = 15
CROSS_WIDTH = 20

RADIUS = SQSIZE // 4

OFFSET = 50

# --- COLORS ---

BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRC1_COLOR = (239, 231, 200)
CIRC2_COLOR = (66, 66, 66)
RED = (255, 0, 0)

# --- PYGAME SETUP ---

pygame.init()
screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
pygame.display.set_caption('Longest Line Game!')
screen.fill( BG_COLOR )

# --- CLASSES ---

class Board:

    def __init__(self):
        self.squares = np.zeros( (ROWS, COLS) )
        self.empty_sqrs = self.squares # [squares]
        self.marked_sqrs = 0
        self.lines_dict = self.set_lines_dict()

    def final_state(self, show=False):
        '''
            @return 0 if there is no win yet
            @return 1 if player 1 wins
            @return 2 if player 2 wins
        '''
        iPos = fPos= win = 0
        for line in self.lines_dict:
            tokens_dict = self.get_sqrs_by_line(line)            
            for token in tokens_dict:
                if token!=0 and tokens_dict[token]['cnt'] == ROWS:
                    (row, col) = self.lines_dict[line][0]
                    #print (f"Player: {token} has won at line: {line} starting at row: {row} ,  col: {col}")
                    win = True
                    
                    if 'C' in line: #vertical wins                        
                        iPos = (col * SQSIZE + SQSIZE // 2, 20)
                        fPos = (col * SQSIZE + SQSIZE // 2, HEIGHT - 20)                        
                    if 'R' in line: #horizontal wins
                        iPos = (20, row * SQSIZE + SQSIZE // 2)
                        fPos = (WIDTH - 20, row * SQSIZE + SQSIZE // 2)
                    if line == 'D0': #desc diagonal wins
                        iPos = (20, 20)
                        fPos = (WIDTH - 20, HEIGHT - 20)
                    if line == 'D1': #asc diagonal wins
                        iPos = (20, HEIGHT - 20)
                        fPos = (WIDTH - 20, 20) 
                    break

            if win: break
        if win:    
            if show:        
                pygame.draw.line(screen, RED, iPos, fPos, LINE_WIDTH) 
            return  token  
        else:
            return 0    
        
    
    #--Generate dict of winning lines for board
    def set_lines_dict(self):
        lines_dict = {}    
        #Loop for line keys
        line_types = ('R','C','D') #Rows, Cols, Diagonals
        for line_type in line_types:
            if line_type == 'R': #Row lines
                for row in range(ROWS):
                    line_key = line_type + str(row)
                    lines_dict[line_key] = []
                    for col in range(COLS):
                        lines_dict[line_key].append((row, col))    
            elif line_type == 'C': #Column lines
                for col in range(COLS):
                    line_key = line_type + str(col)
                    lines_dict[line_key] = []
                    for row in range(ROWS):
                        lines_dict[line_key].append((row, col))
            else:
                line_type == 'D' #Diagonals
                #Descending diagonal
                line_key = line_type + '0'
                lines_dict[line_key] = []
                for idx in range(ROWS):
                    lines_dict[line_key].append((idx, idx))
                
                #Ascending diagonal
                line_key = line_type + '1'
                lines_dict[line_key] = []
                for idx in range(ROWS):
                    lines_dict[line_key].append((COLS-1-idx, idx))    
        return lines_dict
        
    
    #--Get the count of each player(token) for each winning line so we can check if there is a win (or loss) NOW or in 1 move
    def get_sqrs_by_line(self, line):
        tokens_dict = {}
        for sqr in (self.lines_dict[line]):
            token =  self.squares[sqr]
            if token in tokens_dict:
                token_cnt = tokens_dict[token]['cnt'] + 1                
            else:
                tokens_dict[token] = {}
                tokens_dict[token]['sqrs']=[]
                token_cnt = 1    
               
            tokens_dict[token]['cnt'] = token_cnt
            #if (token==0 and  token_cnt>1) : break #If there's >1 empty sqr in this line, there is no immediate win/loss for the line
            tokens_dict[token]['sqrs'].append(sqr)
        return tokens_dict
                
    #Loop through the lines and check if there's a win in 1 move for ANY player
    def get_winning_sqr(self):
        winning_token = None
        winner_sqr = ()
        for line in self.lines_dict:
            tokens_dict = self.get_sqrs_by_line(line)
            if 0 in tokens_dict and tokens_dict[0]['cnt']==1: #There is only 1 empty square in this line
                winner_sqr = tokens_dict[0]['sqrs'][0] #the blank square in a winning line
                if 1 in tokens_dict and tokens_dict[1]['cnt']==ROWS-1:
                    winning_token = 1                    
                elif 2 in tokens_dict and tokens_dict[2]['cnt']==ROWS-1 :
                    winning_token = 2
                break        
        return winning_token, winner_sqr       

     #Loop through the lines and check if there's a win in 1 move for chosen player
    def get_winning_sqr_for_player(self, player):
        winner_sqr = ()
        for line in self.lines_dict:
            tokens_dict = self.get_sqrs_by_line(line)
            if ((0 in tokens_dict and tokens_dict[0]['cnt']==1) and (player in tokens_dict and tokens_dict[player]['cnt']==ROWS-1 )): 
                winner_sqr = tokens_dict[0]['sqrs'][0] #the blank square in a winning line
                break        
        return winner_sqr
            

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
        return self.marked_sqrs == ROWS * COLS

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

    def minimax(self, board, maximizing):
        
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
                eval = self.minimax(temp_board, False)[0]
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
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move

    # --- MINIMAX Alpha Beta Pruning ---

    def minimax_alpha_beta(self, depth, board, alpha, beta, maximizing):
        
        #print (board.squares, "\n at ", depth)

        potential_eval = (ROWS*COLS-depth)
        # terminal case
        case = board.final_state()

        # player 1 wins
        if case == 1:
            return 1 * potential_eval, None # eval, move

        # player 2 wins
        if case == 2:
            return -1 * potential_eval, None

        # draw
        elif board.isfull():
            return 0, None

        if maximizing:
            max_eval = -1 * potential_eval
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                eval = self.minimax_alpha_beta(depth+1, temp_board, alpha, beta, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)
                alpha = max(alpha, max_eval)    
                if beta <= alpha:
                    break     
            return max_eval, best_move

        elif not maximizing:
            min_eval = 1 * potential_eval
            best_move = None
            
            empty_sqrs = board.get_empty_sqrs()
            
            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                eval = self.minimax_alpha_beta(depth+1, temp_board, alpha, beta,True)[0]
                
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)
                beta = min(beta, min_eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    # --- MAIN EVAL ---

    def eval(self, main_board):
        if self.level == 0:
            move = main_board.get_winning_sqr_for_player(2)
            if move: #Check if win for AI in 1
                eval = 1
            else:
                move = main_board.get_winning_sqr_for_player(1)   
                if move: #Check if loss for AI in 1
                    eval = 0 #Avoid loss and at least try for a draw if not a win
                else:    
                    # random choice
                    eval = 'random'
                    move = self.rnd(main_board)
        else:
            # minimax algo choice
            #eval, move = self.minimax(main_board, False)

            #minimax with alpha-beta pruning
            alpha = ROWS*COLS*-1
            beta = ROWS*COLS
            eval, move = self.minimax_alpha_beta(0, main_board, alpha, beta, False)
            
        print(f'AI has chosen to mark the square in pos {move} with an eval of: {eval}')

        return move # row, col
class Game:

    def __init__(self):
        self.board = Board()
        #self.ai = AI()
        self.ai = AI(0)#Init AI to level 0 ( 0 = partial AI, 1 = full AI (default))
        self.player = 1   #1-cross  #2-circles
        self.gamemode = 'ai' # pvp or ai
        self.running = True
        self.show_lines()

    # --- DRAW METHODS ---

    def show_lines(self):
        # bg
        screen.fill( BG_COLOR )

        # Draw vertical lines
        for col in range(1, COLS):
            x = col * SQSIZE
            pygame.draw.line(screen, LINE_COLOR, (x, 0), (x, HEIGHT), LINE_WIDTH)

        # Draw horizontal lines
        for row in range(1, ROWS):
            y = row * SQSIZE
            pygame.draw.line(screen, LINE_COLOR, (0, y), (WIDTH, y), LINE_WIDTH)

    def draw_fig(self, row, col):
        if self.player == 1:
            pygame.draw.circle(screen, CIRC1_COLOR, (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2), RADIUS)
        
        elif self.player == 2:
            # draw circle
            pygame.draw.circle(screen, CIRC2_COLOR, (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2), RADIUS)

    # --- OTHER METHODS ---

    def make_move(self, row, col):
        self.board.mark_sqr(row, col, self.player)
        self.draw_fig(row, col)
        self.next_turn()

    def next_turn(self):
        self.player = self.player % 2 + 1

    def change_gamemode(self):
        self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'

    def isover(self):
        return self.board.final_state(show=True) != 0 or self.board.isfull()

    def reset(self):
        self.__init__()

def main():

    # --- OBJECTS ---

    game = Game()
    board = game.board
    ai = game.ai

    # --- MAINLOOP ---

    while True:
        
        # pygame events
        for event in pygame.event.get():

            # quit event
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # keydown event
            if event.type == pygame.KEYDOWN:

                # g-gamemode
                if event.key == pygame.K_g:
                    game.change_gamemode()

                # r-restart
                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai

                # 0-random ai
                if event.key == pygame.K_0:
                    ai.level = 0
                
                # 1-random ai
                if event.key == pygame.K_1:
                    ai.level = 1

            # click event
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
        if game.gamemode == 'ai' and game.player == ai.player and game.running:

            # update the screen
            pygame.display.update()

            # eval
            row, col = ai.eval(board)
            game.make_move(row, col)

            if game.isover():
                game.running = False
            
        pygame.display.update()

main()
   
   
   