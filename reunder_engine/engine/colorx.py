# colorx.py
import colorsys
import random
import math
import pygame


class ColorX:
    # ----------- Predefined Constants -----------
    BLACK       = (0, 0, 0)
    WHITE       = (255, 255, 255)
    RED         = (255, 0, 0)
    GREEN       = (0, 255, 0)
    BLUE        = (0, 0, 255)
    CYAN        = (0, 255, 255)
    MAGENTA     = (255, 0, 255)
    YELLOW      = (255, 255, 0)
    ORANGE      = (255, 165, 0)
    PURPLE      = (128, 0, 128)
    PINK        = (255, 192, 203)
    GRAY        = (128, 128, 128)
    TRANSPARENT = (0, 0, 0, 0)

    # ----------- Base RGB and HEX Tools -----------
    @staticmethod
    def hex(hex_code, alpha=255):
        hex_code = hex_code.strip("#")
        r = int(hex_code[0:2], 16)
        g = int(hex_code[2:4], 16)
        b = int(hex_code[4:6], 16)
        return (r, g, b, alpha)

    @staticmethod
    def rgb(r, g, b, a=255):
        return (
            max(0, min(255, int(r))),
            max(0, min(255, int(g))),
            max(0, min(255, int(b))),
            max(0, min(255, int(a))),
        )

    @staticmethod
    def to_hex(color):
        r, g, b = color[:3]
        return "#{:02x}{:02x}{:02x}".format(r, g, b)

    # ----------- Manipulation Features -----------
    @staticmethod
    def invert(color):
        r, g, b = color[:3]
        return (255 - r, 255 - g, 255 - b) + color[3:]

    @staticmethod
    def fade(color, percent):
        r, g, b = color[:3]
        return (int(r * percent), int(g * percent), int(b * percent)) + color[3:]

    @staticmethod
    def grayscale(color):
        avg = sum(color[:3]) // 3
        return (avg, avg, avg) + color[3:]

    @staticmethod
    def blend(c1, c2, ratio=0.5):
        return tuple(int(c1[i] * (1 - ratio) + c2[i] * ratio) for i in range(3)) + (255,)

    # ----------- Dynamic Color Generators -----------
    @staticmethod
    def random_color(include_alpha=False):
        rgb = [random.randint(0, 255) for _ in range(3)]
        return tuple(rgb + [random.randint(0, 255)]) if include_alpha else tuple(rgb)

    @staticmethod
    def pastel():
        return tuple(random.randint(128, 255) for _ in range(3)) + (255,)

    @staticmethod
    def neon():
        base = random.choice([(255, random.randint(0, 100), random.randint(0, 100)),
                              (random.randint(0, 100), 255, random.randint(0, 100)),
                              (random.randint(0, 100), random.randint(0, 100), 255)])
        return base + (255,)

    # ----------- HSV and HSL -----------
    @staticmethod
    def hsv(h, s, v):
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return (int(r*255), int(g*255), int(b*255), 255)

    @staticmethod
    def from_hsv_tuple(hsv):
        return ColorX.hsv(*hsv)

    @staticmethod
    def to_hsv(color):
        r, g, b = [c/255 for c in color[:3]]
        return colorsys.rgb_to_hsv(r, g, b)

    # ----------- Utility -----------
    @staticmethod
    def is_dark(color):
        r, g, b = color[:3]
        brightness = (0.299*r + 0.587*g + 0.114*b)
        return brightness < 128

    @staticmethod
    def contrast_text(color):
        return ColorX.WHITE if ColorX.is_dark(color) else ColorX.BLACK

    @staticmethod
    def lerp(c1, c2, t):
        return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3)) + (255,)

    @staticmethod
    def saturate(color, factor=1.2):
        h, s, v = ColorX.to_hsv(color)
        s = min(1.0, s * factor)
        return ColorX.hsv(h, s, v)

    @staticmethod
    def darken(color, amount=0.2):
        h, s, v = ColorX.to_hsv(color)
        v = max(0, v - amount)
        return ColorX.hsv(h, s, v)

class BackgroundX:
    # 1. Solid color fill
    @staticmethod
    def solid(color, size):
        surface = pygame.Surface(size)
        surface.fill(color)
        return surface

    # 2. Vertical gradient
    @staticmethod
    def vertical_gradient(top_color, bottom_color, size):
        surface = pygame.Surface(size)
        width, height = size
        for y in range(height):
            t = y / height
            color = ColorX.lerp(top_color, bottom_color, t)
            pygame.draw.line(surface, color, (0, y), (width, y))
        return surface

    # 3. Horizontal gradient
    @staticmethod
    def horizontal_gradient(left_color, right_color, size):
        surface = pygame.Surface(size)
        width, height = size
        for x in range(width):
            t = x / width
            color = ColorX.lerp(left_color, right_color, t)
            pygame.draw.line(surface, color, (x, 0), (x, height))
        return surface

    # 4. Sine wave gradient
    @staticmethod
    def sine_gradient(size, frame=0, freq=0.01):
        surface = pygame.Surface(size)
        width, height = size
        for y in range(height):
            t = y / height
            r = int(127 + 128 * math.sin(frame * freq + t * 3))
            g = int(127 + 128 * math.sin(frame * freq * 1.2 + t * 3))
            b = int(127 + 128 * math.sin(frame * freq * 1.5 + t * 3))
            pygame.draw.line(surface, (r, g, b), (0, y), (width, y))
        return surface

    # 5. Centered image
    @staticmethod
    def image_background(image, size, position="center"):
        surface = pygame.Surface(size)
        surface.fill(ColorX.BLACK)
        img_rect = image.get_rect()
        scr_rect = surface.get_rect()

        if position == "center":
            img_rect.center = scr_rect.center
        elif position == "topleft":
            img_rect.topleft = (0, 0)
        elif position == "stretch":
            image = pygame.transform.scale(image, size)
            img_rect = image.get_rect()

        surface.blit(image, img_rect)
        return surface

    # 6. Tile image
    @staticmethod
    def tile(image, size):
        surface = pygame.Surface(size)
        iw, ih = image.get_size()
        for x in range(0, size[0], iw):
            for y in range(0, size[1], ih):
                surface.blit(image, (x, y))
        return surface

    # 7. Checker pattern
    @staticmethod
    def checker(color1, color2, size, square_size=40):
        surface = pygame.Surface(size)
        for y in range(0, size[1], square_size):
            for x in range(0, size[0], square_size):
                color = color1 if (x // square_size + y // square_size) % 2 == 0 else color2
                pygame.draw.rect(surface, color, (x, y, square_size, square_size))
        return surface

    # 8. Striped background
    @staticmethod
    def stripes(color1, color2, size, direction="horizontal", stripe_size=20):
        surface = pygame.Surface(size)
        for i in range(0, size[1 if direction == "horizontal" else 0], stripe_size * 2):
            rect = (0, i, size[0], stripe_size) if direction == "horizontal" else (i, 0, stripe_size, size[1])
            pygame.draw.rect(surface, color1, rect)
        surface.fill(color2, special_flags=pygame.BLEND_RGB_SUB)
        return surface

    # 9. Radial gradient
    @staticmethod
    def radial_gradient(center_color, edge_color, size):
        surface = pygame.Surface(size)
        cx, cy = size[0] // 2, size[1] // 2
        max_dist = math.hypot(cx, cy)
        for y in range(size[1]):
            for x in range(size[0]):
                dist = math.hypot(x - cx, y - cy) / max_dist
                color = ColorX.lerp(center_color, edge_color, dist)
                surface.set_at((x, y), color[:3])
        return surface

    # 10. Noise background
    @staticmethod
    def noise(size, intensity=64):
        surface = pygame.Surface(size)
        for y in range(size[1]):
            for x in range(size[0]):
                val = random.randint(0, intensity)
                surface.set_at((x, y), (val, val, val))
        return surface

    # 11. Rainbow wave
    @staticmethod
    def rainbow_wave(size, frame=0):
        surface = pygame.Surface(size)
        width, height = size
        for y in range(height):
            h = (math.sin((y + frame) * 0.02) + 1) / 2
            color = ColorX.hsv(h, 1, 1)
            pygame.draw.line(surface, color, (0, y), (width, y))
        return surface

    # 12. Animated vertical glow
    @staticmethod
    def glowing_gradient(size, frame, speed=0.02):
        surface = pygame.Surface(size)
        width, height = size
        for y in range(height):
            t = math.sin((frame * speed) + (y * 0.05)) * 0.5 + 0.5
            color = ColorX.lerp(ColorX.BLACK, ColorX.WHITE, t)
            pygame.draw.line(surface, color, (0, y), (width, y))
        return surface

    # 13. Grid lines
    @staticmethod
    def grid(color, size, spacing=50):
        surface = pygame.Surface(size)
        surface.fill(ColorX.BLACK)
        for x in range(0, size[0], spacing):
            pygame.draw.line(surface, color, (x, 0), (x, size[1]))
        for y in range(0, size[1], spacing):
            pygame.draw.line(surface, color, (0, y), (size[0], y))
        return surface

    # 14. Custom curve map (func: y = f(x))
    @staticmethod
    def curve(color, size, func):
        surface = pygame.Surface(size)
        surface.fill(ColorX.BLACK)
        for x in range(size[0]):
            y = int(func(x))
            if 0 <= y < size[1]:
                surface.set_at((x, y), color[:3])
        return surface

    # 15. Pulsing solid color
    @staticmethod
    def pulsing_solid(base_color, size, frame, speed=0.1):
        intensity = (math.sin(frame * speed) + 1) / 2
        color = ColorX.fade(base_color, intensity)
        return BackgroundX.solid(color, size)

    # 16. Multi-color gradient
    @staticmethod
    def multi_gradient(colors, size):
        surface = pygame.Surface(size)
        steps = len(colors) - 1
        for i in range(steps):
            part_height = size[1] // steps
            for y in range(part_height):
                t = y / part_height
                color = ColorX.lerp(colors[i], colors[i+1], t)
                pygame.draw.line(surface, color, (0, i * part_height + y), (size[0], i * part_height + y))
        return surface

    # 17. Wave pattern background
    @staticmethod
    def wave_pattern(color, size, amplitude=20, wavelength=40, frame=0):
        surface = pygame.Surface(size)
        surface.fill(ColorX.BLACK)
        for x in range(size[0]):
            y = int(size[1] / 2 + amplitude * math.sin((x + frame) * (2 * math.pi / wavelength)))
            pygame.draw.circle(surface, color, (x, y), 1)
        return surface

    # 18. Blinking background
    @staticmethod
    def blinking(color1, color2, size, frame, rate=30):
        current = color1 if (frame // rate) % 2 == 0 else color2
        return BackgroundX.solid(current, size)

    # 19. Vignette
    @staticmethod
    def vignette(size, strength=0.5):
        surface = pygame.Surface(size)
        cx, cy = size[0] // 2, size[1] // 2
        max_dist = math.hypot(cx, cy)
        for y in range(size[1]):
            for x in range(size[0]):
                dist = math.hypot(x - cx, y - cy) / max_dist
                alpha = int(255 * min(1, dist * strength))
                surface.set_at((x, y), (0, 0, 0, alpha))
        return surface

    # 20. Star field
    @staticmethod
    def starfield(size, count=100):
        surface = pygame.Surface(size)
        surface.fill(ColorX.BLACK)
        for _ in range(count):
            x = random.randint(0, size[0] - 1)
            y = random.randint(0, size[1] - 1)
            brightness = random.randint(150, 255)
            surface.set_at((x, y), (brightness, brightness, brightness))
        return surface