import particle
import sim

import numpy as np
import pygame


def main():
    pygame.init()

    while pygame.get_init():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


if __name__ == "__main__":
    main()
