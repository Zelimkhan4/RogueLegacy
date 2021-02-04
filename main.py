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
GRAVITY = 500
heros = pygame.sprite.Group()
coordinate_of_back = 0
trap_group = pygame.sprite.Group()


class Trap(pygame.sprite.Sprite):
    def __init__(self, image, row, col, width, height):
        super().__init__(trap_group)
        all_sprites.add(self)
        self.image = pygame.transform.scale(image, (50, 50))
        self.rect = image.get_rect()
        self.rect.x = col
        self.rect.y = row



class Background(pygame.Surface):
    def __init__(self, image, screen):
        self.image = pygame.transform.scale(image, (image.get_width(), screen.get_height()))
        self.coordinate_of_back = [0, 0]

    def move(self, value):
        self.coordinate_of_back[0] += value

    def update(self, screen):
        screen.blit(self.image, tuple(self.coordinate_of_back))

class Camera:
    def __init__(self):
        self.dx = 0

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.width // 2 - width // 2)

    def apply(self, obj):
        obj.rect.x += self.dx


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


class Tile(pygame.sprite.Sprite):
    def __init__(self, image, row, col):
        super().__init__(borders)
        all_sprites.add(self)
        self.image = pygame.transform.scale(image, (100, height_of_tile))
        self.rect = image.get_rect()
        self.rect.x = col
        self.rect.y = row


class Ground(pygame.sprite.Sprite):
    def __init__(self, row, col, width_of_tile, height_of_tile):
        super().__init__(borders)
        all_sprites.add(self)
        image = pygame.transform.scale(pygame.image.load('data/Tiles/Tileset/Ground.png'), (width_of_tile, height_of_tile))
        self.image = image
        self.rect = image.get_rect()
        self.rect.x = col
        self.rect.y = row


class GrassUp(pygame.sprite.Sprite):
    def __init__(self, row, col, width_of_tile, height_of_tile):
        super().__init__(borders)
        all_sprites.add(self)
        image = pygame.transform.scale(load_image('Tiles/Tileset/GrassUp.png'), (width_of_tile, height_of_tile))
        self.image = image
        self.rect = image.get_rect()
        self.rect.x = col
        self.rect.y = row


class GrassLeftSide(pygame.sprite.Sprite):
    def __init__(self, row, col, width_of_tile, height_of_tile):
        super().__init__(borders)
        all_sprites.add(self)
        image = pygame.transform.scale(load_image('Tiles/Tileset/GrassLeftSide.png'), (width_of_tile, height_of_tile))
        self.image = image
        self.rect = image.get_rect()
        self.rect.x = col
        self.rect.y = row


class Character(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows):
        super().__init__(heros)
        all_sprites.add(self)
        self.orientation = 'Right'

        self.is_animated = True

        self.onGround = False
        self.onWall = False
        self.velocityX = 0
        self.velocityY = GRAVITY // FPS

        self.frames = []
        self.cut_frames(sheet, columns, rows)


        self.is_idle = True
        self.is_run = False
        self.is_attack = False
        self.is_jump = False


        self.cur_position = 0
        self.one = True
        self.update()


    def cut_frames(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))
        self.idle_sprites = self.frames[:4]
        self.attack_sprites = self.frames[38:60]
        self.run_sprites = self.frames[9:15]
        self.jump_sprites = self.frames[34:40]
        self.fall_sprites = self.frames[23:25]


    def update(self):
        copy = self.rect.copy()
        self.move_horizontal()
        self.move_vertical()
        self.velocityX = 0
        self.velocityY = 0
        self.checkCollision(copy)
        if self.is_animated:
            if self.is_jump:
                self.cur_state = self.jump_sprites
            elif not self.onGround:
                self.cur_state = self.fall_sprites
            elif self.is_idle:
                self.cur_state = self.idle_sprites
            elif self.is_run:
                self.cur_state = self.run_sprites
            elif self.is_jump:
                self.cur_state = self.jump_sprites
            elif self.is_attack:
                self.cur_state = self.attack_sprites
            if self.one:
                self.cur_position = (self.cur_position + 1) % len(self.cur_state)
                self.image = pygame.transform.scale(self.cur_state[self.cur_position], (75, 100))
                self.rect.w = self.image.get_rect().width
                self.rect.h = self.image.get_rect().height
                self.one = False
            self.one = False
        self.one = True

    def move_horizontal(self):
        global coordinate_of_back
        self.rect.x += self.velocityX

    def move_vertical(self):
        self.rect.y += self.velocityY

    def checkCollision(self, old_pos):
        if pygame.sprite.spritecollideany(self, trap_group):
            print("Вы умерли")
            exit()
        border_list = pygame.sprite.spritecollide(self, borders, False)
        print(len(border_list))
        if border_list:
            ground_y = 0
            for border in border_list:
                for point in range(self.rect.y, self.rect.y + self.rect.height):
                    if point in range(border.rect.y, border.rect.y + border.rect.height):
                        self.rect.y = abs(border.rect.y - self.rect.height) + 2
                        self.onGround = True
                        ground_y = border.rect.y
                        self.is_jump = False
                        break
                else:
                    self.rect.x = old_pos.x
                    self.velocityX = 0
        else:
            self.onGround = False
            self.cur_state = self.fall_sprites


    def repaint(self):
        self.image.fill((0, 0, 0))

    def rotate_sprite(self, xbool, ybool):
        self.image = pygame.transform.flip(self.image, xbool, ybool)

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
            elif col == '_':
                Trap(load_image('Tiles\lava_tile1.png'), rowind * height_of_tile, colind * width_of_tile, width_of_tile, height_of_tile)
            elif col == '+':
                Trap(load_image('Tiles\lava_tile4.png'), rowind * height_of_tile, colind * width_of_tile, width_of_tile, height_of_tile)
            elif col == '-':
                Tile(load_image('bridge.png'), rowind * height_of_tile, width_of_tile * colind)




if __name__ == '__main__':
    coordinate = 0

    directionToRight = False
    directionToLeft = False

    camera = Camera()
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    FPS = 15
    clock = pygame.time.Clock()
    running = True
    image = load_image('Tiles\Adventurer-1.3-Sheet.png')
    hero = Character(image, 8, 12)
    width_of_tile = 50
    height_of_tile = 50
    intro(screen)
    loadLevel('data/maps/level1')
    background = Background(load_image('background.jpg'), screen)
    step = 100
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if hero.onGround:
                        hero.move_vertical()
                        hero.onGround = False
                elif event.key == pygame.K_SPACE:
                    hero.velocityY = -100
                    hero.is_jump = True
                elif event.key == pygame.K_LEFT:
                    if not hero.onWall:
                        directionToLeft = True
                    if hero.orientation == 'Right':
                        hero.image = pygame.transform.flip(hero.image, 1, 0)
                        hero.orientation = 'Left'
                    if hero.onGround:
                        hero.is_idle = False
                        hero.is_run = True
                elif event.key == pygame.K_RIGHT:
                    if not hero.onWall:
                        directionToRight = True
                    if hero.orientation == 'Left':
                        hero.image = pygame.transform.flip(hero.image, 1, 0)
                        hero.orientation = 'Right'
                    if hero.onGround:
                        hero.is_idle = False
                        hero.is_run = True
                elif event.key == pygame.K_RETURN:
                    hero.is_animated = False
                    hero.repaint()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    if not hero.onWall:
                        directionToLeft = False
                    hero.is_idle = True
                    hero.is_run = False

                elif event.key == pygame.K_RIGHT:
                    if not hero.onWall:
                        directionToRight = False
                    hero.is_idle = True
                    hero.is_run = False

        screen.fill((0, 0, 0))
        background.update(screen)
        camera.update(hero)
        for sprite in all_sprites:
            camera.apply(sprite)
        all_sprites.update()
        all_sprites.draw(screen)
        if not hero.onGround:
            hero.velocityY = (GRAVITY) / FPS
        if directionToRight:
            hero.velocityX = (step) / FPS
        if directionToLeft:
            hero.velocityX = -((step) / FPS)



        pygame.display.flip()
        clock.tick(FPS)