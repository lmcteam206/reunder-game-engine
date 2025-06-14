import pygame
from pygame.math import Vector2

# --- Base Component ---
class Component:
    def __init__(self, game_object):
        self.game_object = game_object

    def start(self): pass
    def update(self, dt): pass
    def draw(self, screen): pass

    def set_property(self, prop_name, value):
        if hasattr(self, prop_name):
            setattr(self, prop_name, value)
        else:
            print(f"⚠️ Property '{prop_name}' not found in {self.__class__.__name__}")

# --- Rigidbody2D ---
class Rigidbody2D(Component):
    def __init__(self, game_object, gravity=1000, drag=0.0, bounce=0.0):
        super().__init__(game_object)
        self.velocity = Vector2(0, 0)
        self.gravity = gravity
        self.drag = drag
        self.bounce = bounce
        self.use_gravity = True
        self.grounded = False  # Must be set by Collider

    def apply_force(self, force):
        self.velocity += Vector2(force)

    def update(self, dt):
        if self.use_gravity:
            self.velocity.y += self.gravity * dt

        # Apply horizontal drag
        self.velocity.x *= max(0, (1 - self.drag))


# --- Collider ---
class Collider(Component):
    def __init__(self, game_object, group=None, solid=True):
        super().__init__(game_object)
        self.group = group
        self.solid = solid
        self.on_collide = None

    def update(self, dt):
        if not self.group:
            return

        rb = self.game_object.get_component(Rigidbody2D)
        if not rb:
            return

        # Reset grounded before checking collisions
        rb.grounded = False

        # Move horizontally
        self.game_object.rect.x += int(rb.velocity.x * dt)
        hits = pygame.sprite.spritecollide(self.game_object, self.group, False)
        for other in hits:
            if other == self.game_object:
                continue
            if self.solid:
                if rb.velocity.x > 0:
                    self.game_object.rect.right = other.rect.left
                elif rb.velocity.x < 0:
                    self.game_object.rect.left = other.rect.right
                rb.velocity.x = 0
            if self.on_collide:
                self.on_collide(other)

        # Move vertically
        self.game_object.rect.y += int(rb.velocity.y * dt)
        hits = pygame.sprite.spritecollide(self.game_object, self.group, False)
        for other in hits:
            if other == self.game_object:
                continue
            if self.solid:
                if rb.velocity.y > 0:
                    self.game_object.rect.bottom = other.rect.top
                    rb.grounded = True
                elif rb.velocity.y < 0:
                    self.game_object.rect.top = other.rect.bottom
                rb.velocity.y = 0
            if self.on_collide:
                self.on_collide(other)

# --- CharacterController2D ---
class CharacterController2D(Component):
    def __init__(self, game_object, speed=200, jump_force=500, collider_group=None):
        super().__init__(game_object)
        self.speed = speed
        self.jump_force = jump_force
        self.collider_group = collider_group

    def update(self, dt):
        keys = pygame.key.get_pressed()
        move = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            move -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            move += 1

        rb = self.game_object.get_component(Rigidbody2D)
        if rb:
            rb.velocity.x = move * self.speed

            if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and rb.grounded:
                rb.velocity.y = -self.jump_force

class MovingPlatform(Component):
    def __init__(self, game_object, speed=100, range_x=100):
        super().__init__(game_object)
        self.speed = speed
        self.range_x = range_x
        self.start_x = game_object.rect.x
        self.direction = 1

    def update(self, dt):
        self.game_object.rect.x += self.direction * self.speed * dt

        if self.game_object.rect.x > self.start_x + self.range_x:
            self.game_object.rect.x = self.start_x + self.range_x
            self.direction = -1
        elif self.game_object.rect.x < self.start_x:
            self.game_object.rect.x = self.start_x
            self.direction = 1