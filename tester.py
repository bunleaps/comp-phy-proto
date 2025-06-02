import pygame
import numpy as np
import sys
from constants import *
from ball import Ball
from physics import resolve_inelastic_collision, is_in_pocket
from ui import draw_cue, draw_restart_button, draw_hit_spot_selector
from utils import Visualizer
from graph import Graph

class PoolTester:
    def __init__(self, direction, strength, material=('elastic','elastic'),visualize=False):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT + INFO_HEIGHT))
        pygame.display.set_caption("Pool Simulation Tester")
        self.clock = pygame.time.Clock()
        self.visualize = visualize
        self.col_sound = pygame.mixer.Sound("assets/audio/col-1.wav")

        # Graph
        self.graph = Graph(2)

        # Setup balls same as main (or customize)
        INITIAL_SETUP = [
            (WIDTH/2, HEIGHT/2, WHITE, material[0]),  # Cue ball
            (650, HEIGHT/2, RED, material[1]),      
        ]
        self.balls = [Ball(*pos) for pos in INITIAL_SETUP]
        self.cue_ball = self.balls[0]

        # Apply initial impulse to cue ball
        dir_norm = direction / np.linalg.norm(direction)
        impulse_magnitude = strength
        impulse = dir_norm * impulse_magnitude
        self.cue_ball.vel += impulse / self.cue_ball.mass

        # For visualization and debugging
        self.font = pygame.font.SysFont("Arial", 16)
        self.elapsed_time = 0.0
        self.running = True

    def run(self):
        graph_interval = GRAPH_INTERVAL
        last_graph = 0.0
        flag = False

        while self.running:
            dt = self.clock.tick(FPS) / 1000
            self.elapsed_time += dt
            last_graph += dt
            self.handle_events()

            self.screen.fill(GREEN)

            if not flag and self.balls[0].speed > 0:
                print(self.balls[0].speed)
                flag = True

            # Update balls and collisions
            for i, ball in enumerate(self.balls):
                ball.move(self.col_sound)  # Pass None if you don't want sounds here
                for other_ball in self.balls[i+1:]:
                    delta_pos = ball.pos - other_ball.pos
                    dist = np.linalg.norm(delta_pos)
                    if dist <= 2 * BALL_RADIUS:
                        # Run diagnostics + collision resolution
                        self.test_collision_diagnostics(ball, other_ball, resolve_inelastic_collision)
                if is_in_pocket(ball):
                    ball.pocketed = True

            # Draw balls
            for ball in self.balls:
                ball.draw(self.screen)

            # Velocity vectors and data
            if self.visualize:
                for ball in self.balls:
                    Visualizer.draw_ball_data(self.screen, ball, self.font, WHITE)
                    Visualizer.draw_velocity_vector(self.screen, ball, YELLOW, 15, 4)

            # Update graph
            if last_graph >= graph_interval:
                self.graph.update(self.elapsed_time, self.balls)
                last_graph -= graph_interval

            # Simple exit condition: stop after 10 seconds or all balls stopped
            all_stopped = all(ball.speed < 0.01 for ball in self.balls if not ball.pocketed)
            if self.elapsed_time > 15 and all_stopped:
                print(f"Test ended at time={self.elapsed_time:.2f}s")
                self.running = False

            pygame.display.flip()

        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def calculate_ke_loss(self, ball1, ball2, before_vel1, before_vel2):
        """
        Calculates kinetic energy lost in a collision.
        """
        ke_before = 0.5 * ball1.mass * np.dot(before_vel1, before_vel1) + \
                    0.5 * ball2.mass * np.dot(before_vel2, before_vel2)
        ke_after = 0.5 * ball1.mass * np.dot(ball1.vel, ball1.vel) + \
                0.5 * ball2.mass * np.dot(ball2.vel, ball2.vel)

        ke_lost = ke_before - ke_after

        return {
            'before': ke_before,
            'after': ke_after,
            'lost': ke_lost
        }
    
    def test_collision_diagnostics(self, ball1, ball2, resolve_collision_fn):
        """
        Tests momentum change and kinetic energy loss for a ball collision.
        """
        # Pre-collision velocities
        v1_before = ball1.vel.copy()
        v2_before = ball2.vel.copy()

        # Resolve collision
        resolve_collision_fn(ball1, ball2, None)

        # Kinetic energy diagnostics
        ke_result = self.calculate_ke_loss(ball1, ball2, v1_before, v2_before)
        print(f"KE before: {ke_result['before']:.3f}")
        print(f"KE after:  {ke_result['after']:.3f}")
        print(f"KE lost:   {ke_result['lost']:.3f}")
        print("=============================")

        return ke_result


if __name__ == "__main__":
    direction = np.array([1.0, 0.0])
    strength = 1
    material = ('ivory','ivory')
    tester = PoolTester(direction, strength, material, visualize=True)
    tester.run()
