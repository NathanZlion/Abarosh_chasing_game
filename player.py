import pygame
from utils import *


class Player:
    def __init__(self, position, color, speed, game):
        self.initial_position = position or CHASER_INITIAL_POSITION
        self.position = self.initial_position
        self.color = color
        self.speed = speed
        self.game = game

        self.direction = DOWN
        self.pic = char1_down

    def move(self, direction):
        self.direction = direction

        if self.direction == LEFT:
            self.pic = char1_left
        elif self.direction == RIGHT:
            self.pic = char1_right
        elif self.direction == UP:
            self.pic = char1_up
        elif self.direction == DOWN:
            self.pic = char1_down

        # CHECK IF THE PLAYER IS MOVING OUT OF THE SCREEN
        newPosition = (self.position[0] + self.speed * self.direction[0],self.position[1] + self.speed * self.direction[1],)
        if self.isInbound(newPosition) and self.canMove(newPosition):
            self.position = newPosition
    

    def isInbound(self, position):
        return left_offset <= position[0] <= self.game.WIDTH - right_offset and top_offset <= position[1] <= self.game.HEIGHT - bottom_offset
    
    def canMove(self, nextPosition):
        # checks for obstacles
        for obstacle in obstacles:
            if obstacle.collidepoint(nextPosition):
                bump_sound.play()
                return False

        # checks for the screen boundaries
        return self.isInbound(nextPosition)


    def draw(self, screen):
        # Draw the arrow body
        arrow_body_start = (self.position[0] + self.direction[0] * 10, self.position[1] + self.direction[1] * 10)
        arrow_body_end = (self.position[0] + self.direction[0] * 50, self.position[1] + self.direction[1] * 50)
        pygame.draw.line(screen, self.color, arrow_body_start, arrow_body_end, 2)

        arrowhead_point1 = (0,0)
        arrowhead_point2 = (0,0)

        # Define the arrowhead points based on the direction
        if self.direction == UP:
            arrowhead_point1 = (arrow_body_end[0] - 5, arrow_body_end[1] + 10)
            arrowhead_point2 = (arrow_body_end[0] + 5, arrow_body_end[1] + 10)
        elif self.direction == DOWN:
            arrowhead_point1 = (arrow_body_end[0] - 5, arrow_body_end[1] - 10)
            arrowhead_point2 = (arrow_body_end[0] + 5, arrow_body_end[1] - 10)
        elif self.direction == LEFT:
            arrowhead_point1 = (arrow_body_end[0] + 10, arrow_body_end[1] - 5)
            arrowhead_point2 = (arrow_body_end[0] + 10, arrow_body_end[1] + 5)
        elif self.direction == RIGHT:
            arrowhead_point1 = (arrow_body_end[0] - 10, arrow_body_end[1] - 5)
            arrowhead_point2 = (arrow_body_end[0] - 10, arrow_body_end[1] + 5)

        # Draw the arrowhead triangle
        pygame.draw.polygon(screen, self.color, [arrow_body_end, arrowhead_point1, arrowhead_point2])

        screen.blit(self.pic, (self.position[0] - 10, self.position[1] - 10))
        
    def get_rect(self):
        return pygame.Rect(self.position[0] - 10, self.position[1] - 10, 20, 20)

    def reset_position(self):
        self.position = self.initial_position
        self.direction = UP
