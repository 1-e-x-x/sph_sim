import numpy as np
import pygame


class SimulationContext:
    def __init__(self):
        self.segment_width = pygame.display.get_surface().get_size()[0] // 3
        self.segment_height = pygame.display.get_surface().get_size()[1] // 3

        self.segments = np.full((3, 3), None, dtype=pygame.sprite.Group)
        for i in range(len(self.segments)):
            for j in range(len(self.segments[i])):
                self.segments[i][j] = pygame.sprite.Group()

        self.current_time = 0.0
        self.time_step = 0.1

    def add_object(self, *objects):
        for obj in objects:
            self.segments[int(obj.position[0] // self.segment_width), int(obj.position[1] // self.segment_height)]\
                .add(obj)

    def update(self):
        pass
