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
coordinate_of_back = 0


class Camera:
    def __init__(self):
        self.dx = 0

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.width // 2 - width // 2)

    def apply(self, obj):
        obj.rect.x += self.dx
        print(obj.rect)

def load_image(name, colorkey=None):
    fullname = 'data\\' + name
    if not os.path.isfile(fullname):
        print(f"Файл с изображением {fullname} не найден!")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        else:
            if type(colorkey) == tuple:
                if colorkey == (-1, -1):
                    colorkey = image.get_at((image.get_rect().width - 1, image.get_rect().height - 1))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image



class Ground(pygame.sprite.Sprite):
    def __init__(self, row, col, width_of_tile, height_of_tile):
        super().__init__(borders)
        image = pygame.transform.scale(pygame.image.load('data/Tiles/Tileset/Ground.png'), (width_of_tile, height_of_tile))
        self.image = image
        self.rect = image.get_rect()
        self.rect.x = col
        self.rect.y = row

class GrassUp(pygame.sprite.Sprite):
    def __init__(self, row, col, width_of_tile, height_of_tile):
        super().__init__(borders)
        image = pygame.transform.scale(load_image('Tiles/Tileset/GrassUp.png'), (width_of_tile, height_of_tile))
        self.image = image
        self.rect = image.get_rect()
        self.rect.x = col
        self.rect.y = row
    
class GrassLeftSide(pygame.sprite.Sprite):
    def __init__(self, row, col, width_of_tile, height_of_tile):
        super().__init__(borders)
        image = pygame.transform.scale(load_image('Tiles/Tileset/GrassLeftSide.png'), (width_of_tile, height_of_tile))
        self.image = image
        self.rect = image.get_rect()
        self.rect.x = col
        self.rect.y = row

class Character(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__(heros)
        self.onGround = False
        self.onWall = False
        self.velocityX = 0
        self.velocityY = GRAVITY // FPS
        self.image = pygame.transform.scale(image, (50, 50))
        self.rect = pygame.Rect(width // 2 - self.image.get_width() // 2, height // 2 - self.image.get_height() // 2, 100, 100)

    def update(self):
        copy = self.rect.copy()
        self.move_horizontal()
        self.move_vertical()
        self.velocityX = 0
        self.velocityY = 0
        self.checkCollision(copy)

    def move_horizontal(self):
        global coordinate_of_back
        self.rect.x += self.velocityX
        coordinate_of_back -= self.velocityX

    def move_vertical(self):
        self.rect.y += self.velocityY

    def repaint(self):
        self.image.fill((255, 0, 0))

    def checkCollision(self, old_pos):
        border_list = pygame.sprite.spritecollide(self, borders, False)
        if border_list:
            ground_y = 0
            for border in border_list:
                if self.rect.y + self.rect.height in range(border.rect.y, border.rect.y + border.rect.height):
                    self.rect.y = abs(border.rect.y - self.rect.height)
                    self.onGround = True
                    ground_y = border.rect.y
                else:
                    self.rect.x = old_pos.x
        else:
            self.onGround = False



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





def loadLevel(filename):
    with open(filename) as map:
        level = [i.strip('\n') for i in map.readlines()]
    for rowind, row in enumerate(level):
        for colind, col in enumerate(row):
            if col == '@':
                Ground(rowind * height_of_tile, colind * width_of_tile, width_of_tile, height_of_tile)
            elif col == '^':
                GrassUp(rowind * height_of_tile, colind * width_of_tile, width_of_tile, height_of_tile)
            elif col == '<':
                GrassLeftSide(rowind * height_of_tile, colind * width_of_tile, width_of_tile, height_of_tile)

if __name__ == '__main__':
    coordinate = 0

    directionToRight = False
    directionToLeft = False

    camera = Camera()
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    FPS = 30
    clock = pygame.time.Clock()
    running = True
    image = pygame.transform.scale(load_image('Characters/Warrior/Base.png'), (200, 200))
    hero = Character(image)
    width_of_tile = 50
    height_of_tile = 50
    intro(screen)
    loadLevel('data/maps/level1')
    step = 300
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if hero.onGround:
                        hero.move_vertical()
                        hero.onGround = False
                elif event.key == pygame.K_LEFT:
                    if not hero.onWall:
                        directionToLeft = True
                elif event.key == pygame.K_RIGHT:
                    if not hero.onWall:
                        directionToRight = True
                elif event.key == pygame.K_RETURN:
                    hero.repaint()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    if not hero.onWall:
                        directionToLeft = False
                elif event.key == pygame.K_RIGHT:
                    if not hero.onWall:
                        directionToRight = False
        screen.fill((0, 0, 0))
        screen.blit(pygame.transform.scale(load_image('fon.jpg'), (screen.get_width(), screen.get_height())), (0, 0))
        borders.draw(screen)
        borders.update()
        if not hero.onGround:
            hero.velocityY = (step + 100) / FPS
        if directionToRight:
            hero.velocityX = (step + 100) / FPS
        if directionToLeft:
            hero.velocityX = -((step + 100) / FPS)
        heros.update()
        camera.update(hero)
        for sprite in borders:
            camera.apply(sprite)
        camera.apply(hero)
        all_sprites.update()
        all_sprites.draw(screen)
        heros.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)