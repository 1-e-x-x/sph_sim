import numpy as np
import pygame
from scipy import constants


BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

SMOOTHER = 5


def calculate_density(particle, neighbors):
    return (
        (315 * particle.mass)
        / (64 * constants.pi * SMOOTHER**9)
        * sum(
            [
                (
                    SMOOTHER**2
                    - abs(np.linalg.norm(particle.position) - np.linalg.norm(x.position))
                    ** 2
                )
                ** 3
                for x in neighbors if x != particle
            ]
        )
    )


def calculate_pressure(particle):
    return 20 * (particle.density - 1)


def calculate_density_force(particle, neighbors):
    return (
        -(45 * particle.mass)
        / (constants.pi * SMOOTHER**6)
        * sum(
            [
                -(x.position - particle.position)
                / abs(np.linalg.norm(particle.position) - np.linalg.norm(x.position))
                * (particle.pressure + x.pressure)
                / (2 * x.density)
                * (
                    SMOOTHER
                    - abs(
                        np.linalg.norm(particle.position) - np.linalg.norm(x.position)
                    )
                )
                ** 2
                for x in neighbors if x != particle
            ]
        )
    )


def calculate_viscous_force(particle, neighbors):
    return (
        (45 * 0.5 * particle.mass)
        / (constants.pi * SMOOTHER**6)
        * sum(
            [
                (x.velocity - particle.velocity)
                / x.density
                * (
                    SMOOTHER
                    - abs(
                        np.linalg.norm(particle.position) - np.linalg.norm(x.position)
                    )
                )
                for x in neighbors if x != particle
            ]
        )
    )


class Particle(pygame.sprite.Sprite):
    def __init__(self, mass, position, velocity, size=30, color=BLUE):
        pygame.sprite.Sprite.__init__(self)

        self.mass = mass
        self.position = position.astype(np.float64)
        self.velocity = velocity.astype(np.float64)

        self.image = pygame.surface.Surface((size, size))
        pygame.draw.circle(self.image, color, (size // 2, size // 2), size // 2, size)
        self.rect = self.image.get_rect()

    def pre_update(self, neighbors):
        flattened = self.flatten_neighbors(neighbors)
        self.density = calculate_density(self, flattened)
        self.pressure = calculate_pressure(self)

    def update(self, time_step, neighbors):
        force = np.array([0.0, -constants.g])

        flattened = self.flatten_neighbors(neighbors)

        print('d', calculate_density_force(self, flattened))
        print('v', calculate_viscous_force(self, flattened))

        force += calculate_density_force(self, flattened)
        force += calculate_viscous_force(self, flattened)

        self.new_velocity = self.velocity + force / self.density * time_step
        self.new_position = self.position + self.new_velocity * time_step

        # x boundaries
        if self.new_position[0] < 0:
            self.new_position[0] = 0.0
            self.new_velocity[0] *= -0.9
        elif self.new_position[0] > pygame.display.get_surface().get_size()[0]:
            self.new_position[0] = pygame.display.get_surface().get_size()[0]
            self.new_velocity[0] *= -0.9

        # y boundaries
        if self.new_position[1] < 0:
            self.new_position[1] = 0.0
            self.new_velocity[1] *= -0.9
        elif self.new_position[1] > pygame.display.get_surface().get_size()[1]:
            self.new_position[1] = pygame.display.get_surface().get_size()[1]
            self.new_velocity[1] *= -0.9

    def post_update(self):
        self.position = self.new_position
        self.velocity = self.new_velocity
        print(self.position)
        self.rect.x = int(self.position[0])
        self.rect.y = int(pygame.display.get_surface().get_size()[1] - self.position[1])

    def flatten_neighbors(self, groups):
        particles = []
        for group in groups:
            for particle in group:
                particles.append(particle)

        return particles
