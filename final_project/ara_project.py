import pygame
import random
import heapq
import math
import re
import time

pygame.init()
X = 1100
Y = 900
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
bright_GREEN = (0, 255, 0)
RED = (200, 0, 0)
bright_RED = (255, 0, 0)
Grey = (105,105,105)
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

    def generate(self, n, d):
        y_coord = 1
        y = 0
        num = 0
        y_max = 800
        x_max = 1000
        if n == 3:
            y_max = 900
            x_max = 1100
        while y < y_max:
            x = 200
            x_coord = 1
            while x < x_max:
                points = [(x, y), (x + n, y), (x + n, y + n), (x, y + n)]
                square = self.Square(points, x_coord, y_coord)
                self.square_list.append(square)
                num += 1
                x += n
                x_coord += 1
            y += n
            y_coord += 1

        for i in range(0, int(len(self.square_list) * d)):
            pick = random.choice(self.square_list)
            pick.active = False
            self.blocked_squares.append(pick)

    def clear(self):
        for sqr in self.square_list:
            sqr.active = True
        self.blocked_squares = []
        self.start = None
        self.end = None

    def regenerate(self, n, d):
        self.square_list = []
        self.active_squares = []
        self.blocked_squares = []
        self.start = None
        self.end = None
        self.generate(n, d)

    def print_env(self, n):
        # ------------ grid lines ----------------
        for i in range(200, 1100, n):
            pygame.draw.line(screen, BLACK, [i, 0], [i, 900], 1)

        for i in range(0, 900, n):
            pygame.draw.line(screen, BLACK, [200, i], [1100, i])

        for i in range(0, len(self.blocked_squares)):
            pygame.draw.polygon(screen, BLACK, self.blocked_squares[i].vertices)

        if n != 3:
            pygame.draw.rect(screen, Grey, (1000, 0, 100, 900))
            pygame.draw.rect(screen, Grey, (200, 800, 900, 100))

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
            for square in self.square_list:
                if square.active:
                    if square.x1 < mouse[0] < square.x2 and square.y1 < mouse[1] < square.y2:
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

int_size = 8
map_size = '100x100'

density = 0.1
curr_density = '10%'

input_font = pygame.font.Font(None, 25)

text1 = ''
input_box1 = pygame.Rect(60, 20, 125, 30)
active1 = False
w = 0

input_box2 = pygame.Rect(60, 60, 125, 30)
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
        env.generate(int_size, density)
        env_generated = True
    else:
        env.print_env(int_size)

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

    font = pygame.font.Font('freesansbold.ttf', 20)
    fontc = pygame.font.Font('freesansbold.ttf', 17)
    pygame.draw.rect(screen, BLACK, (0, 0, 200, 100), 3)
    pygame.draw.rect(screen, BLACK, (0, 100, 200, 150), 3)
    pygame.draw.rect(screen, BLACK, (0, 250, 200, 100), 3)
    pygame.draw.rect(screen, BLACK, (0, 350, 200, 200), 3)
    pygame.draw.rect(screen, BLACK, (0, 550, 200, 250), 3)

    screen.blit(font.render('Controls', True, BLACK, WHITE), (40, 360))
    screen.blit(font.render('Environment', True, BLACK, WHITE), (40, 110))
    screen.blit(font.render('W', True, BLACK, WHITE), (20, 20))
    screen.blit(font.render('dW', True, BLACK, WHITE), (10, 60))
    screen.blit(font.render('Size: ', True, BLACK, WHITE), (20, 260))
    screen.blit(font.render(map_size, True, BLACK, WHITE), (80, 260))
    screen.blit(font.render('Obstacle Density', True, BLACK, WHITE), (20, 560))
    screen.blit(fontc.render('Current: ', True, BLACK, WHITE), (30, 590))
    screen.blit(fontc.render(curr_density, True, BLACK, WHITE), (110, 590))


    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # quit button
    if 50 + 75 > mouse[0] > 50 and 480 + 40 > mouse[1] > 480:
        pygame.draw.rect(screen, bright_RED, (50, 480, 75, 40))
        if click[0] == 1:
            pygame.quit()
    else:
        pygame.draw.rect(screen, RED, (50, 480, 75, 40))
    screen.blit(font.render('quit', True, BLACK, RED), (60, 490))

    # start button
    if not solution_found:
        if 50 + 75 > mouse[0] > 50 and 430 + 40 > mouse[1] > 430:
            pygame.draw.rect(screen, bright_GREEN, (50, 430, 75, 40))
            if click[0] == 1:
                start_time = round(time.time() * 1000)
                solution = simplified_anytime_repairing(env.start, env.end, w, dw)
                end_time = round(time.time()*1000)
                duration = end_time - start_time
                print(duration/1000)
                solution_found = True
        else:
            pygame.draw.rect(screen, GREEN, (50, 430, 75, 40))
    else:
        pygame.draw.rect(screen, bright_GREEN, (50, 430, 75, 40))
    screen.blit(font.render('start', True, BLACK, GREEN), (60, 440))

    # reset
    if 50 + 75 > mouse[0] > 50 and 385 + 40 > mouse[1] > 385:
        pygame.draw.rect(screen, bright_GREEN, (50, 385, 75, 40))
        if click[0] == 1:
            solution_found = False
            solution = None
            env.start = None
            env.end = None
            start_picked = False
            end_picked = False
    else:
        pygame.draw.rect(screen, GREEN, (50, 385, 75, 40))
    screen.blit(font.render('reset', True, BLACK, GREEN), (60, 395))

    # new env
    if 50 + 75 > mouse[0] > 50 and 140 + 40 > mouse[1] > 140:
        pygame.draw.rect(screen, bright_GREEN, (50, 140, 75, 40))
        if click[0] == 1:
            solution = None
            solution_found = False
            start_picked = False
            end_picked = False
            env.regenerate(int_size, density)
    else:
        pygame.draw.rect(screen, GREEN, (50, 140, 75, 40))
    screen.blit(font.render('new', True, BLACK, GREEN), (60, 150))

    # clear
    # new env
    if 50 + 75 > mouse[0] > 50 and 190 + 40 > mouse[1] > 190:
        pygame.draw.rect(screen, bright_GREEN, (50, 190, 75, 40))
        if click[0] == 1:
            solution = None
            solution_found = False
            start_picked = False
            end_picked = False
            env.clear()
    else:
        pygame.draw.rect(screen, GREEN, (50, 190, 75, 40))
    screen.blit(font.render('clear', True, BLACK, GREEN), (50, 200))

    # 100 x 100 button
    if 10 + 50 > mouse[0] > 10 and 290 + 40 > mouse[1] > 290:
        pygame.draw.rect(screen, bright_GREEN, (10, 290, 50, 40))
        if click[0] == 1:
            int_size = 8
            map_size = '100x100'
            solution = None
            solution_found = False
            start_picked = False
            end_picked = False
            env.regenerate(int_size, density)
    else:
        pygame.draw.rect(screen, GREEN, (10, 290, 50, 40))
    screen.blit(font.render('100x', True, BLACK, GREEN), (10, 300))

    # 200 x 200 button
    if 70 + 50 > mouse[0] > 70 and 290 + 40 > mouse[1] > 290:
        pygame.draw.rect(screen, bright_GREEN, (70, 290, 50, 40))
        if click[0] == 1:
            int_size = 4
            map_size = '200x200'
            solution = None
            solution_found = False
            start_picked = False
            end_picked = False
            env.regenerate(int_size, density)
    else:
        pygame.draw.rect(screen, GREEN, (70, 290, 50, 40))
    screen.blit(font.render('200x', True, BLACK, GREEN), (70, 300))

    # 300 x 300 button
    if 130 + 50 > mouse[0] > 130 and 290 + 40 > mouse[1] > 290:
        pygame.draw.rect(screen, bright_GREEN, (130, 290, 50, 40))
        if click[0] == 1:
            int_size = 3
            map_size = '300x300'
            solution = None
            solution_found = False
            start_picked = False
            end_picked = False
            env.regenerate(int_size, density)
    else:
        pygame.draw.rect(screen, GREEN, (130, 290, 50, 40))
    screen.blit(font.render('300x', True, BLACK, GREEN), (130, 300))

    # 10% button
    if 10 + 50 > mouse[0] > 10 and 630 + 40 > mouse[1] > 630:
        pygame.draw.rect(screen, bright_GREEN, (10, 630, 50, 40))
        if click[0] == 1:
            density = 0.10
            curr_density = '10%'
            solution = None
            solution_found = None
            start_picked = False
            end_picked = False
            env.regenerate(int_size, density)
    else:
        pygame.draw.rect(screen, GREEN, (10, 630, 50, 40))
    screen.blit(font.render('10%', True, BLACK, GREEN), (10, 640))

    # 20% button
    if 70 + 50 > mouse[0] > 70 and 630 + 40 > mouse[1] > 630:
        pygame.draw.rect(screen, bright_GREEN, (70, 630, 50, 40))
        if click[0] == 1:
            density = 0.20
            curr_density = '20%'
            solution = None
            solution_found = None
            start_picked = False
            end_picked = False
            env.regenerate(int_size, density)
    else:
        pygame.draw.rect(screen, GREEN, (70, 630, 50, 40))
    screen.blit(font.render('20%', True, BLACK, GREEN), (70, 640))

    # 30% button
    if 130 + 50 > mouse[0] > 130 and 630 + 40 > mouse[1] > 630:
        pygame.draw.rect(screen, bright_GREEN, (130, 630, 50, 40))
        if click[0] == 1:
            density = 0.30
            curr_density = '30%'
            solution = None
            solution_found = None
            start_picked = False
            end_picked = False
            env.regenerate(int_size, density)
    else:
        pygame.draw.rect(screen, GREEN, (130, 630, 50, 40))
    screen.blit(font.render('30%', True, BLACK, GREEN), (130, 640))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()