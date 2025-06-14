import pygame
from scenes.main_menu import SimplePlatformerScene as sss


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    scene = sss(None)

    running = True
    while running:
        dt = clock.tick(60) / 1000.0  # Delta time in seconds

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        scene.handle_events(events)
        scene.update(dt)
        scene.draw(screen)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()