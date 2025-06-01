import pygame
import numpy as np
import sys
from constants import *
from ball import Ball
from physics import resolve_collision, is_in_pocket
from ui import draw_cue, draw_restart_button, draw_hit_spot_selector
from utils import Visualizer
from graph import Graph

def setup_game():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT + INFO_HEIGHT))
    pygame.display.set_caption("Pool Simulation")
    clock = pygame.time.Clock()
    return screen, clock

def setup_visualizations() -> Graph:
    graph = Graph(3)
    return graph

def main():
    screen, clock = setup_game()
    graph = setup_visualizations()
    graph_interval = GRAPH_INTERVAL
    last_graph = 0.0

    elapsed_time = 0.0

    visualize = True

    # Balls setup with (x, y, color, mass)
    INITIAL_POSITIONS = [
        (200, 200, WHITE, 1.0),  # Cue ball
        (50, 50, RED, 1.0),     # First colored ball near top-left pocket
        (750, 50, BLUE, 1.0),    # Second colored ball near top-right pocket
    ]

    balls = [Ball(*pos) for pos in INITIAL_POSITIONS]
    cue_ball = balls[0]

    dragging = False
    font = pygame.font.SysFont("Arial", 16)
    game_over = False
    selected_hit_spot = "CENTER"  # Default hit spot

    running = True
    while running:
        screen.fill(GREEN)
        mouse_pos = np.array(pygame.mouse.get_pos())

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    visualize = not visualize

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_over:
                    restart_rect = draw_restart_button(screen, font)
                    if restart_rect.collidepoint(event.pos):
                        balls = [Ball(*pos) for pos in INITIAL_POSITIONS]
                        cue_ball = balls[0]
                        game_over = False
                        selected_hit_spot = "CENTER" # Reset hit spot
                else: # Not game over, check for other interactions
                    temp_clickable_spots = draw_hit_spot_selector(pygame.Surface((0,0)), font, selected_hit_spot) # Dummy surface
                    
                    clicked_on_spot_selector = False
                    for spot_key, rect in temp_clickable_spots.items():
                        if rect.collidepoint(event.pos):
                            selected_hit_spot = spot_key
                            clicked_on_spot_selector = True
                            break
                    
                    if not clicked_on_spot_selector and not any(b.is_moving() for b in balls if not b.pocketed) and not cue_ball.pocketed:
                        dragging = True # Start dragging for a shot

            elif event.type == pygame.MOUSEBUTTONUP:
                if dragging:
                    direction = cue_ball.pos - mouse_pos
                    dist = np.linalg.norm(direction)
                    if dist > 5:  # Minimum drag distance to apply force
                        angle_offset = HIT_SPOT_EFFECTS[selected_hit_spot][3]
                        
                        if dist == 0: # Avoid division by zero if somehow dist is zero
                            unit_direction = np.array([0.0,0.0])
                        else:
                            unit_direction = direction / dist
                        
                        # Rotate the unit_direction vector
                        initial_angle = np.arctan2(unit_direction[1], unit_direction[0])
                        modified_angle = initial_angle + angle_offset
                        
                        modified_unit_direction = np.array([np.cos(modified_angle), np.sin(modified_angle)])
                        
                        # Impulse magnitude is proportional to drag distance
                        impulse_magnitude = dist * CUE_STRENGTH_COEFFICIENT
                        applied_impulse = modified_unit_direction * impulse_magnitude
                        
                        cue_ball.vel += applied_impulse / cue_ball.mass
                dragging = False

        # Ball movement and collision
        for i, ball in enumerate(balls):
            ball.move()
            for other_ball in balls[i+1:]:
                resolve_collision(ball, other_ball)
            if is_in_pocket(ball):
                ball.pocketed = True

        # Check game over conditions
        if not game_over and (cue_ball.pocketed or all(ball.pocketed for ball in balls[1:])):
            # Auto-restart after a short delay
            pygame.time.delay(1000)  # 1 second delay
            balls = [Ball(*pos) for pos in INITIAL_POSITIONS]
            cue_ball = balls[0]
            selected_hit_spot = "CENTER" # Reset hit spot

        # Draw game elements
        for px, py in POCKETS:
            pygame.draw.circle(screen, BLACK, (px, py), POCKET_RADIUS)

        if not game_over:
            draw_cue(screen, cue_ball, mouse_pos, dragging)

        for ball in balls:
            ball.draw(screen)

        if game_over:
            draw_restart_button(screen, font)

        # Draw diagnostics
        if visualize:
            for ball in balls:
                Visualizer.draw_ball_data(screen, ball, font, WHITE)
                Visualizer.draw_velocity_vector(screen, ball, YELLOW, 15, 4)

        pygame.draw.rect(screen, BLACK, (0, HEIGHT, WIDTH, INFO_HEIGHT))
        info_text_pos_y = HEIGHT + 10
        info = f"Cue Pos: {cue_ball.pos.astype(int)} Vel: {np.round(cue_ball.vel, 2)} Spot: {HIT_SPOT_EFFECTS[selected_hit_spot][2]}"
        screen.blit(font.render(info, True, WHITE), (10, info_text_pos_y))
        
        draw_hit_spot_selector(screen, font, selected_hit_spot) # Draw the selector UI

        # Updates graph
        if last_graph >= graph_interval:
            graph.update(elapsed_time, balls)
            last_graph -= graph_interval

        dt = clock.tick(FPS) / 1000 #milliseconds
        elapsed_time += dt
        last_graph += dt

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
