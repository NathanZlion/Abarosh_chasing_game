from utils import *
from player import Player


class Chaser(Player):
    def __init__(self, game, color, speed):
        self.game = game
        super().__init__(color=color, speed=speed, game=game, position=CHASER_INITIAL_POSITION)
        self.pic = char2_left
        self.direction = LEFT

    def move(self, direction):
        self.direction = direction

        if self.direction == LEFT:
            self.pic = char2_left
        elif self.direction == RIGHT:
            self.pic = char2_right
        elif self.direction == UP:
            self.pic = char2_up
        elif self.direction == DOWN:
            self.pic = char2_down

        nextPosition = (
            self.position[0] + self.speed * self.direction[0],
            self.position[1] + self.speed * self.direction[1],
        )

        # CHECK IF THE PLAYER IS MOVING OUT OF THE SCREEN and also it he's moving into safe zones
        if self.canMove(nextPosition) and super().isInbound(nextPosition):
            self.position = nextPosition

    def canMove(self, nextPosition):
        if not super().canMove(nextPosition):
            return False

        for safe_zone in safe_zones:
            if safe_zone.collidepoint(nextPosition):
                pygame.mixer.Sound.play(barrel_collision_sound)
                return False

        return True

    def isInbound(self, position):
        return (0 <= position[0] <= self.game.WIDTH and 0 <= position[1] <= self.game.HEIGHT)
