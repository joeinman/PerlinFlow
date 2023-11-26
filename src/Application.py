import pygame
import numpy as np
import noise

IMAGE_SCALE = 720
NOISE_SCALE = 20
NOISE_SPEED = 0.5
ZOOM = 0.1


def main():
    pygame.init()
    screen = pygame.display.set_mode((IMAGE_SCALE, IMAGE_SCALE))
    pygame.display.set_caption("PerlinFlow Simulation")
    clock = pygame.time.Clock()

    # Main loop
    running = True
    time = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))

        # Sample Noise
        values = np.zeros((NOISE_SCALE, NOISE_SCALE))
        for x in range(NOISE_SCALE):
            for y in range(NOISE_SCALE):
                values[x][y] = noise.pnoise3(x * ZOOM, y * ZOOM, time * NOISE_SPEED)
        gradient = np.gradient(values)

        # Draw Noise
        for x in range(NOISE_SCALE):
            for y in range(NOISE_SCALE):
                color_value = int((values[x, y] + 1) * 128)
                pygame.draw.rect(
                    screen,
                    (color_value, color_value, color_value),
                    (
                        x * (IMAGE_SCALE / NOISE_SCALE),
                        y * (IMAGE_SCALE / NOISE_SCALE),
                        (IMAGE_SCALE / NOISE_SCALE),
                        (IMAGE_SCALE / NOISE_SCALE),
                    ),
                )

        # Draw Lines From Center of Each Square to the Gradient
        for x in range(NOISE_SCALE):
            for y in range(NOISE_SCALE):
                pygame.draw.line(
                    screen,
                    (0, 255, 0),
                    (
                        x * (IMAGE_SCALE / NOISE_SCALE)
                        + (IMAGE_SCALE / NOISE_SCALE) / 2,
                        y * (IMAGE_SCALE / NOISE_SCALE)
                        + (IMAGE_SCALE / NOISE_SCALE) / 2,
                    ),
                    (
                        x * (IMAGE_SCALE / NOISE_SCALE)
                        + (IMAGE_SCALE / NOISE_SCALE) / 2
                        + gradient[0][x][y] * 100,
                        y * (IMAGE_SCALE / NOISE_SCALE)
                        + (IMAGE_SCALE / NOISE_SCALE) / 2
                        + gradient[1][x][y] * 100,
                    ),
                    2,
                )

        pygame.display.set_caption(
            "PerlinFlow Simulation - FPS: {}".format(int(clock.get_fps()))
        )
        time += clock.tick(60) / 1000
        pygame.display.flip()


if __name__ == "__main__":
    main()
