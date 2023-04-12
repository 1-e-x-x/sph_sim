import numpy as np
import pygame
from scipy import constants


BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

SMOOTHER = 50


def calculate_density(particle, distances):
    return (
        (315 * particle.mass)
        / (64 * constants.pi * SMOOTHER**9)
        * sum([(SMOOTHER**2 - x**2) ** 3 for x in distances])
    )


def calculate_pressure(particle):
    return 20 * (particle.density - 1)


def calculate_pressure_force(particle, neighbors, distances):
    if len(distances) == 0:
        return np.zeros((2,))

    return (
        -(45 * particle.mass)
        / (constants.pi * SMOOTHER**6)
        * sum(
            [
                -(p.position - particle.position)
                / x
                * (particle.pressure + p.pressure)
                / (2 * p.density)
                * (SMOOTHER - x) ** 2
                for p, x in list(zip(neighbors, distances))
            ]
        )
    )


def calculate_viscous_force(particle, neighbors, distances):
    if len(distances) == 0:
        return np.zeros((2,))

    return (
        (45 * 0.5 * particle.mass)
        / (constants.pi * SMOOTHER**6)
        * sum(
            [
                (p.velocity - particle.velocity) / p.density * (SMOOTHER - x)
                for p, x in list(zip(neighbors, distances))
            ]
        )
    )


class Particle(pygame.sprite.Sprite):
    def __init__(self, mass, position, velocity, size=30, color=BLUE):
        pygame.sprite.Sprite.__init__(self)

        self.size = size

        self.mass = mass
        self.position = position.astype(np.float64)
        self.velocity = velocity.astype(np.float64)

        self.image = pygame.surface.Surface((size, size))
        pygame.draw.circle(self.image, color, (size // 2, size // 2), size // 2, size)
        self.rect = self.image.get_rect()

    def pre_update(self, distances):
        self.density = calculate_density(self, distances)
        self.pressure = calculate_pressure(self)

    def update(self, time_step, neighbors, distances):
        force = np.array([0.0, -0.1])

        force += calculate_pressure_force(self, neighbors, distances)
        force += calculate_viscous_force(self, neighbors, distances)

        self.new_velocity = self.velocity + (force) / self.density * time_step
        self.new_position = self.position + self.new_velocity * time_step

        # x boundaries
        if self.new_position[0] < 0.0:
            self.new_position[0] = 0.0
            self.new_velocity[0] *= -0.2
        elif self.new_position[0] > pygame.display.get_surface().get_size()[0] - self.size:
            self.new_position[0] = pygame.display.get_surface().get_size()[0] - self.size
            self.new_velocity[0] *= -0.2

        # y boundaries
        if self.new_position[1] < self.size:
            self.new_position[1] = self.size
            self.new_velocity[1] *= -0.2
        elif self.new_position[1] > pygame.display.get_surface().get_size()[1]:
            self.new_position[1] = pygame.display.get_surface().get_size()[1]
            self.new_velocity[1] *= -0.2

    def post_update(self):
        self.position = self.new_position
        self.velocity = self.new_velocity

        self.rect.x = int(self.position[0])
        self.rect.y = int(pygame.display.get_surface().get_size()[1] - self.position[1])
