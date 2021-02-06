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
enemy_group = pygame.sprite.Group()


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

        self.hp = 100

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

        self.status = True

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
        self.fall_sprites = self.frames[29:33]


    def update(self):
        if self.hp <= 0:
            font = pygame.font.SysFont('Comic Sans', 100)
            text = font.render('You are lose(r)!', False, (255, 0, 0))
            while self.hp <= 0:
                for ev in pygame.event.get():
                    if ev.type == pygame.KEYDOWN:
                        self.hp = 100
                        break
                screen.blit(text, (100, 100))
                pygame.display.flip()
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
                if self.cur_position == len(self.cur_state) - 1 and self.is_attack:
                    enemy = self.check_enemy()
                    if enemy:
                        enemy.get_damage(25)
                    self.is_attack = False
                    self.is_idle = True
                    self.one = True
                    return
                self.cur_position = (self.cur_position + 1) % len(self.cur_state)
                image = pygame.transform.scale(self.cur_state[self.cur_position], (100, 100))
                if self.orientation == 'Left':
                    image = pygame.transform.flip(image, 1, 0)
                self.image = image
                self.rect.w = 100
                self.rect.h = 100
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
            self.hp -= 1
        border_list = pygame.sprite.spritecollide(self, borders, False)
        if border_list:
            ground_y = 0
            for border in border_list:
                for point in range(self.rect.y, self.rect.y + self.rect.height):
                    if point in range(border.rect.y, border.rect.y + border.rect.height):
                        self.rect.y = abs(border.rect.y - self.rect.height) + 2
                        self.onGround = True
                        self.is_jump = False
                        break
                else:
                    self.rect.x = old_pos.x
                    self.rect.y = old_pos.y
                    self.velocityX = 0
                    print('Тут')
        else:
            self.onGround = False
            self.cur_state = self.fall_sprites


    def repaint(self):
        self.image.fill((0, 0, 0))

    def rotate_sprite(self, xbool, ybool):
        self.image = pygame.transform.flip(self.image, xbool, ybool)
    
    def check_enemy(self):
        return pygame.sprite.spritecollideany(self, enemy_group)

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



class Slime(pygame.sprite.Sprite):
    def __init__(self, sheet, rows, cols, row, col):
        super().__init__(all_sprites)

        enemy_group.add(self)

        self.orientation = 'Left'

        self.is_pursuit = False

        self.is_attack = False


        self.hp = 100

        self.velocityX = 2
        self.sheet = sheet
        self.rows = rows
        self.cols = cols
        self.frames = []
        self.count = 0       
        self.cur_pos = 0
        
        self.cur_state = None
        
        self.cut_sheets(sheet, rows, cols)
        
        self.image = pygame.transform.scale(self.cur_state[self.cur_pos], (50, 50))
        
        self.rect = self.image.get_rect()

        self.rect.x = col
        self.rect.y = row
        
        self.rect.w = 25
        self.rect.h = 25

    def cut_sheets(self, sheet, rows, cols):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // cols, sheet.get_height() // rows)
        for row in range(rows):
            for col in range(cols):
                frame_location = (self.rect.w * col, self.rect.h * row)
                image = sheet.subsurface(pygame.Rect(frame_location, self.rect.size))
                image.set_colorkey(image.get_at((0, 0)))
                self.frames.append(image)

        self.idle_frames = self.frames[:9]
        self.attack_frames = self.frames[8:14]
        self.die_frames = self.frames[16:21]
        self.cur_state = self.idle_frames

    def update(self):
        self.count += 1
        if self.hp <= 0 and not self.cur_state == self.die_frames:
            self.cur_state = self.die_frames 
            self.kill()
        if self.rect.x - hero.rect.x:
            if self.orientation == 'Left':
                if abs((self.rect.x + self.rect.w) - hero.rect.x) in range(0, 51):
                    self.is_attack = True
                    self.is_pursuit = False
                elif abs((self.rect.x + self.rect.w) - hero.rect.x) in range(51, 301):
                    self.is_attack = False
                    self.is_pursuit = True
            else:
                if abs(self.rect.x - (hero.rect.x + hero.rect.y)) in range(0, 51):
                    self.is_attack = True
                    self.is_pursuit = False
                elif abs(self.rect.x - (hero.rect.x + hero.rect.w)) in range(51, 301):
                    self.is_attack = False
                    self.is_pursuit = True
        if self.cur_state == self.die_frames:
            if self.count == 10:
                self.count = 0
                self.cur_pos = (self.cur_pos + 1) % len(self.cur_state)
            else:
                self.cur_pos % len(self.cur_state)
        else:
            self.cur_pos = (self.cur_pos + 1) % len(self.cur_state)
        image = pygame.transform.scale(self.cur_state[self.cur_pos], (50, 50))
        image.set_colorkey(image.get_at((0, 0)))
        if self.orientation == 'Right':
            image = pygame.transform.flip(image, 1, 0)
        self.image = image
        if self.is_pursuit:
            self.is_attack = False
            self.cur_state = self.idle_frames
            if self.rect.x < hero.rect.x:
                self.rect.x += self.velocityX
                self.orientation = 'Right'
            elif self.rect.x > hero.rect.x:
                self.rect.x -= self.velocityX
                self.orientation = 'Left'
        elif self.is_attack:
            if not self.cur_state == self.attack_frames:
                self.cur_state = self.attack_frames
            if self.cur_pos == len(self.cur_state) - 1:
                hero.hp -= 2
            
        if self.cur_pos == len(self.cur_state) - 1 and self.cur_state == self.die_frames:
            self.kill()
        


    def get_damage(self, damage):
        self.hp -= damage 
        self.hp = self.hp if self.hp >= 0 else 0

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
                Tile(load_image('Tiles\\bridge.png', (-1, -1)), rowind * height_of_tile, width_of_tile * colind)
            elif col == '%':
                slime = Slime(load_image('characters\slime-Sheet.png'), 3, 8, rowind * height_of_tile, width_of_tile * colind)
    return slime

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
    slime = loadLevel('data/maps/level1')
    background = Background(load_image('background.jpg'), screen)
    step = 100
    length_of_health_bar = 200
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
                        hero.orientation = 'Left'
                    if hero.onGround:
                        hero.is_idle = False
                        hero.is_run = True
                elif event.key == pygame.K_RIGHT:
                    if not hero.onWall:
                        directionToRight = True
                        hero.orientation = 'Right'
                    if hero.onGround:
                        hero.is_idle = False
                        hero.is_run = True
                elif event.key == pygame.K_RETURN:
                    hero.is_animated = False
                    hero.repaint()
                elif event.key == pygame.K_f:
                    hero.is_idle = False
                    hero.is_attack = True
                elif event.key == pygame.K_e:
                    hero.hp -= 15
                elif event.key == pygame.K_a:
                    slime.image = pygame.Surface((50, 50)).fill((255, 0, 0))

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
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(20, 20, length_of_health_bar * (hero.hp / 100), 20))



        pygame.display.flip()
        clock.tick(FPS)