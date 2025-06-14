import pygame

# ---------- Base Component ----------
class Component:
    def __init__(self, game_object):
        self.game_object = game_object

    def start(self): pass
    def update(self, dt): pass
    def draw(self, screen): pass

# ---------- GameObject with Components ----------
class GameObject(pygame.sprite.Sprite):
    def __init__(self, image, pos=(0, 0), size=None):
        super().__init__()
        self.original_image = image
        self.size = size
        self.image = pygame.transform.scale(image, size) if size else image
        self.rect = self.image.get_rect(topleft=pos)
        self.components = []
        self.z_index = 0  # Used for draw sorting if needed

    def add_component(self, component_cls, *args, **kwargs):
        component = component_cls(self, *args, **kwargs)
        self.components.append(component)
        component.start()
        return component

    def get_component(self, component_type):
        for c in self.components:
            if isinstance(c, component_type):
                return c
        return None

    def update(self, dt):
        for c in self.components:
            c.update(dt)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)  # Ensure the sprite is drawn!
        for c in self.components:
            c.draw(screen)

# ---------- AnimatedSprite ----------
class AnimatedSprite(GameObject):
    def __init__(self, frames, pos=(0, 0), frame_delay=100, size=None):
        scaled_frames = [pygame.transform.scale(f, size) for f in frames] if size else frames
        super().__init__(scaled_frames[0], pos, size)
        self.frames = scaled_frames
        self.frame_delay = frame_delay
        self.current_time = 0
        self.frame_index = 0

    def update(self, dt):
        self.current_time += dt
        if self.current_time >= self.frame_delay:
            self.current_time = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]
        super().update(dt)

# ---------- ObjectManager ----------
class ObjectManager:
    def __init__(self):
        self.backgrounds = []  # List of (image, mode)
        self.sprites = pygame.sprite.Group()

    def add_sprite(self, image, pos=(0, 0), size=None):
        sprite = GameObject(image, pos, size)
        self.sprites.add(sprite)
        return sprite

    def add_animated_sprite(self, frame_list, pos=(0, 0), frame_delay=100, size=None):
        sprite = AnimatedSprite(frame_list, pos, frame_delay, size)
        self.sprites.add(sprite)
        return sprite

    def add_background(self, image, mode="stretch"):
        self.backgrounds.append((image, mode))

    def clear_sprites(self):
        self.sprites.empty()
        self.backgrounds.clear()

    def update(self, dt):
        for sprite in self.sprites:
            sprite.update(dt)

    def draw(self, screen, camera=None):
        screen_size = screen.get_size()

        # Draw background
        for bg_image, mode in self.backgrounds:
            if mode == "stretch":
                scaled = pygame.transform.scale(bg_image, screen_size)
                screen.blit(scaled, (0, 0))
            elif mode == "tile":
                w, h = bg_image.get_size()
                for x in range(0, screen_size[0], w):
                    for y in range(0, screen_size[1], h):
                        screen.blit(bg_image, (x, y))
            elif mode == "center":
                x = (screen_size[0] - bg_image.get_width()) // 2
                y = (screen_size[1] - bg_image.get_height()) // 2
                screen.blit(bg_image, (x, y))

        # Draw sprites with camera offset
        for sprite in sorted(self.sprites, key=lambda s: getattr(s, 'z_index', 0)):
            pos = sprite.rect.topleft
            offset = camera.offset if camera else pygame.Vector2(0, 0)
            screen.blit(sprite.image, (pos[0] - offset.x, pos[1] - offset.y))
            for c in sprite.components:
                c.draw(screen)

