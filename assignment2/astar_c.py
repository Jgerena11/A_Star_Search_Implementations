import pygame
from shapely.geometry import LinearRing, LineString, Point, Polygon
import heapq
import re

pygame.init()
X = 1100
Y = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
bright_GREEN = (0, 255, 0)
RED = (200, 0, 0)
bright_RED = (255, 0, 0)
size = (X, Y)
screen = pygame.display.set_mode(size)


class Environment:
    array_of_shapes = []
    array_of_vertices = []
    start_position = (0, 0)
    goal_position = (0, 0)

    def __init__(self, env):
        if env == 'a':
            self.environment1()
        elif env == 'b':
            self.environment2()

    # ------methods for shape creation -------------
    def createShape(self, coordinates):
        self.array_of_shapes.append(coordinates)
        for index in range(0, len(coordinates)):
            self.array_of_vertices.append(coordinates[index])

    def environment1(self):
        # ------- hard coded shapes ----------------------
        self.start_position = (100, 500)
        self.goal_position = (950, 175)
        self.createShape([(200, 450), (550, 450), (550, 550), (200, 550)])  # shape A
        self.createShape([(400, 225), (360, 400), (440, 400)])  # shape B
        self.createShape([(585, 350), (605, 500), (670, 450)])  # shape C
        self.createShape([(275, 390), (350, 260), (275, 160), (165, 275), (185, 375)])  # shape D
        self.createShape([(470, 295), (475, 160), (555, 150), (625, 200)])  # shape E
        self.createShape([(650, 175), (775, 175), (775, 400), (650, 400)])  # shape F
        self.createShape([(725, 450), (725, 525), (795, 560), (860, 525), (860, 450), (800, 400)])  # shape G
        self.createShape([(800, 200), (860, 165), (900, 200), (875, 415)])  # shape H

    def environment2(self):
        # ------- hard coded shapes ----------------------
        # insert new start and end here
        self.start_position = (100, 150)
        self.goal_position = (950, 500)
        self.createShape([(200, 200), (300, 150), (350, 250), (200, 300)])  # shape A
        self.createShape([(150, 350), (200, 450), (440, 400)])  # shape B
        self.createShape([(400, 200), (500, 200), (500, 350), (400, 350)])  # shape C
        self.createShape([(400, 520), (425, 450), (500, 400), (550, 500)])  # shape D
        self.createShape([(575, 450), (550, 400), (555, 325), (725, 350)])  # shape E
        self.createShape([(600, 150), (700, 150), (750, 200), (750, 250), (700, 300), (600, 300), (550, 250)])  # shape F
        self.createShape([(650, 450), (750, 450), (850, 550), (600, 550)])  # shape G
        self.createShape([(800, 450), (800, 200), (900, 200), (855, 300), (900, 350)])  # shape H

    def switch_env(self, choice):
        if choice == 'a':
            self.array_of_vertices = []
            self.array_of_shapes = []
            self.environment1()
        elif choice == 'b':
            self.array_of_vertices = []
            self.array_of_shapes = []
            self.environment2()

    def draw_env(self):
        # start label and point
        font3 = pygame.font.Font('freesansbold.ttf', 20)
        start_text = font3.render('Start', True, BLACK, WHITE)
        screen.blit(start_text, (self.start_position[0] - 50, self.start_position[1]))
        pygame.draw.circle(screen, BLACK, self.start_position, 5, 0)

        # end label and point
        end_text = font3.render('End', True, BLACK, WHITE)
        screen.blit(end_text, (self.goal_position[0] + 5, self.goal_position[1]))
        pygame.draw.circle(screen, BLACK, self.goal_position, 5, 0)
        for i in range(0, len(self.array_of_shapes)):
            pygame.draw.polygon(screen, BLACK, self.array_of_shapes[i], 3)

class Path:

    array_of_shapes = []
    array_of_vertices = []
    goal_path = []

    #-------for Astar implementation -------------
    class Node:
        def __init__(self, parent, coord):
            self.parent = parent
            self.position = coord
            self.g = 0
            self.h = 0
            self.f = 0

        def __lt__(self, other):
            return self.f < other.f

    def __init__(self, shapes, vertices):
        self.array_of_shapes = shapes
        self.array_of_vertices = vertices

    def get_path(self, start, end, C):
        self.goal_path = self.Astar(start, end, C)
        return self.goal_path

    def crosses(self, shape, coord1, coord2):
        polygon = Polygon(shape)
        line = LineString([coord1, coord2])
        if line.intersects(polygon):
            if line.touches(polygon):
                return False
            elif line.crosses(polygon) or polygon.contains(line):
                return True

    def get_children(self, node):
        children = []
        for k in range(0, len(self.array_of_vertices)):
            flag = False
            if self.array_of_vertices[k] == node.position:
                continue
            else:
                for j in range(0, len(self.array_of_shapes)):
                    if self.crosses(self.array_of_shapes[j], node.position, self.array_of_vertices[k]):
                        flag = True
            if flag:
                continue
            else:
                child_node = self.Node(node, self.array_of_vertices[k])
                children.append(child_node)
        return children

    def distance(self, start, end):
        Line = LineString([start, end])
        return Line.length

    def Astar(self, start, end, C):
        start_Node = self.Node(None, start)
        end_node = self.Node(None, end)
        self.array_of_vertices.append(end)

        open_list = []
        closed_list = []
        path = []
        heapq.heapify(open_list)

        open_list.append(start_Node)

        while len(open_list) > 0:
            current_node = heapq.heappop(open_list)
            closed_list.append(current_node.position)

            if current_node.position == end:
                path.append(current_node.position)
                while current_node.parent != None:
                    current_node = current_node.parent
                    path.append(current_node.position)
                return path

            #get child nodes --------------------------
            children = self.get_children(current_node)

            for child in children:
                if child.position in closed_list:
                    continue
                child.g = current_node.g + self.distance(current_node.position, child.position)
                child.h = self.distance(child.position, end)
                child.f = child.g + child.h
                if child.f >= C:
                    continue
                for node in open_list:
                    if child.position == node.position and child.g > node.g:
                        continue
                open_list.append(child)
        return None

    def draw_path(self):
        if self.goal_path != None:
            for i in range(0, len(self.goal_path)):
                if i < len(self.goal_path) - 1:
                    pygame.draw.line(screen, RED, self.goal_path[i], self.goal_path[i + 1], 3)
                    i += 1
        else:
            font = pygame.font.Font('freesansbold.ttf', 100)
            screen.blit(font.render('No Solution Found', True, BLACK), (150, 250))

path_found = False
choice = 'a'
cost = 0
cost_input_flag = 0
env = Environment(choice)
path = Path(env.array_of_shapes, env.array_of_vertices)
carryOn = True
clock = pygame.time.Clock()
font1 = pygame.font.Font(None, 30)
input_font = pygame.font.Font(None, 25)
text = ''
input_box = pygame.Rect(150, 50, 150, 40)
active = False

while carryOn:
    # --- Main event loop -----------
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            carryOn = False  # Flag that we are done so we exit this loop
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                active = True
            else:
                active = False
            # color = color_active if active else color_inactive
        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    print(text)
                    text = ''
                if event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
    screen.fill(WHITE)

    font = pygame.font.Font('freesansbold.ttf', 30)
    pygame.draw.rect(screen, BLACK, (100, 0, 250, 100), 3)
    pygame.draw.rect(screen, BLACK, (400, 0, 250, 100), 3)
    pygame.draw.rect(screen, BLACK, (700, 0, 350, 100), 3)

    screen.blit(font.render('Cost', True, BLACK, WHITE), (200, 10))
    screen.blit(font.render('Environment', True, BLACK, WHITE), (430, 10))
    screen.blit(font.render('Controls', True, BLACK, WHITE), (820, 10))

    numbers = input_font.render(text, True, BLACK)
    screen.blit(numbers, (input_box.x + 5, input_box.y + 5))
    pygame.draw.rect(screen, BLACK, input_box, 2)
    cost = float(text) if re.match(r"[0-9]", text) else 0

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if 410 + 100 > mouse[0] > 410 and 50 + 40 > mouse[1] > 50:
        pygame.draw.rect(screen, bright_GREEN, (410, 50, 100, 40))
        if click[0] == 1:
            choice = 'a'
            env.switch_env(choice)
            path_found = False
            cost_input_flag = 0
    else:
        pygame.draw.rect(screen, GREEN, (410, 50, 100, 40))

    if 535 + 100 > mouse[0] > 535 and 50 + 40 > mouse[1] > 50:
        pygame.draw.rect(screen, bright_RED, (535, 50, 100, 40))
        if click[0] == 1:
            choice = 'b'
            env.switch_env(choice)
            path_found = False
            cost_input_flag = 0
    else:
        pygame.draw.rect(screen, RED, (535, 50, 100, 40))

    if 940 + 100 > mouse[0] > 940 and 50 + 40 > mouse[1] > 50:
        pygame.draw.rect(screen, bright_RED, (940, 50, 100, 40))
        if click[0] == 1:
            pygame.quit()
    else:
        pygame.draw.rect(screen, RED, (940, 50, 100, 40))

    if 825 + 100 > mouse[0] > 825 and 50 + 40 > mouse[1] > 50:
        pygame.draw.rect(screen, bright_RED, (825, 50, 100, 40))
        if click[0] == 1:
            cost_input_flag = 0
            path_found = False
    else:
        pygame.draw.rect(screen, RED, (825, 50, 100, 40))

    if not path_found:
        if 710 + 100 > mouse[0] > 710 and 50 + 40 > mouse[1] > 50:
            pygame.draw.rect(screen, bright_GREEN, (710, 50, 100, 40))
            if click[0] == 1:
                if text == '':
                    cost_input_flag = 1
                elif not re.match(r"[0-9]", text):
                    cost_input_flag = 2
                else:
                    cost_input_flag = 0
                    path = Path(env.array_of_shapes, env.array_of_vertices)
                    path.get_path(env.start_position, env.goal_position, cost)
                    path_found = True
        else:
            pygame.draw.rect(screen, GREEN, (710, 50, 100, 40))
    else:
        pygame.draw.rect(screen, bright_GREEN, (710, 50, 100, 40))

    screen.blit(font.render('A', True, BLACK, GREEN), (450, 55))
    screen.blit(font.render('B', True, BLACK, RED), (565, 55))
    screen.blit(font.render('quit', True, BLACK, RED), (950, 55))
    screen.blit(font.render('start', True, BLACK, GREEN), (725, 55))
    screen.blit(font.render('reset', True, BLACK, RED), (840, 55))

    env.draw_env()

    if cost_input_flag == 1:
        warning = pygame.font.Font('freesansbold.ttf', 20)
        screen.blit(warning.render('Must enter cost', True, RED), (750, 110))
    elif cost_input_flag == 2:
        warning = pygame.font.Font('freesansbold.ttf', 20)
        screen.blit(warning.render('Please enter integers only', True, RED), (120, 110))
    if path_found:
        path.draw_path()

    pygame.display.flip()

    clock.tick(60)

pygame.quit()