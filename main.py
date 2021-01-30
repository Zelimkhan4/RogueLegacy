import pygame
import sys
import os

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


if __name__ == '__main__':
    step = 1
    size = width, height = 600, 400
    screen = pygame.display.set_mode(size)
    FPS = 60
    clock = pygame.time.Clock()
    running = True
    image = pygame.transform.scale(load_image('knight.png', -1), (100, 100))
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
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick()
print(4)