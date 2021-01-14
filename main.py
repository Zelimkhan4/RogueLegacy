import pygame


if __name__ == '__main__':
    size = width, height = 400, 600
    screen = pygame.display.set_mode(size)
    FPS = 60
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((255, 255, 255))
        pygame.display.flip()
        clock.tick()