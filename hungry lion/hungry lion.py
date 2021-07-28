import pygame
import random
import sys

from pygame.pixelcopy import surface_to_array
from pygame.scrap import put

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


class Block(pygame.sprite.Sprite):

    def __init__(self, color, width, height):

        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        self.rect = self.image.get_rect()

    def reset_pos(self):

        self.rect.y = random.randrange(-300, -20)
        self.rect.x = random.randrange(0, screen_width)

    def update(self):

        self.rect.y += 1

        if self.rect.y > screen_height + self.rect.height:
            self.reset_pos()


class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.Surface([20, 15])
        self.image.fill(BLUE)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.change_x = 0
        self.change_y = 0

    def changespeed(self, x, y):
        self.change_x += x
        self.change_y += y

    def update(self):
        self.rect.x += self.change_x
        self.rect.y += self.change_y


pygame.init()


screen_width = 700
screen_height = 400
screen = pygame.display.set_mode([screen_width, screen_height])


block_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()

bad_block_list = pygame.sprite.Group()

for i in range(15):

    block = Block(GREEN, 20, 15)

    block.rect.x = random.randrange(screen_width)
    block.rect.y = random.randrange(screen_height)

    block_list.add(block)
    all_sprites_list.add(block)


for i in range(30):
    bad_block = Block(RED, 20, 15)
    bad_block.rect.x = random.randrange(screen_width)
    bad_block.rect.y = random.randrange(screen_height)

    bad_block_list.add(bad_block)
    all_sprites_list.add(bad_block)


player = Player(50, 50)
all_sprites_list.add(player)


done = False


clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)

score = 0

good_sound = pygame.mixer.Sound("19fef7f71648b21.mp3")
bad_sound = pygame.mixer.Sound("b5f0886abfa6621.mp3")

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.changespeed(-3, 0)
            elif event.key == pygame.K_RIGHT:
                player.changespeed(3, 0)
            elif event.key == pygame.K_UP:
                player.changespeed(0, -3)
            elif event.key == pygame.K_DOWN:
                player.changespeed(0, 3)

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.changespeed(3, 0)
            elif event.key == pygame.K_RIGHT:
                player.changespeed(-3, 0)
            elif event.key == pygame.K_UP:
                player.changespeed(0, 3)
            elif event.key == pygame.K_DOWN:
                player.changespeed(0, -3)

    screen.fill(WHITE)

    all_sprites_list.update()

    blocks_hit_list = pygame.sprite.spritecollide(player, block_list, False)

    blocks_hit_list2 = pygame.sprite.spritecollide(
        player, bad_block_list, False)

    for block in blocks_hit_list:
        score += 1
        print(score)
        good_sound.play()

    for block in blocks_hit_list2:
        score -= 1
        print(score)
        bad_sound.play()

    block.reset_pos()

    all_sprites_list.draw(screen)

    text = font.render("Score: "+str(score), True, BLACK)
    screen.blit(text, [10, 10])

    clock.tick(60)

    pygame.display.flip()

pygame.quit()
