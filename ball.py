import pygame
import numpy as np
from constants import BALL_RADIUS, WIDTH, HEIGHT

class Ball:
    def __init__(self, x, y, color):
        self.pos = np.array([x, y], dtype=float)
        self.vel = np.array([0, 0], dtype=float)
        self.color = color
        self.pocketed = False

    def move(self):
        if not self.pocketed:
            # Move the ball based on its velocity
            self.pos += self.vel
            self.vel *= 0.99  # Friction

            # Wall collisions (left, right, top, bottom)
            if self.pos[1] - BALL_RADIUS <= 0:  # Top wall
                self.pos[1] = BALL_RADIUS
                self.vel[1] *= -1
            elif self.pos[1] + BALL_RADIUS >= HEIGHT:  # Bottom wall
                self.pos[1] = HEIGHT - BALL_RADIUS
                self.vel[1] *= -1

            if self.pos[0] - BALL_RADIUS <= 0:  # Left wall
                self.pos[0] = BALL_RADIUS
                self.vel[0] *= -1
            elif self.pos[0] + BALL_RADIUS >= WIDTH:  # Right wall
                self.pos[0] = WIDTH - BALL_RADIUS
                self.vel[0] *= -1

    def is_moving(self):
        return np.linalg.norm(self.vel) > 0.01

    def draw(self, screen):
        if not self.pocketed:
            pygame.draw.circle(screen, self.color, self.pos.astype(int), BALL_RADIUS)