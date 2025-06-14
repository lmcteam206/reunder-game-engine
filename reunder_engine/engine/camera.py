import pygame
class Camera:
    def __init__(self, screen_size):
        self.offset = pygame.Vector2(0, 0)
        self.screen_width, self.screen_height = screen_size
        self.target = None

    def follow(self, target):
        self.target = target

    def update(self):
        if self.target:
            target_center = self.target.rect.center
            self.offset.x = target_center[0] - self.screen_width // 2
            self.offset.y = target_center[1] - self.screen_height // 2
