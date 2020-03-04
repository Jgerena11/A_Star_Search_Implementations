import pygame
import random
from shapely.geometry import LinearRing, LineString, Point, Polygon
import heapq
import re

pygame.init()
X = 1000
Y = 700
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
size = (X, Y)
screen = pygame.display.set_mode(size)

class Environment:
    square_list = []
    blocked_squares = []

    class Square:
        vertices = []
        num = 0
        active = True

        def __init__(self, vertices, num):
            self.vertices = vertices
            self.num = num

    def generate(self):
        y = 100
        num = 0
        while y < 700:
            x = 0
            while x < 1000:
                square = self.Square([(x, y), (x + 50, y), (x + 50, y + 50), (x, y + 50)], num)
                self.square_list.append(square)
                num += 1
                x += 50
            y += 50

        for i in range(0, int(len(self.square_list) / 2)):
            pick = random.choice(self.square_list)
            pick.active = False
            self.blocked_squares.append(pick)

    def print_env(self):
        # ------------ grid lines ----------------
        for i in range(50, 1000, 50):
            pygame.draw.line(screen, BLACK, [i, 100], [i, 700], 1)

        for i in range(100, 700, 50):
            pygame.draw.line(screen, BLACK, [0, i], [1000, i])

        for i in range(0, len(self.blocked_squares)):
            pygame.draw.polygon(screen, BLACK, self.blocked_squares[i].vertices)

carryOn = True
clock = pygame.time.Clock()
env_generated = False
env = Environment()

while carryOn:
    # --- Main event loop -----------
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            carryOn = False  # Flag that we are done so we exit this loop
    screen.fill(WHITE)

    if not env_generated:
        env.generate()
        env_generated = True
    else:
        env.print_env()

    pygame.display.flip()

    clock.tick(60)

pygame.quit()