import pygame
import numpy as np
import noise

IMAGE_SCALE = 720
NOISE_SCALE = 40
NOISE_SPEED = 0.5
ZOOM = 0.05


def main():
    pygame.init()
    screen = pygame.display.set_mode((IMAGE_SCALE, IMAGE_SCALE))
    pygame.display.set_caption("Perlin Noise")
    clock = pygame.time.Clock()

    # Main loop
    running = True
    time = 0

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))

        # Create a 2D array of values between 0 and 1
        values = np.zeros((NOISE_SCALE, NOISE_SCALE))
        for x in range(NOISE_SCALE):
            for y in range(NOISE_SCALE):
                values[x][y] = noise.pnoise3(x * ZOOM, y * ZOOM, time * NOISE_SPEED)

        # Draw the noise
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

        pygame.display.set_caption(f"Perlin Noise - FPS: {int(clock.get_fps())}")
        pygame.display.flip()
        time += clock.tick(60) / 1000


if __name__ == "__main__":
    main()
