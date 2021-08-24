###########################################################################
# This File is the pygame implementation of snakes game made by me.       #
# Run this script along with "hand_direction_control.py" file and         #
#  select the game tab and enjoy playing. You can also run this script    #
# without the other script and enjoy playing with the keyboard.           #
###########################################################################
# Pygame implementation of snakes games

#### Imports ####
import pygame
import random
from enum import Enum
from collections import namedtuple

Point = namedtuple('Point', 'x, y')


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


#### Some Parameters which can be changed to customize the game ####
WHITE = (255, 255, 255)
RED = (239, 48, 56)  # Carmine Red
BLUE1 = (0, 0, 255)
BLUE2 = (0, 255, 255)  # Cyan
BLACK = (0, 0, 0)
GREEN = (124, 252, 0)  # Lawn Green
BLOCK_SIZE = 20
INNER_BLOCK_SIZE = 8
SPEED = 5  # slow right now to help user adapt the changing hand direction quickly
WIDTH = 640
HEIGHT = 480
pygame.init()


class SnakeGame:
    def __init__(self, w=WIDTH, h=HEIGHT):
        self.w = w
        self.h = h

        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snakes Game')
        self.clock = pygame.time.Clock()

        self.direction = Direction.RIGHT  # initial direction

        # Declaring the head block and also initialising a 3 block snake
        self.head = Point(self.w // 2, self.h // 2)
        self.snake = [self.head, Point(self.head.x - BLOCK_SIZE, self.head.y),
                      Point(self.head.x - (2 * BLOCK_SIZE), self.head.y)]

        self.score = 0
        self.apple = None
        self._place_food()  # Randomly placing the food in the game space

    #### Randomly generates new position for apple to be placed ####
    def _place_food(self):
        x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.apple = Point(x, y)
        if self.apple in self.snake:
            self._place_food()

    #### Main Game Control --> Calls all helper functions in order ####
    def play(self):
        #### event Checker Loop ####
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN

        self._move(self.direction)
        self.snake.insert(0, self.head)

        game_over = False
        if self._collision():
            game_over = True
            return game_over, self.score

        if self.head == self.apple:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()

        self._update_screen()
        self.clock.tick(SPEED)
        return game_over, self.score

    #### Update the pygame Window each frame ####
    def _update_screen(self):
        self.display.fill(GREEN)

        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x + (BLOCK_SIZE-INNER_BLOCK_SIZE)//2,
                                                              pt.y + (BLOCK_SIZE-INNER_BLOCK_SIZE)//2,
                                                              INNER_BLOCK_SIZE, INNER_BLOCK_SIZE))


        pygame.draw.rect(self.display, RED, pygame.Rect(self.apple.x, self.apple.y, BLOCK_SIZE, BLOCK_SIZE))

        pygame.display.flip()

    #### Motion of the Snake ####
    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)

    #### Collision Cases ####
    def _collision(self):
        #### hits boundary ####
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
            return True
        #### its itself ####
        if self.head in self.snake[1:]:
            return True

        return False


if __name__ == "__main__":
    game = SnakeGame()

    #### Game Loop ####
    while True:
        game_over, score = game.play()

        if game_over:
            break
    print("Final Score ", score)  # printing on terminal...can also be printed on screen (Will work on it)
    pygame.quit()
