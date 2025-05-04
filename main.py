import pygame
import numpy as np
import sys
from constants import *
from ball import Ball
from physics import resolve_collision, is_in_pocket
from ui import draw_cue, draw_restart_button

def setup_game():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT + INFO_HEIGHT))
    pygame.display.set_caption("Pool Simulation")
    clock = pygame.time.Clock()
    return screen, clock

def main():
    screen, clock = setup_game()

    # Balls setup with easy pocket positions
    INITIAL_POSITIONS = [
        (200, 200, WHITE),  # Cue ball
        (50, 50, RED),     # First colored ball near top-left pocket
        (750, 50, BLUE),    # Second colored ball near top-right pocket
    ]
    
    balls = [Ball(*pos) for pos in INITIAL_POSITIONS]
    cue_ball = balls[0]

    dragging = False
    font = pygame.font.SysFont("Arial", 16)
    game_over = False

    running = True
    while running:
        screen.fill(GREEN)
        mouse_pos = np.array(pygame.mouse.get_pos())

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_over:
                    restart_rect = draw_restart_button(screen, font)
                    if restart_rect.collidepoint(event.pos):
                        balls = [Ball(*pos) for pos in INITIAL_POSITIONS]
                        cue_ball = balls[0]
                        game_over = False
                elif not any(b.is_moving() for b in balls if not b.pocketed) and not cue_ball.pocketed:  # Only check non-pocketed balls
                    dragging = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if dragging:
                    direction = cue_ball.pos - mouse_pos
                    if np.linalg.norm(direction) > 5:
                        cue_ball.vel += direction * 0.05
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
        pygame.draw.rect(screen, BLACK, (0, HEIGHT, WIDTH, INFO_HEIGHT))
        info = f"Cue Pos: {cue_ball.pos.astype(int)} Vel: {np.round(cue_ball.vel, 2)}"
        screen.blit(font.render(info, True, WHITE), (10, HEIGHT + 15))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
