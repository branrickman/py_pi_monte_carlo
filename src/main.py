import pygame
from random import randint
from math import sqrt

pygame.init()

SCREEN_SIDE_SIZE: int = 901
assert SCREEN_SIDE_SIZE % 2 != 0, "Error: SCREEN_SIDE_SIZE must be an odd integer"

FPS = 200

screen = pygame.display.set_mode((SCREEN_SIDE_SIZE, SCREEN_SIDE_SIZE))
pygame.display.set_caption("Monte Carlo Pi Calculator")
clock = pygame.time.Clock()

# define colors (generated at coolers.co)
TURQUOISE = "#55DDE0"
YELLOW = "#F6AE2D"
ORANGE = "#F26419"
PURPLE = "#5E3E7A"
GREY = "#464946"

# import font
selected_font = pygame.font.Font('assets/font.ttf', 30)  # https://fonts.google.com/specimen/Inconsolata


def render_text(text, position, color=GREY):
    """ renders input text at a given position in a given color (RGB or Hex) """
    rendered_text = selected_font.render(text, True, color)
    screen.blit(rendered_text, position)


def print_fps():
    """ prints the framerate to the top left of the screen"""
    render_text(str(f'FPS: {int(clock.get_fps())}'),
                (10, 10))  # https://stackoverflow.com/questions/67946230/show-fps-in-pygame


class Point:
    def __init__(self, x=SCREEN_SIDE_SIZE // 2, y=SCREEN_SIDE_SIZE // 2, color=TURQUOISE, radius=3):
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)


class Square:
    def __init__(self, x=0, y=0, color=GREY, size=SCREEN_SIDE_SIZE):
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.rect = pygame.Rect(x, y, size, size)

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)


def choose_random_point():
    """returns a Point with random x and y coordinates within the range from 0 to SCREEN_SIDE_SIZE"""
    random_point = Point(randint(0, SCREEN_SIDE_SIZE), randint(0, SCREEN_SIDE_SIZE))
    return random_point


def point_in_circle(point, circle):
    """ is a given point inside a given circle"""
    delta_x = abs(circle.x - point.x)
    delta_y = abs(circle.y - point.y)
    if sqrt(delta_x ** 2 + delta_y ** 2) > circle.radius:  # test if point outside circle
        return False
    else:
        return True


# objects to draw
square = Square()
circle = Point(color=ORANGE, radius=SCREEN_SIDE_SIZE // 2)
point_array = []
update_estimate_this_frame = False

# bookkeeping
points_in_circle = 0
points_outside_circle = 1  # initialize to 1 to avoid dividing by 0
pi_estimate = 0


# timers
pygame.time.set_timer(pygame.USEREVENT + 1, 1)
pygame.time.set_timer(pygame.USEREVENT + 2, 1000)

run = True
play = True
debug = False  # places a point at the mouse position each update tick
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                play = not play
        if event.type == pygame.USEREVENT+1 and play and debug:
            pos = pygame.mouse.get_pos()
            new_point = Point(pos[0], pos[1])
            point_array.append(new_point)
            if point_in_circle(new_point, circle):
                points_in_circle += 1
            else:
                points_outside_circle += 1
        if event.type == pygame.USEREVENT+1 and play and not debug:
            # draw new point
            new_point = choose_random_point()
            point_array.append(new_point)
            if point_in_circle(new_point, circle):
                points_in_circle += 1
            else:
                points_outside_circle += 1
        if event.type == pygame.USEREVENT + 2:  # only render each time the timer hits (make estimate readable)
            update_estimate_this_frame = True

    square.draw()
    circle.draw()
    for point in point_array:
        point.draw()

    if update_estimate_this_frame:
        # print(f'in circle: {points_in_circle} \n 'f'outside circle: {points_outside_circle}')
        pi_estimate = round(4 * points_in_circle / (points_outside_circle + points_in_circle), 5)
        update_estimate_this_frame = False

    render_text(f'pi estimate: {pi_estimate}', (SCREEN_SIDE_SIZE // 2 - 150, SCREEN_SIDE_SIZE - 100),
                color=PURPLE)  # TODO: Center text

    print_fps()  #TODO not working for some reason
    clock.tick(FPS)
    pygame.display.update()
