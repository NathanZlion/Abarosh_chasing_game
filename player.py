import pygame
from utils import *


class Player:
    def __init__(self, position, color, speed, game):
        self.initial_position = position or CHASER_INITIAL_POSITION
        self.position = self.initial_position
        self.color = color
        self.speed = speed
        self.direction = UP
        self.game = game

    def move(self):
        # CHECK IF THE PLAYER IS MOVING OUT OF THE SCREEN
        newPosition = (
            self.position[0] + self.speed * self.direction[0],
            self.position[1] + self.speed * self.direction[1],
        )
        if self.isInbound(newPosition) and self.canMove(newPosition):
            self.position = newPosition
    

    def isInbound(self, position):
        offset = 20
        return left_offset <= position[0] <= self.game.WIDTH - right_offset and top_offset <= position[1] <= self.game.HEIGHT - bottom_offset
    
    def canMove(self, nextPosition):
        # checks for obstacles
        for obstacle in obstacles:
            if obstacle.collidepoint(nextPosition):
                bump_sound.play()
                return False

        # checks for the screen boundaries
        return self.isInbound(nextPosition)


    def rotate(self, rotation_direction: str):
        if rotation_direction == "left":
            self.direction = LEFT_ROTATION[self.direction]

        elif rotation_direction == "right":
            self.direction = RIGHT_ROTATION[self.direction]

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.position, 10)
        # # draw an eye for it based in the direction it's facing
        if self.direction == UP:
            pygame.draw.circle(screen, GREEN, (self.position[0] - 5, self.position[1] - 5), 2)
            pygame.draw.circle(screen, GREEN, (self.position[0] + 5, self.position[1] - 5), 2)
        elif self.direction == DOWN:
            pygame.draw.circle(screen, GREEN, (self.position[0] - 5, self.position[1] + 5), 2)
            pygame.draw.circle(screen, GREEN, (self.position[0] + 5, self.position[1] + 5), 2)
        elif self.direction == LEFT:
            pygame.draw.circle(screen, GREEN, (self.position[0] - 5, self.position[1] - 5), 2)
            pygame.draw.circle(screen, GREEN, (self.position[0] - 5, self.position[1] + 5), 2)
        elif self.direction == RIGHT:
            pygame.draw.circle(screen, GREEN, (self.position[0] + 5, self.position[1] - 5), 2)
            pygame.draw.circle(screen, GREEN, (self.position[0] + 5, self.position[1] + 5), 2)
    
    def get_rect(self):
        return pygame.Rect(self.position[0] - 10, self.position[1] - 10, 20, 20)

    def reset_position(self):
        self.position = self.initial_position
        self.direction = UP
