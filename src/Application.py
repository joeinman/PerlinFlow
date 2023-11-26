import pygame
import numpy as np
import noise

from Particle import Particle

IMAGE_SCALE = 720
NOISE_SCALE = 40
NOISE_SPEED = 0.1
ZOOM = 0.05
N_PARTICLES = 300


def drawNoise(screen, noise):
    # Draw Noise
    for x in range(NOISE_SCALE):
        for y in range(NOISE_SCALE):
            color_value = int((noise[x, y] + 1) * 128)
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


def drawGradient(screen, gradient):
    # Draw Lines From Center of Each Square to the Gradient
    for x in range(NOISE_SCALE):
        for y in range(NOISE_SCALE):
            pygame.draw.line(
                screen,
                (0, 255, 0),
                (
                    x * (IMAGE_SCALE / NOISE_SCALE) + (IMAGE_SCALE / NOISE_SCALE) / 2,
                    y * (IMAGE_SCALE / NOISE_SCALE) + (IMAGE_SCALE / NOISE_SCALE) / 2,
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


def draw_particles(screen, particles):
    trans_surface = pygame.Surface((IMAGE_SCALE, IMAGE_SCALE), pygame.SRCALPHA)

    # Get Max Speed Of All Particles
    max_speed = max([np.linalg.norm(particle.velocity) for particle in particles])
    max_speed = max_speed if max_speed != 0 else 1

    for particle in particles:

        # Map Speed Between 0 and 255
        color_value = np.clip(int(np.linalg.norm(particle.velocity) * 255 / max_speed), 0, 255)

        pygame.draw.circle(
            trans_surface,
            (color_value, 0, 255 - color_value),
            particle.position.astype(int),
            5,
        )

    screen.blit(trans_surface, (0, 0))


def main():
    pygame.init()
    screen = pygame.display.set_mode((IMAGE_SCALE, IMAGE_SCALE))
    pygame.display.set_caption("PerlinFlow Simulation")
    clock = pygame.time.Clock()

    particles = [
        Particle(bounds=[0, IMAGE_SCALE, 0, IMAGE_SCALE], mass=1, position=position)
        for position in np.random.rand(N_PARTICLES, 2) * IMAGE_SCALE
    ]

    # Main loop
    running = True
    time = 0
    dt = 0

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

        # Update Particles
        for particle in particles:
            grid_x = int(particle.position[0] / (IMAGE_SCALE / NOISE_SCALE))
            grid_y = int(particle.position[1] / (IMAGE_SCALE / NOISE_SCALE))

            # Ensure grid indices are within bounds
            grid_x = max(0, min(grid_x, NOISE_SCALE - 1))
            grid_y = max(0, min(grid_y, NOISE_SCALE - 1))

            force = (
                np.array([gradient[0][grid_x, grid_y], gradient[1][grid_x, grid_y]])
                * 1000
            )

            particle.update(dt, force=force)

        # Draw Noise
        drawNoise(screen, values)
        drawGradient(screen, gradient)
        draw_particles(screen, particles)

        pygame.display.set_caption(
            "PerlinFlow Simulation - FPS: {}".format(int(clock.get_fps()))
        )
        dt = clock.tick(60) / 1000
        time += dt
        pygame.display.flip()


if __name__ == "__main__":
    main()
