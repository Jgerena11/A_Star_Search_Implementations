import pygame
from shapely.geometry import LinearRing, LineString, Point, Polygon
import heapq

pygame.init()
X = 1100
Y = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
size = (X, Y)
screen = pygame.display.set_mode(size)

array_of_shapes = []
array_of_vertices = []
goal_path = []
start_position = (100, 500)
goal_position = (950, 175)

#-------for Astar implementation -------------
class Node():
    def __init__(self, parent, coord):
        self.parent = parent
        self.position = coord
        self.g = 0
        self.h = 0
        self.f = 0

    def __lt__(self, other):
        return self.f < other.f

def crosses(shape, coord1, coord2):
    polygon = Polygon(shape)
    line = LineString([coord1, coord2])
    if line.intersects(polygon):
        if line.touches(polygon):
            return False
        elif line.crosses(polygon):
            return True

def get_children(node):
    children2 = []
    for k in range(0, len(array_of_vertices)):
        flag = False
        if array_of_vertices[k] == node.position:
            continue
        else:
            for j in range(0, len(array_of_shapes)):
                if crosses(array_of_shapes[j], node.position, array_of_vertices[k]):
                    flag = True
        if flag:
            continue
        else:
            child_node = Node(node, array_of_vertices[k])
            children2.append(child_node)
    return children2

def distance(start, end):
    Line = LineString([start, end])
    return Line.length

def Astar(start, end):
    start_Node = Node(None, start)
    end_node = Node(None, end)
    array_of_vertices.append(end)

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
        children = get_children(current_node)

        for child in children:

            if child.position in closed_list:
                continue
            child.g = current_node.g + distance(current_node.position, child.position)
            child.h = distance(child.position, end)
            child.f = child.g + child.h
            for node in open_list:
                if child.position == node.position and child.g > node.g:
                    continue
            open_list.append(child)

#------methods for shape creation -------------
def createShape(coordinates):
    array_of_shapes.append(coordinates)
    for index in range(0, len(coordinates)):
        array_of_vertices.append(coordinates[index])

# ------- hard coded shapes ----------------------
createShape([(200, 450), (550, 450), (550, 550), (200, 550)]) #shape A
createShape([(400, 225), (360, 400), (440, 400)]) #shape B
createShape([(585, 350), (605, 500), (670, 450)]) #shape C
createShape([(275, 390), (350, 260), (275, 160), (165, 275), (185, 375)]) #shape D
createShape([(470, 295), (475, 160), (555, 150), (625, 200)]) #shape E
createShape([(650, 175), (775, 175), (775, 400), (650, 400)]) #shape F
createShape([(725, 450), (725, 525), (795, 560), (860, 525), (860, 450), (800, 400)]) #shape G
createShape([(800, 200), (860, 165), (900, 200), (875, 415)]) #shape H

carryOn = True
clock = pygame.time.Clock()
Astar_stop = False
while carryOn:
    # --- Main event loop -----------
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            carryOn = False  # Flag that we are done so we exit this loop
    screen.fill(WHITE)

    # --------generate shapes --------------------
    for i in range(0, len(array_of_shapes)):
        pygame.draw.polygon(screen, BLACK, array_of_shapes[i], 3)

    # ----------generate goal path ---------------
    for i in range(0, len(goal_path)):
        if i < len(goal_path) - 1:
            pygame.draw.line(screen, RED, goal_path[i], goal_path[i+1], 3)
            i += 1

    # start label and point
    font3 = pygame.font.Font('freesansbold.ttf', 20)
    start_text = font3.render('Start', True, BLACK, WHITE)
    screen.blit(start_text, (50, 515))
    pygame.draw.circle(screen, BLACK, start_position, 5, 0)

    # end label and point
    end_text = font3.render('End', True, BLACK, WHITE)
    screen.blit(end_text, (955, 180))
    pygame.draw.circle(screen, BLACK, goal_position, 5, 0)

    if not Astar_stop:
        goal_path = Astar(start_position, goal_position)
        Astar_stop = True

    pygame.display.flip()

    clock.tick(60)

pygame.quit()