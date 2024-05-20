import pygame
import sys
import random

class MyCar:
    pass

class Trees:
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, speed=7):
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.image = pygame.image.load('img/tree.png')
        self.speed = speed
        self.reset()

    def reset(self):
        self.side_tree = random.choice([(0, self.SCREEN_WIDTH - 1000),
                                        (self.SCREEN_WIDTH - 550, self.SCREEN_WIDTH - 350)])
        self.x = random.randint(self.side_tree[0], self.side_tree[1])
        self.y = -self.image.get_height()

    def update(self):
        self.y += self.speed
        if self.y > self.SCREEN_HEIGHT:
            self.reset()

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


class Forest:
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, num_trees, delay):
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.num_trees = num_trees
        self.delay = delay  # Delay in milliseconds
        self.trees = []
        self.last_tree_time = 0

    def update(self):
        current_time = pygame.time.get_ticks()

        if len(self.trees) < self.num_trees and current_time - self.last_tree_time >= self.delay:
            self.trees.append(Trees(self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
            self.last_tree_time = current_time

        for tree in self.trees:
            tree.update()

    def draw(self, screen):
        for tree in self.trees:
            tree.draw(screen)

class Road:
    def __init__(self, field_width, field_height, speed=5):
        self.field_width = field_width
        self.field_height = field_height + 50
        self.speed = speed
        self.lane_width = 100
        self.line_length = 30
        self.line_spacing = 20
        self.lanes = 4
        self.lines = []
        self.initialize_lines()

    def initialize_lines(self):
        self.lines = []
        for lane in range(1, self.lanes):
            x = (self.field_width // 2 - (self.lane_width * self.lanes // 2)) + lane * self.lane_width
            for y in range(0, self.field_height, self.line_length + self.line_spacing):
                self.lines.append((x, y))

    def update(self):
        for i in range(len(self.lines)):
            x, y = self.lines[i]
            y += self.speed
            if y > self.field_height - self.line_length:
                y = -self.line_length
            self.lines[i] = (x, y)

    def draw(self, field_surface):
        for x, y in self.lines:
            pygame.draw.line(field_surface, (255, 255, 255), (x, y), (x, y + self.line_length), 5)

def main():
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 650

    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Race Game')
    icon = pygame.image.load("img/icon.jpg")
    pygame.display.set_icon(icon)

    field_width, field_height = 400, 650
    field_surface = pygame.Surface((field_width, field_height))
    field_rect = field_surface.get_rect(topleft=(250, 0))

    clock = pygame.time.Clock()
    game_running = True
    forest = Forest(SCREEN_WIDTH, SCREEN_HEIGHT, num_trees=10, delay=1500)
    road = Road(field_width, field_height)

    while game_running:
        delta_time = clock.tick(30)  # Теперь возвращает миллисекунды с последнего вызова

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False

        screen.fill('green')
        field_surface.fill('grey51')

        forest.update()
        road.update()

        road.draw(field_surface)
        forest.draw(screen)

        screen.blit(field_surface, field_rect.topleft)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

main()
