import pygame
import sys
import os

class Borders(pygame.sprite.Group):
    def repaint(self):
        for sprite in self.sprites():
            sprite.image.fill((255, 255, 255))
pygame.init()
borders = Borders()
all_sprites = pygame.sprite.Group()
GRAVITY = 10
heros = pygame.sprite.Group()

class Tiles(pygame.sprite.Sprite):
    def __init__(self, row, col):
        super().__init__(borders)
        image = pygame.image.load('data/tiles.jpg')
        self.image = image
        self.rect = image.get_rect()
        self.rect.x = col
        self.rect.y = row
        self.image.fill((0, 0, 0))

    def repaint(self):
        self.image.fill((0, 0, 0))

class Controller:
    def __init__(self, sprite):
        self.sprite = sprite
        self.velocity_x = 10
        self.velocity_Y = GRAVITY

class Character(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(heros)
        self.onGround = False
        self.onWall = False
        
    def update(self, new_pos):
        old_pos = self.rect.copy()
        self.rect = new_pos
        borderes = pygame.sprite.spritecollide(self, borders, False)
        self.onGround = False

        if borderes:
            if new_pos.y - old_pos.y > 0:
                dir_horizontal = 'right'
            if new_pos.y - old_pos.y < 0:
                dir_horizontal = 'left'
            ground_y = 0
            for border in borderes:
                if border.rect.y <= self.rect.y + self.rect.height and\
                        self.rect.x + self.rect.width // 2 in range(border.rect.x, border.rect.x + border.rect.width):
                    border.image.fill((0, 255, 0))
                    #print('пол')
                    self.rect.y = border.rect.y - self.rect.height + 1
                    self.onGround = True
                    ground_y = border.rect.y
                if not border.rect.y <= self.rect.y + self.rect.height and\
                         ground_y != self.rect.y:
                    self.rect.x = old_pos.x
                    self.rect.y = border.rect.y - self.rect.height + 1
                    border.image.fill((255, 0, 0))
                    #print('стена')
                else:
                    border.image.fill((0, 255, 0))
                    self.rect.y = border.rect.y - self.rect.height + 1

def intro(screen):
    image = pygame.transform.scale((pygame.image.load('data/intro.jpg')), (screen.get_width() - 20, screen.get_height() - 20))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
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
    size = width, height = 1000, 600
    screen = pygame.display.set_mode(size)
    FPS = 30
    clock = pygame.time.Clock()
    running = True
    image = pygame.transform.scale(load_image('Characters/Warrior/Base.png'), (200, 200))
    hero = Character()
    hero.image = image
    hero.rect = image.get_rect()
    new_pos = hero.rect
    intro(screen)
    loadLevel('data/maps/level1')
    while running:
        new_pos = hero.rect.copy()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    new_pos.y -= 100
                if event.key == pygame.K_DOWN:
                    if not hero.onGround:
                        new_pos.y += step                    
                elif event.key == pygame.K_LEFT:
                    if not hero.onWall:
                        new_pos.x -= step
                elif event.key == pygame.K_RIGHT:
                    if not hero.onWall:
                        new_pos.x += step
                elif event.key == pygame.K_SPACE:
                    copy = new_pos.copy()
                    copy.y = new_pos.y - 100
                    hero.rect = copy.y
                elif event.key == pygame.K_RETURN:
                    step += 1
                    box = pygame.Surface((200, 200))
                    hero.image = box
                    hero.image.fill((0, 0, 255))
                    hero.rect.width, hero.rect.height = box.get_rect().width, box.get_rect().height
                elif event.key == pygame.K_BACKSPACE:
                    hero.image = image
        screen.fill((0, 0, 0))

        borders.draw(screen)
        borders.update()
        if not hero.onGround:
            new_pos.y += GRAVITY
        all_sprites.update()
        all_sprites.draw(screen)

        borders.repaint()
        heros.update(new_pos)
        heros.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)