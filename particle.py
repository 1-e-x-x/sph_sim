import numpy as np
import pygame

BLACK = (0, 0, 0)


class Particle(pygame.sprite.Sprite):
    def __init__(
        self, pos: np.ndarray, vel: np.ndarray, size: int, color: tuple[int, int, int]
    ) -> None:
        pygame.sprite.Sprite.__init__(self)

        self.position = pos.astype(np.float64)
        self.velocity = vel.astype(np.float64)

        self.image = pygame.surface.Surface((size, size))
        self.image.fill(BLACK)
        pygame.draw.circle(self.image, color, (size // 2, size // 2), size // 2, size)
        self.rect = self.image.get_rect()
