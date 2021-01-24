import pygame
import sys
import os

pygame.init()
borders = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
GRAVITY = 9.8
heros = pygame.sprite.Group()

class Tiles(pygame.sprite.Sprite):
    def __init__(self, row, col):
        super().__init__(borders)
        image = pygame.image.load('data/tiles.jpg')
        self.image = image
        self.rect = image.get_rect()
        self.rect.x = col
        self.rect.y = row


class Character(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(heros)
        self.onGround = False
        
    def update(self, new_pos):
        border = pygame.sprite.spritecollideany(self, borders) 
        if border:
            self.onGround = True
        else:
            self.onGround = False
        if not self.onGround:
            new_pos.y += GRAVITY
        else:
            self.rect.y = border.rect.y - self.rect.height

        old_pos = self.rect
        self.rect = new_pos


def intro(screen):
    image = pygame.transform.scale((pygame.image.load('data\intro.jpg')), (screen.get_width() - 20, screen.get_height() - 20))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                return
        screen.fill((0, 0, 0))
        screen.blit(image, (10, 10))
        pygame.display.flip()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением {fullname} не найден!")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def loadLevel(filename):
    with open(filename) as map:
        level = [i.strip('\n') for i in map.readlines()]
    width_of_tile = width / len(level[0])
    height_of_tile = height / len(level)
    for rowind, row in enumerate(level):
        for colind, col in enumerate(row):
            if col == '@':
                Tiles(rowind * height_of_tile, colind * width_of_tile)


if __name__ == '__main__':
    step = 20
    size = width, height = 1366, 768
    screen = pygame.display.set_mode(size)
    FPS = 20
    clock = pygame.time.Clock()
    running = True
    image = pygame.transform.scale(load_image('Characters\Warrior\Base.png'), (200, 200))
    hero = Character()
    hero.image = image
    hero.rect = image.get_rect()
    new_pos = hero.rect
    intro(screen)
    print(id(hero.image.get_rect()) == id(new_pos))
    while running:
        new_pos = hero.rect
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if not hero.onGround:
                        new_pos.y -= step
                elif event.key == pygame.K_DOWN:
                    if not hero.onGround:
                        new_pos.y += step
                elif event.key == pygame.K_LEFT:
                	new_pos.x -= step
                elif event.key == pygame.K_RIGHT:
                	new_pos.x += step
                elif event.key == pygame.K_RETURN:
                    step += 1


        screen.fill((0, 0, 0))
        loadLevel('data/maps/level1')
        borders.draw(screen)


        all_sprites.update()
        all_sprites.draw(screen)

        
        heros.update(new_pos)
        heros.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)