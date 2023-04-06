import particle
import sim

import numpy as np
import pygame


def main():
    pygame.init()
    pygame.display.set_mode((640, 480))

    ctx = sim.SimulationContext()
    p1 = particle.Particle(np.array([100, 400]), np.array([0, 0]), 30)
    ctx.add_object(p1)

    while pygame.get_init():
        ctx.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


if __name__ == "__main__":
    main()
