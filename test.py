import pygame
import sys
from PIL import Image


# pygame.init()
# count = 0
# all_sprites = pygame.sprite.Group()
# my_sprite = pygame.sprite.Sprite(all_sprites)
# briedge = pygame.image.load('data/Tiles/bridge.png')
# my_sprite.image = briedge
# my_sprite.rect = my_sprite.image.get_rect()
# running = True
# size = width, height = 800, 600
# screen = pygame.display.set_mode(size)
# image = briedge
# while running:
#     for ev in pygame.event.get():
#         if ev.type == pygame.QUIT:
#             running = False
#         elif ev.type == pygame.KEYDOWN:
#             if ev.key == pygame.K_RETURN:
#                 count += 1
#                 print(my_sprite.rect)
#                 print(my_sprite.rect.w - 2, my_sprite.rect.h - 2)
                
#                 image = image.subsurface(pygame.Rect(5, 5, my_sprite.rect.w - 5 * count, my_sprite.rect.h - 5 * count))
            
#                 my_sprite.image = image

#             elif ev.key == pygame.K_f:
#                 image = pygame.Surface((my_sprite.rect.w, my_sprite.rect.h))
#                 image.fill((255, 0, 0))
#                 my_sprite.image = image
#             elif ev.key == pygame.K_e:
#                 my_sprite.image = briedge
#     screen.fill((0, 0, 0))
#     all_sprites.update()
#     all_sprites.draw(screen)
#     pygame.display.flip()







image = pygame.image.load('data/Tiles/Adventurer.png')
column_n = 8
row_n = 12
w, h = image.get_size()
cell_w = w // column_n
cell_h = h // row_n
hero_image = image.subsurface((0, 0, cell_w, cell_h))
pixels = []
width, height = hero_image.get_size()
for col in range(width):
    for row in range(height):
        pixels.append(hero_image.get_at((col, row)))

res = Image.new('RGBA', (width, height))
pixels_of_res = res.load()
print(width, height)
for row in range(height):
    for col in range(width):
        print((row, col))
        print(pixels_of_res[row, col])

res.show()

