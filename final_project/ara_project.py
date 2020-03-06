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
bright_GREEN = (0, 255, 0)
RED = (200, 0, 0)
bright_RED = (255, 0, 0)
size = (X, Y)
screen = pygame.display.set_mode(size)

class Environment:
    square_list = []
    active_squares = []
    blocked_squares = []
    start = None
    end = None

    class Square:
        x1 = 0
        x2 = 0
        y1 = 0
        y2 = 0
        x_coord = []
        y_coord = []
        vertices = []
        active = True

        def __init__(self, vertices, x_coord, y_coord):
            self.vertices = vertices
            self.x1 = vertices[0][0]
            self.x2 = vertices[1][0]
            self.y1 = vertices[0][1]
            self.y2 = vertices[2][1]
            self.x_axis = x_coord
            self.y_axis = y_coord

    def generate(self):
        y_coord = 1
        y = 100
        num = 0
        while y < 700:
            x = 0
            x_coord = 1
            while x < 1000:
                points = [(x, y), (x + 50, y), (x + 50, y + 50), (x, y + 50)]
                square = self.Square(points, x_coord, y_coord)
                self.square_list.append(square)
                num += 1
                x += 50
                x_coord += 1
            y += 50
            y_coord += 1

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

        if self.start is not None:
            pygame.draw.polygon(screen, GREEN, self.start.vertices)

    def pick_start(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if click[0] == 1:
            print('clicked')
            for square in self.square_list:
                if square.active:
                    if square.x1 < mouse[0] < square.x2 and square.y1 < mouse[1] < square.y2:
                        print(mouse)
                        self.start = square
                else:
                    continue

carryOn = True
clock = pygame.time.Clock()
env_generated = False
start_picked = False
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

    if env.start is None:
        env.pick_start()



    pygame.display.flip()

    clock.tick(60)

pygame.quit()