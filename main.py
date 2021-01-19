import pygame
import sys
import os

pygame.init()
vertical_borders = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
status_of_moving = True
class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2: # Вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)


class Character(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)

    def update(self):
        global status_of_moving
        if not pygame.sprite.spritecollideany(hero, horizontal_borders) or not pygame.sprite.spritecollideany(hero, vertical_borders):
            status_of_moving = False
        else:
            status_of_moving = True

        print(status_of_moving)

        
def intro(screen):
    image = pygame.transform.scale((pygame.image.load('data\intro.jpg')), (screen.get_width() - 20, screen.get_height() - 20))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                return
        screen.blit(image, (10, 10))
        pygame.display.flip()

def animation_of_attack():
    if First <= 15:
        hero.image = pygame.transform.scale(load_image(f'Attack_1\Picture ({First}).png', -1), (100, 200))
        return True
    else:
        return False


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


if __name__ == '__main__':
    step = 1
    size = width, height = 600, 400
    screen = pygame.display.set_mode(size)
    FPS = 15
    status = False
    clock = pygame.time.Clock()
    running = True
    image = pygame.transform.scale(load_image('Normal.png', -1), (100, 200))
    hero = pygame.sprite.Sprite(all_sprites)
    hero.image = image
    hero.rect = image.get_rect()
    hor_1 = Border(5, 5, width - 5, 5)
    hor2 = Border(5, height - 5, width - 5, height - 5)
    vert1 = Border(5, 5, 5, height - 5)
    vert2 = Border(width - 5, 5, width - 5, height - 5)
    intro(screen)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                print('Столкновение сейчас:', pygame.sprite.spritecollideany(hero, horizontal_borders))
                if status_of_moving:
                    if event.key == pygame.K_UP:
                        if pygame.sprite.spritecollideany(hero, horizontal_borders) is None:
                            hero.rect.y -= step
                    elif event.key == pygame.K_DOWN:
                        hero.rect.y += step
                    elif event.key == pygame.K_RIGHT:
                        hero.rect.x += step
                    elif event.key == pygame.K_LEFT:
                        hero.rect.x -= step
                    elif event.key == pygame.K_RETURN:
                        step += 1
                    elif event.key == pygame.K_f:
                        status = True
        screen.fill((255, 0, 0))
        if status:
            ans = animation_of_attack()
            if not ans:
                status = False
            First += 1
        else:
            First = 1
            hero.image = image
        all_sprites.draw(screen)
        all_sprites.update()
        horizontal_borders.draw(screen)
        vertical_borders.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)