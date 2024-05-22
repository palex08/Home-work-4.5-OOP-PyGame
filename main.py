import pygame
import sys
import random

class PlayerCar:
    def __init__(self, road_width, road_height, speed):
        self.image = pygame.image.load('img/mycar.png')
        self.road_width = road_width
        self.road_height = road_height
        self.x = 470 - self.image.get_width() // 2
        self.y = self.road_height - 150
        self.speed = speed
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def move_left(self):
        if self.x - self.speed >= 290:
            self.x -= self.speed
        self.rect.topleft = (self.x, self.y)

    def move_right(self):
        if self.x + self.speed <= 650 - self.image.get_width():
            self.x += self.speed
        self.rect.topleft = (self.x, self.y)


class Tree:
    def __init__(self, screen_width, screen_height, speed, trees_list):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.images = ['img/nature/tree1.png', 'img/nature/tree2.png', 'img/nature/tree3.png']
        self.image = pygame.image.load(random.choice(self.images))
        self.speed = speed
        self.side_tree = random.choice([(0, self.screen_width - 1030),
                                        (self.screen_width - 500, self.screen_width - 300)])
        self.x = random.randint(self.side_tree[0], self.side_tree[1])
        self.y = 0 - self.image.get_height()
        self.trees_list = trees_list
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.trees_list.append(self)

    def update(self):
        self.y += self.speed
        self.rect.topleft = (self.x, self.y)
        if self.y > self.screen_height:
            self.trees_list.remove(self)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


class Road:
    def __init__(self, screen_width, screen_height, speed=6):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.road_image = pygame.image.load("img/road.png")
        self.x = 250
        self.y = 0
        self.speed = speed

    def update(self):
        self.y += self.speed
        if self.y + self.road_image.get_height() > self.screen_height:
            self.y = -self.road_image.get_height()

    def draw(self, screen):
        screen.blit(self.road_image, (self.x, self.y))
        screen.blit(self.road_image, (self.x, self.y + self.road_image.get_height()))


class Target:
    def __init__(self, screen_width, screen_height, player_car, target_list):
        self.player_car = player_car
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.images = ['img/targets/car1.png', 'img/targets/car2.png', 'img/targets/car3.png',
                       'img/targets/car4.png', 'img/targets/car5.png', 'img/targets/car6.png',
                       'img/targets/car7.png', 'img/targets/car8.png', 'img/targets/car9.png']
        self.image = pygame.image.load(random.choice(self.images))
        self.x = random.choice([310, 400, 490, 585])
        self.y = 0 - self.image.get_height()
        self.speed = random.randint(3, 6)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.target_list = target_list
        self.target_list.append(self)

    def update(self):
        self.y += self.speed
        self.rect.topleft = (self.x, self.y)
        self.check_collision_with_others()
        if self.y > self.screen_height:
            self.target_list.remove(self)
        if self.rect.colliderect(self.player_car.rect):
            self.target_list.remove(self)
            return True
        return False

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def check_collision_with_others(self):
        for target in self.target_list:
            if target != self and self.rect.colliderect(target.rect):
                self.speed = 3
                target.speed = 4


class Game:
    def __init__(self):
        self.SCREEN_WIDTH = 1200
        self.SCREEN_HEIGHT = 650
        self.speed = 6
        self.road_width, self.road_height = 446, 650
        self.target_list = []
        self.trees_list = []
        self.target_time = 60
        self.tree_time = 60
        self.distance_traveled = 0
        self.lives = 5

        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption('Race Game')
        icon = pygame.image.load("img/icon.jpg")
        pygame.display.set_icon(icon)

        self.side_bar = pygame.Surface((self.SCREEN_WIDTH - 970, self.SCREEN_HEIGHT))
        self.side_bar.fill((255, 255, 255))
        self.font = pygame.font.Font(None, 24)

        self.clock = pygame.time.Clock()
        self.road = Road(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.speed)
        self.player_car = PlayerCar(self.road_width, self.road_height, self.speed)

    def can_spawn_target(self, x):
        return sum(1 for target in self.target_list if target.x == x and target.y < 300) < 1

    def run(self):
        game_running = True
        while game_running:
            delta_time = self.clock.tick(30)
            self.distance_traveled += self.speed * delta_time / 1000  # Update distance

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False
                if event.type == pygame.MOUSEBUTTONUP:
                    print(pygame.mouse.get_pos())

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player_car.move_left()
            if keys[pygame.K_RIGHT]:
                self.player_car.move_right()
            if keys[pygame.K_UP]:
                if self.speed < 10:
                    self.road.speed += 1
                    for target in self.target_list:
                        target.speed += 1
                    for tree in self.trees_list:
                        tree.speed += 1
                    self.speed += 1
            if keys[pygame.K_DOWN]:
                if self.speed > 7:
                    self.road.speed = max(2, self.road.speed - 1)
                    for target in self.target_list:
                        target.speed -= 1
                    for tree in self.trees_list:
                        tree.speed = max(2, tree.speed - 1)
                    self.speed -= 1

            self.screen.fill('DarkGreen')
            self.screen.blit(self.side_bar, (970, 0))
            self.side_bar.fill((0, 0, 0))

            if self.tree_time == 0:
                Tree(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.speed, self.trees_list)
                self.tree_time = random.randint(30, 60)
            else:
                self.tree_time -= 1

            if self.target_time == 0:
                possible_x_positions = [310, 400, 490, 585]
                random.shuffle(possible_x_positions)
                for x in possible_x_positions:
                    if self.can_spawn_target(x):
                        target = Target(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.player_car, self.target_list)
                        target.x = x
                        target.rect.topleft = (target.x, target.y)
                        break
                self.target_time = random.randint(30, 60)
            else:
                self.target_time -= 1

            self.road.update()
            self.road.draw(self.screen)

            for target in self.target_list:
                if target.update():
                    self.lives -= 1
                target.draw(self.screen)

            for tree in self.trees_list:
                tree.update()
                tree.draw(self.screen)

            self.player_car.draw(self.screen)

            # Update and draw sidebar
            distance_miles = self.distance_traveled / 1000  # Convert pixels to miles
            distance_text = self.font.render(f"Distance: {distance_miles:.2f} miles", True, (255, 255, 255))
            lives_text = self.font.render(f"Lives: {self.lives}", True, (255, 255, 255))
            self.side_bar.blit(distance_text, (20, 20))
            self.side_bar.blit(lives_text, (20, 60))

            if self.lives <= 0:
                game_running = False
                game_over_text = self.font.render("GAME OVER", True, (255, 0, 0))
                self.screen.blit(game_over_text, (self.SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, self.SCREEN_HEIGHT // 2))
                pygame.display.update()
                pygame.time.wait(3000)

            pygame.display.update()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    Game().run()


