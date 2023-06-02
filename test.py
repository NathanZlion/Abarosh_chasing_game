


import pygame
from pygame.locals import *



SCREEN = pygame.display.set_mode(800, 800)

rectangle = pygame.draw.rect(SCREEN, (0,0,0), (0,0,1,1))

# q: Here out my Idea and suggest me how to do this
# 

# The idea for this game is to build a python game that simulates the traditional Ethiopian abarosh game.
# The rule of the game is simple:
# - Don't get caught by the person chasing you.

# How the game works:-
# - Say player 1 is the chaser and player 2 is the one  being chased.
# - The goal of player one is to chase and catch player 2.
# - on the other hand the goal of player 2 is to reach his goal with out being caught by player 1.

# To spice things up we have added some features.
# - There will be 4 corners where player 2 can enter but not player 2.
# - One is the place where player 1 will be when the game starts, the opposite corner -- the finish corner is the target player 1 should reach in order to win the game.
# - All 4 corners are places (safe zones) where player 1 can enter to avoid being caught by player 2.
# - Player 2 will have to try to catch player 1 before he enters these safe zones, and defenately before he enters one of the 4 corners -- the finish corner


# ## Controls:
# - One player will have to use the `WAD`
#     - `W` => forward
#     - `A` => rotate left by some degree in a continuous manner
#     - `D` => rotate right by some degree in a continuous manner

# - Second player will use the same logic to navigate the field with keys `UP LEFT RIGHT` respectively.


# # TIP
# - In order to make the game interesting, we had to make the players (chaser, and chased) have different attributes.
# - Chaser can move fast but can't rotate fast.
# - Chased player can rotate (change directions) faster than the chaser, Meaning the chased have to use techinques like drifting to get the chaser off his tail.

## Have a Nice Time.
