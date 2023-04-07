import numpy as np
import pygame

from particle import *


class SimulationContext:
    def __init__(self):
        self.segment_width = pygame.display.get_surface().get_size()[0] // 3 + 1
        self.segment_height = pygame.display.get_surface().get_size()[1] // 3 + 1

        self.segments = np.full((3, 3), None, dtype=pygame.sprite.Group)
        for i in range(len(self.segments)):
            for j in range(len(self.segments[i])):
                self.segments[i][j] = pygame.sprite.Group()

        self.current_time = 0.0
        self.time_step = 0.000000001

    def add_object(self, *objects):
        for obj in objects:
            self.segments[
                int(obj.position[0] // self.segment_width),
                int(obj.position[1] // self.segment_height),
            ].add(obj)

    def update(self):
        pygame.display.get_surface().fill(BLACK)

        for i in range(len(self.segments)):
            for j in range(len(self.segments[i])):
                self.segments[i][j].update(self.time_step, [self.segments[x, y] for x, y in self.get_neighbors(i, j)])

        for i in range(len(self.segments)):
            for j in range(len(self.segments[i])):
                for particle in self.segments[i][j].sprites():
                    particle.update_display()
                    if int(particle.position[0] // self.segment_width) != i or \
                        int(particle.position[1] // self.segment_height) != j:
                        self.segments[i][j].remove(particle)
                        self.add_object(particle)

        for i in range(len(self.segments)):
            for j in range(len(self.segments[i])):
                self.segments[i][j].draw(pygame.display.get_surface())

        pygame.display.flip()
        self.current_time += self.time_step

    def get_neighbors(self, i, j):
        ranges = [
            [x if 0 <= x < 3 else -1 for x in range(i - 1, i + 2)],
            [x if 0 <= x < 3 else -1 for x in range(j - 1, j + 2)],
        ]

        perms = []
        for i in range(len(ranges)):
            for j in range(len(ranges[i])):
                if i != -1 or j != -1:
                    perms.append([i, j])

        return np.array(perms)
