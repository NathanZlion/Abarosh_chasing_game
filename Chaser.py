from utils import *
from player import Player


class Chaser(Player):
    def __init__(self, game, color, speed):
        self.game = game
        super().__init__( color = color,speed =  speed, game = game, position = CHASER_INITIAL_POSITION)
        pass

    def move(self):
        # CHECK IF THE PLAYER IS MOVING OUT OF THE SCREEN and also it he's moving into safe zones
        nextPosition = (
            self.position[0] + self.speed * self.direction[0],
            self.position[1] + self.speed * self.direction[1],
        )

        if self.canMove(nextPosition) and self.isInbound(nextPosition):
            self.position = nextPosition

    def canMove(self, nextPosition):
        # if the super() canMove() returns false, then the player is trying to move into an obstacle
        if not super().canMove(nextPosition):
            return False

        for safe_zone in self.game.safe_zones:
            if safe_zone.collidepoint(nextPosition):
                return False
        return True

    def isInbound(self, position):
        return (
            0 <= position[0] <= self.game.WIDTH and 0 <= position[1] <= self.game.HEIGHT
        )
