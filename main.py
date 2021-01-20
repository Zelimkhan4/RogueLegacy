import pygame
import sys
import os

pygame.init()
borders = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2: # Вертикальная стенка
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)
        else:
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)

class Tiles(pygame.sprite.Sprite):
    def __init__(self, row, col):
        super().__init__(borders)
        image = pygame.image.load('data/tiles.jpg')
        self.image = image
        self.image.fill((0, 0, 0))
        self.rect = image.get_rect()
        self.rect.x = col
        self.rect.y = row

class Character(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)

    def update(self):
        if pygame.sprite.spritecollideany(self, borders) is None:
            self.rect.y += 5


def intro(screen):
    image = pygame.transform.scale((pygame.image.load('data\intro.jpg')), (screen.get_width() - 20, screen.get_height() - 20))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                return
        screen.blit(image, (10, 10))
        pygame.display.flip()

def load_image(name, colorkey=None):
    fullname = os.path.join('data\Knight\Right_Side\Warrior1', name)
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


def load_image1(name, colorkey=None):
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
    jump = 25
    status_of_jumping = 0
    rel = 0
    step = 1
    size = width, height = 600, 400
    screen = pygame.display.set_mode(size)
    FPS = 20
    clock = pygame.time.Clock()
    running = True
    image = pygame.transform.scale(load_image1('fire.jpg', -1), (100, 100))
    hero = Character()
    hero.image = image
    hero.rect = image.get_rect()
    intro(screen)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if pygame.sprite.spritecollideany(hero, borders) is None:
                        hero.rect.y -= step
                elif event.key == pygame.K_DOWN:
                    if pygame.sprite.spritecollideany(hero, borders) is None:
                        hero.rect.y += step
                elif event.key == pygame.K_RIGHT:
                    hero.rect.x += step
                elif event.key == pygame.K_LEFT:
                    hero.rect.x -= step
                elif event.key == pygame.K_RETURN:
                    step += 1
                elif event.key == pygame.K_SPACE:
                    status_of_jumping = True
            else:
                print(hero.rect.x, hero.rect.y)

        screen.fill((255, 255, 255))
        loadLevel('data/maps/level1')
        if status_of_jumping:
            if rel != jump:
                rel += 5
                hero.rect.y -= 5
            else:
                status_of_jumping = False
                rel = 0
        else:
            all_sprites.update()
        borders.draw(screen)
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)