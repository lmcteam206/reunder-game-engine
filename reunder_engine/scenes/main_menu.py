import random
import pygame
from engine.scene_manager import BaseScene
from engine.object_manager import ObjectManager
from engine.components import Rigidbody2D, Collider, CharacterController2D, MovingPlatform
from engine.utils import load_img
from engine.camera import Camera

class SimplePlatformerScene(BaseScene):
    def __init__(self, manager):
        super().__init__(manager)
        self.level_index = 0
        self.max_levels = 1
        self.objects = ObjectManager()
        self.camera = Camera((800, 600))
        self.interaction_ready = False
        self.player = None
        self.goal = None
        self.setup_scene()

    def setup_scene(self):
        bg = load_img("background.png")
        if bg:
            self.objects.add_background(bg, mode="stretch")
        else:
            print("⚠️ Warning: 'background.png' not found. Using fallback background.")
        self.load_level(self.level_index)

    def load_level(self, index):
        self.objects.clear_sprites()
        self.interaction_ready = False
        self.goal = None

        screen_width = 800
        platform_width = 140

        def create_platform(x, y, w, h, moving=False):
            surface = pygame.Surface((w, h))
            surface.fill((100, 200, 100))
            plat = self.objects.add_sprite(surface, (x, y), size=(w, h))
            plat.add_component(Collider, solid=True, group=self.objects.sprites)
            plat.z_index = 0
            if moving:
                speed = random.uniform(50, 150)
                range_x = random.randint(50, 150)
                plat.add_component(MovingPlatform, speed=speed, range_x=range_x)
            return plat

        def create_goal(x, y, w=40, h=40):
            surface = pygame.Surface((w, h))
            surface.fill((255, 255, 0))
            goal = self.objects.add_sprite(surface, (x, y), size=(w, h))
            goal.z_index = 0
            goal.add_component(Collider, solid=False, group=self.objects.sprites)
            self.goal = goal

        # Floor platform at bottom (static)
        create_platform(0, 580, 800, 20)

        # Create 19 moving platforms (because last one is static)
        for i in range(19):
            random_x = random.randint(0, screen_width - platform_width)
            y = 480 - i * 100
            create_platform(random_x, y, platform_width, 20, moving=True)

        # Create last platform (highest) WITHOUT moving component, static
        last_platform_y = 480 - 19 * 100
        last_platform_x = random.randint(0, screen_width - platform_width)
        last_platform = create_platform(last_platform_x, last_platform_y, platform_width, 20, moving=False)

        player_img = load_img("player.png")
        self.player = self.objects.add_sprite(player_img, (300, 530), size=(48, 48))
        self.player.z_index = 1

        rb = self.player.add_component(Rigidbody2D, gravity=1500, bounce=0)
        col = self.player.add_component(Collider, solid=True, group=self.objects.sprites)
        ctrl = self.player.add_component(CharacterController2D, collider_group=self.objects.sprites)

        # Adjust player properties dynamically
        if ctrl:
            ctrl.set_property("jump_force", 1000)
            ctrl.set_property("speed", 400)

        if rb:
            rb.set_property("gravity", 1040)
            rb.set_property("bounce", 1)

        self.camera.follow(self.player)

        # Place goal on top of the last platform
        create_goal(last_platform.rect.x + (platform_width - 40) // 2, last_platform.rect.y - 40)

        # Save reference to last platform for updating goal position
        self.last_platform = last_platform

    def handle_events(self, events):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN] and self.interaction_ready:
            print("🎯 Level Complete!")
            self.load_level(self.level_index)

    def update(self, dt):
        self.objects.update(dt)
        self.camera.update()

        # Keep goal locked on top of last platform
        if self.goal and hasattr(self, 'last_platform'):
            self.goal.rect.x = self.last_platform.rect.x + (self.last_platform.rect.width - self.goal.rect.width) // 2
            self.goal.rect.y = self.last_platform.rect.y - self.goal.rect.height

        self.interaction_ready = False
        if self.player and self.goal:
            player_rect = self.player.rect
            goal_rect = self.goal.rect
            interaction_area = goal_rect.inflate(20, 20)
            if player_rect.colliderect(interaction_area):
                self.interaction_ready = True

    def draw(self, screen):
        if not self.objects.backgrounds:
            screen.fill((30, 30, 30))
        self.objects.draw(screen, camera=self.camera)
