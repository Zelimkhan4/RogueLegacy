import pygame
import sys
import os


First = 1
def animation_of_attack():
    if First <= 15:
        sprite.image = pygame.transform.scale(load_image(f'Attack_1\Picture ({First}).png', -1), (100, 200))
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
    all_sprites = pygame.sprite.Group()
    sprite = pygame.sprite.Sprite(all_sprites)
    sprite.image = image
    sprite.rect = image.get_rect()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    sprite.rect.y -= step
                elif event.key == pygame.K_DOWN:
                    sprite.rect.y += step
                elif event.key == pygame.K_RIGHT:
                    sprite.rect.x += step
                elif event.key == pygame.K_LEFT:
                    sprite.rect.x -= step
                elif event.key == pygame.K_RETURN:
                    step += 1
                elif event.key == pygame.K_f:
                    status = True
        screen.fill((0, 0, 0))
        if status:
            ans = animation_of_attack()
            if not ans:
                status = False
            First += 1
        else:
            First = 1
            sprite.image = image
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)