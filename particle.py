import numpy as np
import pygame
from scipy import constants

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)


def pressure_force(original_particle, other_particle):
    distance = abs(
        np.linalg.norm(original_particle.position)
        - np.linalg.norm(other_particle.position)
    )

    return (
        -(45 * original_particle.mass)
        / (constants.pi * original_particle.size)
        * -(other_particle.position - original_particle.position)
        / distance
        * (original_particle.pressure + other_particle.pressure)
        / (2 * other_particle.density)
        * (original_particle.size - distance) ** 2
    )


def viscous_force(original_particle, other_particle):
    return (
        (22.5 * original_particle.mass)
        / (constants.pi * original_particle.size**6)
        * (other_particle.velocity - original_particle.velocity)
        / other_particle.density
        * (
            original_particle.size
            - abs(
                np.linalg.norm(original_particle.position)
                - np.linalg.norm(other_particle.position)
            )
        )
    )


class Particle(pygame.sprite.Sprite):
    def __init__(
        self,
        pos,
        vel,
        mass=1.0,
        size=30,
        color=BLUE,
    ):
        pygame.sprite.Sprite.__init__(self)

        self.size = size
        self.mass = mass

        self.position = pos.astype(np.float64)
        self.velocity = vel.astype(np.float64)
        self.new_position = self.position.copy()
        self.new_velocity = self.velocity.copy()
        self.density = (315 * self.mass) / (64 * constants.pi * self.size**9)
        self.pressure = 20 * (self.density - self.mass)

        self.image = pygame.surface.Surface((size, size))
        pygame.draw.circle(self.image, color, (size // 2, size // 2), size // 2, size)
        self.rect = self.image.get_rect()
        self.update_display()

    def update(self, time_step, neighbors):
        force = np.array([0.0, -constants.g])

        for group in neighbors:
            g = pygame.sprite.Group()
            for particle in group.sprites():
                # REALLY bad solution
                if (particle.position == self.position).all():
                    continue

                if (
                    abs(
                        np.linalg.norm(self.position)
                        - np.linalg.norm(particle.position)
                    )
                    > self.size
                ):
                    continue

                force += self.calculate(particle)

        self.new_velocity = self.velocity + force / self.density * time_step
        self.new_position = self.position + self.new_velocity * time_step

        print(self.new_position)

        # handle x bounds
        if self.new_position[0] <= 0.0:
            print('hi 1')
            self.new_position[0] = 0.1
            self.new_velocity[0] *= -1
        elif self.new_position[0] > pygame.display.get_surface().get_size()[0]:
            print('hi 2')
            self.new_position[0] = np.float64(
                pygame.display.get_surface().get_size()[0]
            )
            self.new_velocity[0] *= -1

        # handle y bounds
        if self.new_position[1] <= 0.0:
            print('hi 3')
            self.new_position[1] = 0.1
            self.new_velocity[1] *= -1
        elif self.new_position[1] > pygame.display.get_surface().get_size()[1]:
            print('hi 4')
            self.new_position[1] = np.float64(
                pygame.display.get_surface().get_size()[1]
            )
            self.new_velocity[1] *= -1

    def calculate(self, other):
        force = np.array([0.0, 0.0])
        force += pressure_force(self, other) + viscous_force(self, other)
        return force

    def update_display(self):
        self.velocity = self.new_velocity
        self.position = self.new_position

        self.rect.x = int(self.position[0])
        self.rect.y = int(pygame.display.get_surface().get_size()[1] - self.position[1])
