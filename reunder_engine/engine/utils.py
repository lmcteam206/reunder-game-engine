import pygame
import os

def load_img(path, size=None):
    """
    Load an image from the 'assets' folder.
    :param path: Relative path to the image file (e.g., 'player.png')
    :param size: Optional (width, height) tuple to scale the image.
    :return: pygame.Surface or None if not found.
    """
    full_path = os.path.join("assets", path)
    try:
        image = pygame.image.load(full_path).convert_alpha()
        if size is not None:
            image = pygame.transform.scale(image, size)
        return image
    except pygame.error as e:
        print(f"⚠️ Warning: Failed to load image '{full_path}': {e}")
        return None
