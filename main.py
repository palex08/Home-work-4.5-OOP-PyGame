import pygame
import sys
import random


class MyCar:
    def __init__(self, road_width, road_height, speed=6):
        self.image = pygame.image.load('img/mycar.png')
        self.road_width = road_width
        self.road_height = road_height
        self.x = self.road_width // 2 - self.image.get_width() // 2
        self.y = self.road_height - 150
        self.speed = speed  # Скорость перемещения машины

    def draw(self, field_surface):
        field_surface.blit(self.image, (self.x, self.y))

    def move_left(self):
        if self.x - self.speed - 50 >= 0:
            self.x -= self.speed

    def move_right(self):
        if self.x + self.speed <= self.road_width - self.image.get_width() - 50:
            self.x += self.speed


class Trees:
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, speed=6):
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.image = pygame.image.load('img/tree.png')
        self.speed = speed
        self.side_tree = random.choice([(0, self.SCREEN_WIDTH - 1030),
                                        (self.SCREEN_WIDTH - 550, self.SCREEN_WIDTH - 380)])
        self.x = random.randint(self.side_tree[0], self.side_tree[1])
        self.y = 0 - self.image.get_height()
        trees_list.append(self)

    def update(self):
        self.y += self.speed
        if self.y > self.SCREEN_HEIGHT:
            trees_list.remove(self)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


class Road:
    def __init__(self, road_width, road_height, speed=6):
        self.road_width = road_width
        self.road_height = road_height + 50
        self.speed = speed
        self.lane_width = 60
        self.line_length = 30
        self.line_spacing = 20
        self.lanes = 6
        self.lines = []
        self.initialize_lines()

    def initialize_lines(self):
        self.lines = []
        for lane in range(1, self.lanes):
            x = (self.road_width // 2 - (self.lane_width * self.lanes // 2)) + lane * self.lane_width
            for y in range(0, self.road_height, self.line_length + self.line_spacing):
                self.lines.append((x, y))

    def update(self):
        for i in range(len(self.lines)):
            x, y = self.lines[i]
            y += self.speed
            if y > self.road_height - self.line_length:
                y = -self.line_length
            self.lines[i] = (x, y)

    def draw(self, road_surface):
        for x, y in self.lines:
            pygame.draw.line(road_surface, (255, 255, 255), (x, y), (x, y + self.line_length), 5)


class Target:
    def __init__(self, road_width, road_height, lanes, speed=3):
        self.images = ['img/car1.png', 'img/car2.png', 'img/car3.png']
        self.image = pygame.image.load(random.choice(self.images))
        self.road_width = road_width
        self.road_height = road_height
        self.x = random.randint(0, road_width - self.image.get_width())
        self.y = 0 - self.image.get_height()
        self.lanes = lanes
        self.speed = speed
        self.lane_width = self.road_width // self.lanes
        target_list.append(self)



    def update(self):
        self.y += self.speed
        if self.y > self.road_height:
            target_list.remove(self)

    def draw(self, field_surface):
        field_surface.blit(self.image, (self.x, self.y))


trees_list = []
target_list = []

def main():
    time = 60
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 650

    road_width, road_height = 400, 650
    lanes = 6  # Number of lanes on the road
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Race Game')
    icon = pygame.image.load("img/icon.jpg")
    pygame.display.set_icon(icon)

    field_surface = pygame.Surface((road_width, road_height))
    field_rect = field_surface.get_rect(topleft=(250, 0))

    clock = pygame.time.Clock()
    game_running = True
    road = Road(road_width, road_height)
    mycar = MyCar(road_width, road_height)

    while game_running:
        delta_time = clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False

        # Обработка нажатий клавиш
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            mycar.move_left()
        if keys[pygame.K_RIGHT]:
            mycar.move_right()

        screen.fill('DarkGreen')
        field_surface.fill('grey51')

        if time == 0:
            tree = Trees(SCREEN_WIDTH, SCREEN_HEIGHT)
            taeget = Target(SCREEN_WIDTH, SCREEN_HEIGHT, lanes)
            time = random.randint(10, 60)
        else:
            time -= 1

        for target in target_list:
            target.update()
        for trees in trees_list:
            trees.update()
        road.update()

        road.draw(field_surface)

        for trees in trees_list:
            trees.draw(screen)
        mycar.draw(field_surface)

        for target in target_list:
            target.draw(field_surface)

        screen.blit(field_surface, field_rect.topleft)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


main()
