import pygame
import random
import heapq
import math
import re

pygame.init()
X = 1000
Y = 700
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
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
        reachable_tiles = []
        x1 = 0
        x2 = 0
        y1 = 0
        y2 = 0
        vertices = []
        position = None
        active = True

        def __init__(self, vertices, x_coord, y_coord):
            self.vertices = vertices
            self.x1 = vertices[0][0]
            self.x2 = vertices[1][0]
            self.y1 = vertices[0][1]
            self.y2 = vertices[2][1]
            self.position = (x_coord, y_coord)

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

        for tile in self.square_list:
            temp = [(tile.x1, tile.y1), (tile.x2, tile.y1), (tile.x2, tile.y2), (tile.x1, tile.y2)]
            right = [(tile.x1 + 50, tile.y1), (tile.x2 + 50, tile.y1), (tile.x2 + 50, tile.y2), (tile.x1 + 50, tile.y2)]
            left = [(tile.x1 - 50, tile.y1), (tile.x2 - 50, tile.y1), (tile.x2 - 50, tile.y2), (tile.x1 - 50, tile.y2)]
            up = [(tile.x1, tile.y1 - 50), (tile.x2, tile.y1 - 50), (tile.x2, tile.y2 - 50), (tile.x1, tile.y2 - 50)]
            down = [(tile.x1, tile.y1 + 50), (tile.x2, tile.y1 + 50), (tile.x2, tile.y2 + 50), (tile.x1, tile.y2 + 50)]
            lud = [(tile.x1 - 50, tile.y1 - 50), (tile.x2 - 50, tile.y1 - 50), (tile.x2 - 50, tile.y2 -50), (tile.x1 - 50, tile.y2 - 50)]
            rud = [(tile.x1 + 50, tile.y1 - 50), (tile.x2 + 50, tile.y1 - 50), (tile.x2 + 50 , tile.y2 - 50), (tile.x1 + 50, tile.y2 - 50)]
            lld = [(tile.x1 - 50, tile.y1 + 50), (tile.x2 - 50, tile.y1 + 50), (tile.x2 - 50, tile.y2 + 50), (tile.x1 - 50, tile.y2 + 50)]
            rld = [(tile.x1 + 50, tile.y1 + 50), (tile.x2 + 50, tile.y1 + 50), (tile.x2 + 50, tile.y2 + 50), (tile.x1 + 50, tile.y2 + 50)]

            for sqr in self.square_list:
                if sqr.vertices == right:
                    tile.reachable_tiles.append(sqr)
                if sqr.vertices == left:
                    tile.reachable_tiles.append(sqr)
                if sqr.vertices == up:
                    tile.reachable_tiles.append(sqr)
                if sqr.vertices == down:
                    tile.reachable_tiles.append(sqr)
                if sqr.vertices == lud:
                    tile.reachable_tiles.append(sqr)
                if sqr.vertices == rud:
                    tile.reachable_tiles.append(sqr)
                if sqr.vertices == lld:
                    tile.reachable_tiles.append(sqr)
                if sqr.vertices == rld:
                    tile.reachable_tiles.append(sqr)

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

    def print_solution(self, solution):
        for node in solution:
            pygame.draw.polygon(screen, BLUE, node.tile.vertices)

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


class Queue:
    li = []
    heapq.heapify(li)

    def push(self, node):
        heapq.heappush(self.li, node)

    def pop(self, *nodes):
        if len(nodes) == 0:
            node = heapq.heappop(self.li)
            return node
        else:
            for i in range(0, len(self.li)):
                if self.li[i].position == nodes[0].position:
                    node = self.li[i]
                    self.li[i] = self.li[-1]
                    self.li.pop()
                    heapq.heapify(self.li)
            return node

    def update(self, child):
        node = self.get(child)
        heapq.heappop(node)
        heapq.heapush(self.li, child)

    def contains(self, child):
        for node in self.li:
            if node.position == child.position:
                return True
        return False

    def get(self, child):
        for node in self.li:
            if node.position == child.position:
                return node
        return None

    def prune(self, G):
        for node in self.li:
            if node.g + node.h <= G:
                self.pop(node)


class Node:
    def __init__(self, parent, tile):
        self.parent = parent
        self.tile = tile
        self.g = 0
        self.h = 0
        self.f = 0
        self.position = tile.position

    def __lt__(self, other):
        return self.f < other.f


class Solution:
    path = []
    cost = 0

    def add_to_path(self, node):
        self.path.insert(0, node.tile)


def distance(pos1, pos2):
    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]
    d = math.sqrt(math.pow(dx, 2) + math.pow(dy, 2))
    return d


def cost_fw(node, w, end):
    current_tile = node.parent.tile
    child_tile = node.tile

    g = distance(current_tile.position, child_tile.position)
    h = distance(child_tile.position, end.position)
    f = g + (w * h)
    return f


def get_children(parent_node):
    children = []
    tile = parent_node.tile
    for t in tile.reachable_tiles:
        if t.active:
            node = Node(parent_node, t)
            children.append(node)
    return children


def improved_solution(open_list, w, G, end):
    while len(open_list.li) > 0:
        current_node = open_list.pop() # pop the node with lowest f(w)

        if G <= current_node.f:
            return None # G is proven to be w admissible
        for child in get_children(current_node):
            cost_fw(child, w, end)
            if not open_list.contains(child) or child.g < open_list.get(child).g:
                if child.g + child.h < G:
                    if child.tile.position == end.position:
                        solution = Solution()
                        solution.cost = child.g
                        solution.add_to_path(child)
                        node = child
                        while node.parent is not None:
                            node = node.parent
                            solution.add_to_path(node)
                        return solution
                    else:
                        if open_list.contains(child):
                            open_list.update(child)
                        else:
                            open_list.push(child)
    return None # no solution better than G exists


def simplified_anytime_repairing(start, end, w, dw):
    G = 999999999999999
    open_list = Queue()
    incumbent = None
    start_node = Node(None, start)
    open_list.push(start_node)

    while len(open_list.li) > 0:
        new_solution = improved_solution(open_list, w, G, end)
        if new_solution is not None:
            G = new_solution.cost
            incumbent = new_solution
        else:
            return incumbent
        w = w - dw
        open_list.prune(G)
    return incumbent


carryOn = True
clock = pygame.time.Clock()
env_generated = False
solution_found = False
start_picked = False
end_picked = False
env = Environment()
w = 100
dw = 10


def gui():
    global solution_found
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

    if not solution_found:
        if 710 + 100 > mouse[0] > 710 and 50 + 40 > mouse[1] > 50:
            pygame.draw.rect(screen, bright_GREEN, (710, 50, 100, 40))
            if click[0] == 1:
                solution = simplified_anytime_repairing(env.start, env.end, w, dw)
                solution_found = True
        else:
            pygame.draw.rect(screen, GREEN, (710, 50, 100, 40))
    else:
        pygame.draw.rect(screen, bright_GREEN, (710, 50, 100, 40))
    screen.blit(font.render('start', True, BLACK, GREEN), (725, 55))


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