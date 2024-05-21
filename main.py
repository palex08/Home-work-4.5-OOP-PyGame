import pygame
import sys
import random


class MyCar:
    def __init__(self, road_width, road_height, speed=6):
        self.image = pygame.image.load('img/mycar.png')
        self.road_width = road_width
        self.road_height = road_height
        self.x = 470 - self.image.get_width() // 2
        self.y = self.road_height - 150
        self.speed = speed  # Скорость перемещения машины

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def move_left(self):
        if self.x - self.speed >= 290:
            self.x -= self.speed

    def move_right(self):
        if self.x + self.speed <= 650 - self.image.get_width():
            self.x += self.speed


class Trees:
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, speed=6):
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.image = pygame.image.load('img/tree.png')
        self.speed = speed
        self.side_tree = random.choice([(0, self.SCREEN_WIDTH - 1030),
                                        (self.SCREEN_WIDTH - 500, self.SCREEN_WIDTH - 300)])
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
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, speed=6):
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.road_image = pygame.image.load("img/road.png")
        self.x = 250
        self.y = 0
        self.speed = speed

    def update(self):
        self.y += self.speed
        if self.y + self.road_image.get_height() > self.SCREEN_HEIGHT:
            self.y = -self.road_image.get_height()

    def draw(self, screen):
        screen.blit(self.road_image, (self.x, self.y))
        screen.blit(self.road_image, (self.x, self.y + self.road_image.get_height()))


class Target:
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.images = ['img/car1.png', 'img/car2.png', 'img/car3.png']
        self.image = pygame.image.load(random.choice(self.images))
        self.x = random.choice([310, 400, 490, 585])
        self.y = 0 - self.image.get_height()
        self.speed = random.randint(2, 5)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        target_list.append(self)

    def update(self):
        self.y += self.speed
        self.rect.topleft = (self.x, self.y)
        if self.y > self.SCREEN_HEIGHT:
            target_list.remove(self)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def check_collision(self, other):
        return self.rect.colliderect(other.rect)


trees_list = []
target_list = []


def main():
    target_time = 60
    tree_time = 60
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 650

    road_width, road_height = 446, 650
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Race Game')
    icon = pygame.image.load("img/icon.jpg")
    pygame.display.set_icon(icon)

    clock = pygame.time.Clock()
    game_running = True
    road = Road(SCREEN_WIDTH, SCREEN_HEIGHT)
    mycar = MyCar(road_width, road_height)

    def can_spawn_target(x):
        count = sum(1 for target in target_list if target.x == x and target.y < 300)
        return count < 1

    while game_running:
        delta_time = clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
            if event.type == pygame.MOUSEBUTTONUP:
                print(pygame.mouse.get_pos())

        # Обработка нажатий клавиш
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            mycar.move_left()
        if keys[pygame.K_RIGHT]:
            mycar.move_right()

        screen.fill('DarkGreen')

        if tree_time == 0:
            tree = Trees(SCREEN_WIDTH, SCREEN_HEIGHT)
            tree_time = random.randint(10, 60)
        else:
            tree_time -= 1

        if target_time == 0:
            possible_x_positions = [310, 400, 490, 585]
            random.shuffle(possible_x_positions)
            for x in possible_x_positions:
                if can_spawn_target(x):
                    target = Target(SCREEN_WIDTH, SCREEN_HEIGHT)
                    target.x = x
                    target.rect.topleft = (target.x, target.y)
                    break
            target_time = random.randint(30, 60)
        else:
            target_time -= 1

        road.update()
        road.draw(screen)

        for target in target_list:
            target.update()
            target.draw(screen)

        for i in range(len(target_list)):
            for j in range(i + 1, len(target_list)):
                if target_list[i].check_collision(target_list[j]):
                    target_list[i].speed = 4
                    target_list[j].speed = 3

        for trees in trees_list:
            trees.update()
            trees.draw(screen)

        mycar.draw(screen)

        pygame.display.update()

    pygame.quit()
    sys.exit()


main()
