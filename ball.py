import pygame
import numpy as np
from constants import BALL_RADIUS, WIDTH, HEIGHT, MASS, FRICTION, WALL_RESTITUTION
import math

class Ball:
    def __init__(self, x, y, color, material):
        self.pos = np.array([x, y], dtype=float)
        self.vel = np.array([0, 0], dtype=float)
        self.speed = 0
        self.color = color
        self.mass = MASS # Ensure mass is a float
        self.material = material
        self.pocketed = False

    def move(self, col_sound):
        if not self.pocketed:
            # Move the ball based on its velocity
            self.pos += self.vel
            self.vel *= FRICTION  # Friction
            self.speed = math.hypot(self.vel[0],self.vel[1])

            # volume adjustment
            volume = min(1.0, self.speed / 20)
            

            # Wall collisions (left, right, top, bottom)
            if self.pos[1] - BALL_RADIUS <= 0:  # Top wall
                self.pos[1] = BALL_RADIUS
                self.vel[1] *= -WALL_RESTITUTION
                col_sound.set_volume(volume)
                col_sound.play()

            elif self.pos[1] + BALL_RADIUS >= HEIGHT:  # Bottom wall
                self.pos[1] = HEIGHT - BALL_RADIUS
                self.vel[1] *= -WALL_RESTITUTION
                col_sound.set_volume(volume)
                col_sound.play()

            if self.pos[0] - BALL_RADIUS <= 0:  # Left wall
                self.pos[0] = BALL_RADIUS
                self.vel[0] *= -WALL_RESTITUTION
                col_sound.set_volume(volume)
                col_sound.play()
                
            elif self.pos[0] + BALL_RADIUS >= WIDTH:  # Right wall
                self.pos[0] = WIDTH - BALL_RADIUS
                self.vel[0] *= -WALL_RESTITUTION
                col_sound.set_volume(volume)
                col_sound.play()
        else:
            self.vel *= 0
            self.speed = 0

    def is_moving(self):
        return np.linalg.norm(self.vel) > 0.01

    def draw(self, screen):
        if not self.pocketed:
            pygame.draw.circle(screen, self.color, self.pos.astype(int), BALL_RADIUS)