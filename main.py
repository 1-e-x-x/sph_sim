import particle
import sim

import numpy as np
import pygame


def main():
    pygame.init()
    pygame.display.set_mode((640, 480))

    ctx = sim.SimulationContext()
    p1 = particle.Particle(1, np.array([100, 400]), np.array([0, 0]))
    p11 = particle.Particle(1, np.array([110, 400]), np.array([0, 0]))
    p111 = particle.Particle(1, np.array([120, 400]), np.array([0, 0]))
    p1111 = particle.Particle(1, np.array([130, 400]), np.array([0, 0]))
    p11111 = particle.Particle(1, np.array([140, 400]), np.array([0, 0]))
    p2 = particle.Particle(1, np.array([100, 200]), np.array([0, 0]))
    ctx.add_object(p1, p11, p111, p1111, p11111, p2)

    while pygame.get_init():
        ctx.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


if __name__ == "__main__":
    main()
