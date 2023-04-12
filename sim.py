import numpy as np
import pygame
from sklearn import neighbors

from particle import *


class SimulationContext:
    def __init__(self):
        self.segment_width = pygame.display.get_surface().get_size()[0] // 3 + 1
        self.segment_height = pygame.display.get_surface().get_size()[1] // 3 + 1

        self.add_tick = 200
        self.tick = 1

        self.group = pygame.sprite.Group()
        self.time_step = 0.01

    def add_object(self, *objects):
        self.group.add(objects)

    def update(self):
        self.tick += 1
        if self.tick % self.add_tick == 0 and len(self.group.sprites()) < 1000:
            new = Particle(1, np.array([200.0, 400.0]), np.array([0.0, 0.0]))
            self.add_object(new)
            self.tick = 1

        pygame.display.get_surface().fill(BLACK)
        neighbors, distances = self.get_neighbors()

        for i, particle in enumerate(self.group.sprites()):
            particle.pre_update(distances[i])
        
        for i, particle in enumerate(self.group.sprites()):
            particle.update(self.time_step, np.array(list(map(lambda x: self.group.sprites()[x], np.delete(neighbors[i], 0)))), np.delete(distances[i], 0))

        for particle in self.group.sprites():
            particle.post_update()

        self.group.draw(pygame.display.get_surface())
        pygame.display.flip()

    def get_neighbors(self):
        tree = np.array(list(map(lambda x: x.position, self.group.sprites())))
        return neighbors.KDTree(tree).query_radius(tree, SMOOTHER, return_distance=True, sort_results=True)
