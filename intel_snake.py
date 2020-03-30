import pygame
import math

END = (380, 300)
DIRECTIONS = [[10, 0], [0, 10], [-10, 0],  [0, -10]]
BLOCKED_CELLS = [(60, 10), (50, 10), (40, 10), (30, 10), (20, 10), (70, 10), (80, 10), (90, 10), (100, 10), (100, 20),
                 (100, 30), (100, 40), (100, 50),
                 (100, 60), (100, 70), (100, 80), (100, 90), (100, 100), (100, 110), (100, 120), (60, 200), (50, 200),
                 (40, 200), (30, 200), (20, 200),
                 (10, 200), (0, 200), (70, 200), (80, 200), (90, 200), (100, 200), (110, 200), (120, 200), (130, 200),
                 (140, 200), (150, 200), (160, 200),
                 (170, 200), (180, 200), (190, 200), (200, 200), (210, 200), (210, 190), (210, 180),
                 (300, 40), (300, 50), (300, 60), (300, 70), (300, 80), (300, 90),
                 (300, 100), (300, 110), (300, 120), (300, 130), (300, 140), (300, 150),
                 (300, 160), (300, 170), (300, 180), (300, 190), (300, 200),
                 (300, 210), (300, 220), (300, 230), (300, 240), (300, 250),(360,340),(370,340),(380,340),(390,340),
                 (170,140),(180,140),(190,140),(200,140),(210,140),(220,140),(230,140),(240,140),(250,140),(260,140),(270,140),(280,140),(290,140),
                 (100,340),(110,340),(120,340),(130,340),(140,340),(150,340),(160,340),(170,340),(180,340),(190,340),(200,340),(210,340),(220,340),
                 (230,340),(240,340),(250,340),(260,340),(270,340),(280,340),(290,340),(300,340),(310,340),(320,340),(330,340),(340,340),(350,340),]
snake = [(0, 0), (10, 0), (20, 0), (30, 0)]
START = snake[3]
snake_w = 10
snake_h = 10
velocity_x = 0
velocity_y = 0
direction = ''
fps = 10
snake_move = False
step = 0
dest = False


def nearest(num):
    if abs(math.floor(num / 10) - num / 10) < abs(math.ceil(num / 10) - num / 10):
        return math.floor(num / 10) * 10
    else:
        return math.ceil(num / 10) * 10


class Node:

    def __init__(self, current_pos, previous_pos, g, h):
        self.current_pos = current_pos
        self.previous_pos = previous_pos
        self.h = h
        self.g = g

    def f(self):
        return self.h + self.g


def heuristic_cost(node_pos):
    cost = abs(node_pos[0] - END[0]) + abs(node_pos[1] - END[1])
    return (cost / 10)


def get_best_node(open_set):
    firstEnter = True

    for node in open_set.values():
        if firstEnter or node.f() < bestF:
            firstEnter = False
            bestNode = node
            bestF = bestNode.f()
    return bestNode


def get_adjacent_node(node):
    list_of_node = []

    for dir in DIRECTIONS:
        new_pos = (node.current_pos[0] + dir[0], node.current_pos[1] + dir[1])
        if 0 <= new_pos[0] <= 390 and 0 <= new_pos[1] <= 390:
            list_of_node.append(Node(new_pos, node.current_pos, node.g + 1, heuristic_cost(new_pos)))

    return list_of_node


def min_path(closed_set):
    path = []
    node = closed_set[str(END)]
    while node.current_pos != START:
        path.insert(0, node.current_pos)
        node = closed_set[str(node.previous_pos)]
    return path


def is_blocked(node):
    blocked = False
    if node.current_pos in BLOCKED_CELLS:
        blocked = True
    return blocked


def main(start_pos):
    open_set = {str(start_pos): Node(start_pos, start_pos, 0, heuristic_cost(start_pos))}
    closed_set = {}

    while True:
        test_node = get_best_node(open_set)
        closed_set[str(test_node.current_pos)] = test_node

        if test_node.current_pos == END:
            return min_path(closed_set)

        adj_node = get_adjacent_node(test_node)

        for node in adj_node:
            if is_blocked(node) or str(node.current_pos) in closed_set.keys() or str(
                    node.current_pos) in open_set.keys() and open_set[
                str(node.current_pos)].f() < node.f():
                continue
            open_set[str(node.current_pos)] = node
        del open_set[str(test_node.current_pos)]


path = main(START)

# initiate pygame module--- required
pygame.init()

# screen
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption('my game window')
running = True

# clock
clock = pygame.time.Clock()

# main loop
while running:
    # key event
    for event in pygame.event.get():
        # closing events
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = event.pos
                new_pos_x = nearest(pos[0])
                new_pos_y = nearest(pos[1])
                if (new_pos_x, new_pos_y) not in BLOCKED_CELLS:
                    snake_move = True
                    END = (new_pos_x, new_pos_y)
                    START = snake[3]
                    path = main(START)
                    step = 0
                    dest = True

    if snake_move:
        snake.append(path[step])
        snake.pop(0)
        if snake[3] != END:
            step += 1
        else:
            snake_move = False

    # screen color
    screen.fill((255, 255, 255))
    if dest:
        pygame.draw.rect(screen, (0, 255, 0), [END[0], END[1], 10, 10])

    # blocked draw
    for b in BLOCKED_CELLS:
        pygame.draw.rect(screen, (0, 0, 0), [b[0], b[1], 10, 10])

    # rectangle draw
    for pos in range(len(snake)):
        if pos < 3:
            pygame.draw.rect(screen, (0, 255, 255), [snake[pos][0], snake[pos][1], snake_w, snake_h])
        else:
            pygame.draw.rect(screen, (255, 0, 255), [snake[pos][0], snake[pos][1], snake_w, snake_h])
    # update display--- required
    pygame.display.update()
    clock.tick(fps)

pygame.quit()
quit()
