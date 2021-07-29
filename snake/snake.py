import pygame
import random
import time

pygame.init()

WIDTH = 800
HEIGHT = 600

FPS = 30
clock = pygame.time.Clock()

font = pygame.font.SysFont('comicsansms', 25)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('snake game')

wall_image = pygame.image.load('wall2.jpg')


class Snake:

    def __init__(self, x, y):
        self.size = 1
        self.elements = [[x, y]]
        self.radius = 10
        self.dx = 5
        self.dy = 0
        self.is_add = False
        self.speed = 10
        self.score = 0

    def draw(self):
        for element in self.elements:
            pygame.draw.circle(screen, (214, 0, 0), element, self.radius)

    def add_to_snake(self):
        self.size += 1
        self.elements.append([0, 0])
        self.is_add = False
        self.score += 1
        if self.score % 3 == 0:
            self.speed += 5

    def move(self):
        if self.is_add:
            self.add_to_snake()
        for i in range(self.size - 1, 0, -1):
            self.elements[i][0] = self.elements[i - 1][0]
            self.elements[i][1] = self.elements[i - 1][1]

        self.elements[0][0] += self.dx
        self.elements[0][1] += self.dy


class Food:

    def __init__(self):
        self.x = random.randint(100, WIDTH - 70)
        self.y = random.randint(100, HEIGHT - 70)
        self.image = pygame.image.load('apple.jpg')

    def gen(self):
        self.x = random.randint(100, WIDTH - 70)
        self.y = random.randint(100, HEIGHT - 70)

    def draw(self):
        screen.blit(self.image, (self.x, self.y))


def walls():
    for i in range(0, WIDTH, 15):
        screen.blit(wall_image, (i, 0))
        screen.blit(wall_image, (i, HEIGHT - 20))
        screen.blit(wall_image, (0, i))
        screen.blit(wall_image, (WIDTH - 20, i))


def collision():
    if(food.x in range(snake1.elements[0][0] - 20, snake1.elements[0][0])) and (food.y in range(snake1.elements[0][1] - 20, snake1.elements[0][1])):
        snake1.is_add = True
        food.gen()


def collision2():
    if(food.x in range(snake2.elements[0][0] - 20, snake2.elements[0][0])) and (food.y in range(snake2.elements[0][1] - 20, snake2.elements[0][1])):
        snake2.is_add = True
        food.gen()


def is_in_walls():
    return snake1.elements[0][0] > WIDTH - 30 or snake1.elements[0][0] < 30 or snake1.elements[0][1] > HEIGHT - 30 or snake1.elements[0][1] < 30


def is_in_walls_2():
    return snake2.elements[0][0] > WIDTH - 25 or snake2.elements[0][0] < 30 or snake2.elements[0][1] > HEIGHT - 30 or snake2.elements[0][1] < 30


def scores(x, y, score):
    score_body = font.render('Score: ' + str(score), True, (235, 239, 141))
    screen.blit(score_body, (x, y))


def new_walls():
    if (snake1.score % 5 == 0 and snake1.score > 0) or (snake2.score % 5 == 0 and snake2.score > 0):
        a = 150
        b = 400
        for i in range(a, b, 15):
            screen.blit(wall_image, (i, 200))


def new_walls_col():
    return 150 < snake1.elements[0][0] < 400 and 200 < snake1.elements[0][1] < 232


def new_walls_col_2():
    return 150 < snake2.elements[0][0] < 400 and 200 < snake2.elements[0][1] < 232


def game_over():
    f = open("snakescores.txt", "a")
    f.write("1st player: " + str(snake1.score) +
            ", 2nd player: " + str(snake2.score))
    f.close()
    screen.fill((255, 0, 0))
    txt = font.render('GAME OVER!', True, (255, 255, 255))
    score1 = font.render(
        'Total score: ' + str(snake1.score), True, (255, 255, 255))
    score2 = font.render(
        'Total score: ' + str(snake2.score), True, (255, 255, 255))
    screen.blit(txt, (200, 200))
    screen.blit(score1, (200, 300))
    screen.blit(score2, (200, 350))
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()


snake1 = Snake(100, 100)
snake2 = Snake(100, 150)
food = Food()
d = 5

running = True

while running:
    clock.tick(snake1.speed)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_RIGHT and snake1.dx != -d:
                snake1.dx = d
                snake1.dy = 0
            if event.key == pygame.K_LEFT and snake1.dx != d:
                snake1.dx = -d
                snake1.dy = 0
            if event.key == pygame.K_UP and snake1.dy != d:
                snake1.dx = 0
                snake1.dy = -d
            if event.key == pygame.K_DOWN and snake1.dy != -d:
                snake1.dx = 0
                snake1.dy = d

            if event.key == pygame.K_d and snake2.dx != -d:
                snake2.dx = d
                snake2.dy = 0
            if event.key == pygame.K_a and snake2.dx != d:
                snake2.dx = -d
                snake2.dy = 0
            if event.key == pygame.K_w and snake2.dy != d:
                snake2.dx = 0
                snake2.dy = -d
            if event.key == pygame.K_s and snake2.dy != -d:
                snake2.dx = 0
                snake2.dy = d

    if is_in_walls() or is_in_walls_2():
        game_over()
        running = False

    if (snake1.score > 0 and snake1.score % 5 == 0) or (snake2.score > 0 and snake2.score % 5 == 0):
        if new_walls_col() or new_walls_col_2():
            game_over()
            running = False

    collision()
    collision2()
    snake1.move()
    snake2.move()
    screen.fill((122, 147, 148))
    snake1.draw()
    snake2.draw()
    walls()
    new_walls()
    food.draw()

    scores(40, 35, snake1.score)
    scores(40, 60, snake2.score)

    pygame.display.flip()

pygame.quit()
