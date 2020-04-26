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

    def __init__(self):
        self.square_list = []
        self.active_squares = []
        self.blocked_squares = []
        self.start = None
        self.end = None
        self.solution = None

    class Square:
        def __init__(self, vertices, x_coord, y_coord):
            self.vertices = vertices
            self.x1 = vertices[0][0]
            self.x2 = vertices[1][0]
            self.y1 = vertices[0][1]
            self.y2 = vertices[2][1]
            self.x_coord = x_coord
            self.y_coord = y_coord
            self.position = (x_coord, y_coord)
            self.reachable_tiles = []
            self.active = True

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

    def clear(self):
        for sqr in self.square_list:
            sqr.active = True
        self.blocked_squares = []
        self.start = None
        self.end = None

    def regenerate(self):
        self.square_list = []
        self.active_squares = []
        self.blocked_squares = []
        self.start = None
        self.end = None
        self.generate()

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

    @staticmethod
    def print_solution(sol):
        for node in sol.path:
            pygame.draw.polygon(screen, BLUE, node.vertices)

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

    def get_neighboring_tiles(self, tile):
        tile.reachable_tiles = []

        right = (tile.x_coord + 1, tile.y_coord)
        left = (tile.x_coord - 1, tile.y_coord)
        up = (tile.x_coord, tile.y_coord - 1)
        down = (tile.x_coord, tile.y_coord + 1)
        lud = (tile.x_coord - 1, tile.y_coord - 1)
        rud = (tile.x_coord + 1, tile.y_coord - 1)
        lld = (tile.x_coord - 1, tile.y_coord + 1)
        rld = (tile.x_coord + 1, tile.y_coord + 1)

        for sqr in self.square_list:
            if sqr.position == right:
                tile.reachable_tiles.append(sqr)
                continue
            if sqr.position == left:
                tile.reachable_tiles.append(sqr)
                continue
            if sqr.position == up:
                tile.reachable_tiles.append(sqr)
                continue
            if sqr.position == down:
                tile.reachable_tiles.append(sqr)
                continue
            if sqr.position == lud:
                tile.reachable_tiles.append(sqr)
                continue
            if sqr.position == rud:
                tile.reachable_tiles.append(sqr)
                continue
            if sqr.position == lld:
                tile.reachable_tiles.append(sqr)
                continue
            if sqr.position == rld:
                tile.reachable_tiles.append(sqr)
                continue

        return tile.reachable_tiles


class Queue:

    def __init__(self):
        self.li = []
        heapq.heapify(self.li)

    def push(self, node):
        heapq.heappush(self.li, node)

    def pop(self, *nodes):
        if len(nodes) == 0:
            node = heapq.heappop(self.li)
            return node
        else:
            i = 0
            for node in self.li:
                if self.li[i].position == nodes[0].position:
                    node = self.li[i]
                    self.li.pop(i)
                    heapq.heapify(self.li)
                    return node
                i = i + 1
            return None

    def update(self, child):
        self.pop(child)
        heapq.heappush(self.li, child)

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
            if node.g + node.h >= G:
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
    def __init__(self):
        self.path = []
        self.cost = 0

    def add_to_path(self, node):
        self.path.insert(0, node.tile)


def distance(pos1, pos2):
    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]
    d = math.sqrt(math.pow(dx, 2) + math.pow(dy, 2))
    return d


def g_cost(node):
    if node.parent is not None:
        g = node.parent.g + distance(node.parent.position, node.position)
        return g
    else:
        g = 0
        return g


def h_cost(node, end):
    h = distance(node.position, end.position)
    return h


def cost_fw(node, w, end):
    current_node = node.parent
    child = node

    g = g_cost(child)
    h = distance(child.position, end.position)
    f = g + (w * h)
    return f


def get_children(parent_node):
    children = []
    reachable_tiles = env.get_neighboring_tiles(parent_node.tile)
    for t in reachable_tiles:
        if t.active:
            node = Node(parent_node, t)
            children.append(node)
    return children


def improved_solution(open_list, w, G, end):
    while len(open_list.li) > 0:
        current_node = open_list.pop() # pop the node with lowest f(w)

        if G <= cost_fw(current_node, w, end):
            return None # G is proven to be w admissible
        for child in get_children(current_node):
            if not open_list.contains(child) or g_cost(child) < g_cost(open_list.get(child)):
                child.g = g_cost(child)
                child.h = h_cost(child, end)
                child.f = cost_fw(child, w, end)
                if child.g + child.h < G:
                    if child.position == end.position:
                        soln = Solution()
                        soln.cost = child.g
                        soln.add_to_path(child)
                        node = child
                        while node.parent is not None:
                            node = node.parent
                            soln.add_to_path(node)
                        return soln
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
        print('here')
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
solution = None
start_picked = False
end_picked = False
env = Environment()

input_font = pygame.font.Font(None, 25)

text1 = ''
input_box1 = pygame.Rect(60, 20, 175, 30)
active1 = False
w = 0

input_box2 = pygame.Rect(60, 60, 175, 30)
text2 = ''
active2 = False
dw = 0


while carryOn:
    # --- Main event loop -----------
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            carryOn = False  # Flag that we are done so we exit this loop
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_box1.collidepoint(event.pos):
                active1 = True
            else:
                active1 = False
            if input_box2.collidepoint(event.pos):
                active2 = True
            else:
                active2 = False
            # color = color_active if active else color_inactive
        if event.type == pygame.KEYDOWN:
            if active1:
                if event.key == pygame.K_RETURN:
                    print(text1)
                    text1 = ''
                if event.key == pygame.K_BACKSPACE:
                    text1 = text1[:-1]
                else:
                    text1 += event.unicode
            if active2:
                if event.key == pygame.K_RETURN:
                    text1 = ''
                if event.key == pygame.K_BACKSPACE:
                    text2 = text2[:-1]
                else:
                    text2 += event.unicode
    screen.fill(WHITE)

    numbers1 = input_font.render(text1, True, BLACK)
    screen.blit(numbers1, (input_box1.x + 5, input_box1.y + 5))
    pygame.draw.rect(screen, BLACK, input_box1, 2)
    w = float(text1) if re.match(r"[0-9]", text1) else 0


    numbers2 = input_font.render(text2, True, BLACK)
    screen.blit(numbers2, (input_box2.x + 5, input_box2.y + 5))
    pygame.draw.rect(screen, BLACK, input_box2, 2)
    dw = float(text2) if re.match(r"[0-9]", text2) else 0


    if not env_generated:
        env.generate()
        env_generated = True
    else:
        env.print_env()

    if not start_picked:
        if env.pick_start():
            start_picked = True
            continue

    elif not end_picked:
        if env.pick_end():
            end_picked = True
            continue

    if solution_found:
        env.print_solution(solution)

    font = pygame.font.Font('freesansbold.ttf', 30)
    pygame.draw.rect(screen, BLACK, (0, 0, 250, 100), 3)
    pygame.draw.rect(screen, BLACK, (250, 0, 375, 100), 3)
    pygame.draw.rect(screen, BLACK, (625, 0, 350, 100), 3)

    screen.blit(font.render('Controls', True, BLACK, WHITE), (720, 10))
    screen.blit(font.render('Environment', True, BLACK, WHITE), (340, 10))
    screen.blit(font.render('W', True, BLACK, WHITE), (20, 20))
    screen.blit(font.render('dW', True, BLACK, WHITE), (10, 60))

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # quit button
    if 860 + 100 > mouse[0] > 860 and 50 + 40 > mouse[1] > 50:
        pygame.draw.rect(screen, bright_RED, (860, 50, 100, 40))
        if click[0] == 1:
            pygame.quit()
    else:
        pygame.draw.rect(screen, RED, (860, 50, 100, 40))
    screen.blit(font.render('quit', True, BLACK, RED), (885, 55))

    # start button
    if not solution_found:
        if 750 + 100 > mouse[0] > 740 and 50 + 40 > mouse[1] > 50:
            pygame.draw.rect(screen, bright_GREEN, (750, 50, 100, 40))
            if click[0] == 1:
                print('beginning solution search')
                solution = simplified_anytime_repairing(env.start, env.end, w, dw)
                solution_found = True
        else:
            pygame.draw.rect(screen, GREEN, (750, 50, 100, 40))
    else:
        pygame.draw.rect(screen, bright_GREEN, (750, 50, 100, 40))
    screen.blit(font.render('start', True, BLACK, GREEN), (760, 55))

    # reset
    if 640 + 100 > mouse[0] > 640 and 50 + 40 > mouse[1] > 50:
        pygame.draw.rect(screen, bright_GREEN, (640, 50, 100, 40))
        if click[0] == 1:
            solution_found = False
            solution = None
            env.start = None
            env.end = None
            start_picked = False
            end_picked = False
    else:
        pygame.draw.rect(screen, GREEN, (640, 50, 100, 40))
    screen.blit(font.render('reset', True, BLACK, GREEN), (650, 55))

    # new env
    if 260 + 100 > mouse[0] > 260 and 50 + 40 > mouse[1] > 50:
        pygame.draw.rect(screen, bright_GREEN, (260, 50, 100, 40))
        if click[0] == 1:
            solution = None
            solution_found = False
            start_picked = False
            end_picked = False
            env.regenerate()
    else:
        pygame.draw.rect(screen, GREEN, (260, 50, 100, 40))
    screen.blit(font.render('new', True, BLACK, GREEN), (270, 55))

    # clear
    # new env
    if 370 + 100 > mouse[0] > 370 and 50 + 40 > mouse[1] > 50:
        pygame.draw.rect(screen, bright_GREEN, (370, 50, 100, 40))
        if click[0] == 1:
            solution = None
            solution_found = False
            start_picked = False
            end_picked = False
            env.clear()
    else:
        pygame.draw.rect(screen, GREEN, (370, 50, 100, 40))
    screen.blit(font.render('clear', True, BLACK, GREEN), (380, 55))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()