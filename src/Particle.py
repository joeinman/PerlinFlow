import numpy as np

MAX_SPEED = 1000

class Particle:
    def __init__(self, bounds, mass=1, position=np.zeros(2), velocity=np.zeros(2)):
        self.bounds = bounds
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.acceleration = np.zeros(2)
        self.prev_position = position

    def update(self, dt, force=np.zeros(2)):
        self.prev_position = self.position.copy()
        self.acceleration = force / self.mass
        self.velocity += self.acceleration * dt
        self.velocity = np.clip(self.velocity, -MAX_SPEED, MAX_SPEED)

        self.acceleration = np.zeros(2)

        # Bounds Is Of The Form (x_min, x_max, y_min, y_max)
        # Wrap Around
        if self.position[0] > self.bounds[1]:
            self.position[0] = self.bounds[0]
        elif self.position[0] < self.bounds[0]:
            self.position[0] = self.bounds[1]

        if self.position[1] > self.bounds[3]:
            self.position[1] = self.bounds[2]
        elif self.position[1] < self.bounds[2]:
            self.position[1] = self.bounds[3]

        self.position += self.velocity * dt
