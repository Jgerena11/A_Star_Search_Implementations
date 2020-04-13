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

        for i in range(0, int(len(self.square_list) / 3)):
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

        if self.end is not None:
            pygame.draw.polygon(screen, RED, self.end.vertices)

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
                        return True
                else:
                    continue

    def pick_end(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if click[0] == 1:
            print('clicked')
            for square in self.square_list:
                if square.active:
                    if square.x1 < mouse[0] < square.x2 and square.y1 < mouse[1] < square.y2:
                        if square == self.start:
                            continue
                        else:
                            print(mouse)
                            self.end = square
                            return True
                    else:
                        continue

class Node:
    def __init__(self, parent, tile):
        self.parent = parent
        self.tile = tile
        self.g = 0
        self.h = 0
        self.f = 0

    def __lt__(self, other):
        return self.f < other.f

def improved_solution(open_list, w, G, end):
    closed_list = []
    path = []

    while len(open_list) > 0:
        current_node = heapq.heappop(open_list)
        closed_list.append(current_node)

        if G <= current_node.f:
            return None

        if current_node.tile == end:
            path.append(current_node.position)
            while current_node.parent != None:
                current_node = current_node.parent
                path.append(current_node.tile)
            return path

        children = get_children(current_node)
        for child in children:
            if child in closed_list:
                continue
            compute_cost(child)
            if child not in open_list:



def simplified_anytime_repairing(start, end, w, d):
    G = 999999999999999
    open_list = []
    start_node = Node(None, start)

    open_list.append(start_node)
    heapq.heapify(open_list)

    while len(open) > 0:
        new_solution = improved_solution(open_list, w, G)


def gui():
    font = pygame.font.Font('freesansbold.ttf', 30)
    pygame.draw.rect(screen, BLACK, (100, 0, 250, 100), 3)
    #pygame.draw.rect(screen, BLACK, (400, 0, 250, 100), 3)
    pygame.draw.rect(screen, BLACK, (625, 0, 350, 100), 3)

    screen.blit(font.render('Controls', True, BLACK, WHITE), (720, 10))

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if 850 + 100 > mouse[0] > 850 and 50 + 40 > mouse[1] > 50:
        pygame.draw.rect(screen, bright_RED, (850, 50, 100, 40))
        if click[0] == 1:
            pygame.quit()
    else:
        pygame.draw.rect(screen, RED, (850, 50, 100, 40))
    screen.blit(font.render('quit', True, BLACK, RED), (875, 55))


carryOn = True
clock = pygame.time.Clock()
env_generated = False
start_picked = False
end_picked = False
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
        if env.pick_start():
            continue

    elif env.end is None:
        if env.pick_end():
            continue

    gui()

    pygame.display.flip()

    clock.tick(60)

pygame.quit()