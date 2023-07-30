# Longest Line
Software Design and Development Assessment Task 2
** Description
This project is a game whose objective is to make the longest line possible on a 5 x 5 dotted  grid

## ASCII Rules
The objective of the game is to create the longest line possible in a dotted grid by connecting two at a time, whilst also blocking the other player from developing their line. 
Players can only connect two dots in a turn
They must continue their line in their subsequent turns (ie each line has to be sharing a dot with another line)
They can only continue the line from the end they developed in their previous move (ie the line will grow in one direction)
A player’s line can’t touch the same dot as the other player
If there are no possible moves for even one player, the game ends and the length of the lines is calculated (ie you might have blocked the other person from making any move but still lose because your line is shorter)

## PVP GUI rules
The game is played on a grid of size 7x7.

Two players take turns marking a square on the grid. Player 1 uses white circles, and Player 2 uses black circles.

The objective of the game is to form the longest line (vertical, horizontal, or diagonal) of your own circles on the board.

The game ends when one of the players forms a line of 5 circles in a row (horizontally, vertically, or diagonally).

If all squares on the board are filled and no player has formed a line of 5, the game ends in a draw.

How the Game Works:
The game starts with an empty 7x7 grid.

Player 1 (white circles) goes first.

Players take turns by clicking on an empty square on the grid to place their circle in that position.

The game checks after each move if any player has formed a line of 5 circles in a row. If a line of 5 is formed, the game ends, and the player who formed the line wins.

If the entire board is filled with circles, and no line of 5 is formed, the game ends in a draw.

When the game is over, the winning player is displayed on the screen. If it's a draw, the game will display a draw message.

After the game ends, the scores of both players (number of wins) are displayed at the top of the screen.

To restart the game, press the "r" key on the keyboard. The scores will be reset to 0, and the game will start again.

How to Play:
Run the Python script, and a window will appear displaying the game grid.

Player 1 (white circles) starts the game.

Click on an empty square on the grid to place a circle in that position.

Take turns with the other player until one player forms a line of 5 circles or the board is full.

If a line of 5 circles is formed, the winning player will be displayed on the screen.

To start a new game, press the "r" key on the keyboard.


## MinimaxAIgame/ AlphaBetaPruning
PLEASE NOTE: These are two notebooks which are essentially the same however the alpha beta pruning notebook is just a record of my attempt of using alpha beta pruning to reduce the time it takes for the minimax function however, unless you want to wait an hour or use a super computer, the hard ai (ie the ai using the minimax) will not produce an output and the window will glitch and say 'not responding' 
In minimax, the win condition was set to three in a row (just to make it simpler to visualise how the program was running.)
The game starts with an empty 4x4 grid.

Player 1  goes first.
Press g to toggle between PVP and AI, and press 0 for the 'Easy AI'. The hard AI will not work due to the sheer number of combinations the minimax function goes through which, therefore takes extremely long amounts of time. 

Players take turns by clicking on an empty square on the grid to place their symbol in that position.

The game checks after each move if any player has formed a line of 4 symbols in a row. If a line of 4 is formed, the game ends, and the player who formed the line wins.

If the entire board is filled with symbols, and no line of 4 is formed, the game ends in a draw.

If the game mode is set to 'ai' and it is Player 2's turn, the AI will automatically make its move. The AI's level of intelligence can be changed using the keyboard during the game.

When the game is over, the winning player is displayed on the screen. If it's a draw, the game will display a draw message.

To restart the game, press the "r" key on the keyboard. The game will reset with Player 1  starting the game again.

## AIANDPVP
The game starts with an empty 4x4 grid.

Player 1  goes first.
Press g to toggle between PVP and AI, and press 1 for the 'Hard AI'. The hard AI will not work due to the sheer number of combinations the minimax function goes through which, therefore takes extremely long amounts of time. 

Players take turns by clicking on an empty square on the grid to place their symbol in that position.

The game checks after each move if any player has formed a line of 4 symbols in a row. If a line of 4 is formed, the game ends, and the player who formed the line wins.

If the entire board is filled with symbols, and no line of 4 is formed, the game ends in a draw.

If the game mode is set to 'ai' and it is Player 2's turn, the AI will automatically make its move. The AI's level of intelligence can be changed using the keyboard during the game.

When the game is over, the winning player is displayed on the screen. If it's a draw, the game will display a draw message.

To restart the game, press the "r" key on the keyboard. The game will reset with Player 1  starting the game again.

## Homepage
The homepage code works the same as the 'AIANDPVP' however it has a homepage that allows the user to visualise their options and simply click on one. 

## Finalguiversion
The final version is, ultimately, the end project. This version contains the AI that chooses its moves based on whether there is a win/loss in one and if there isn't, it will pick a random move. Furthermore, I have made this code so that nothing is hard-coded and, essentialy, you can choose any grid size you would like to play the game on and it will work. This involved changing the win function, the drawing the winning line fnuction, and using loops to created the dictionary with the possible lines. It still has the minimax and alpha-beta pruning however that will not work, as mentioned above. 


