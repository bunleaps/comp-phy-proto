import pygame
import numpy as np
import sys

# Constants
WIDTH, HEIGHT = 800, 400
INFO_HEIGHT = 50
FPS = 60
BALL_RADIUS = 15
POCKET_RADIUS = 20

# Define pockets at global scope
POCKETS = [(0, 0), (WIDTH, 0), (0, HEIGHT), (WIDTH, HEIGHT)]  # Pocket positions

# Colors
GREEN = (0, 128, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
BROWN = (139, 69, 19)
PINK = (255, 192, 203)
GRAY = (128, 128, 128)

# Ball class (for the cue ball and colored balls)
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
                self.pos[1] = BALL_RADIUS  # Reset the position to just above the wall
                self.vel[1] *= -1  # Reverse vertical velocity
            elif self.pos[1] + BALL_RADIUS >= HEIGHT:  # Bottom wall
                self.pos[1] = HEIGHT - BALL_RADIUS  # Reset position to just above the bottom wall
                self.vel[1] *= -1  # Reverse vertical velocity

            if self.pos[0] - BALL_RADIUS <= 0:  # Left wall
                self.pos[0] = BALL_RADIUS  # Reset position to just after the left wall
                self.vel[0] *= -1  # Reverse horizontal velocity
            elif self.pos[0] + BALL_RADIUS >= WIDTH:  # Right wall
                self.pos[0] = WIDTH - BALL_RADIUS  # Reset position to just before the right wall
                self.vel[0] *= -1  # Reverse horizontal velocity

    def is_moving(self):
        return np.linalg.norm(self.vel) > 0.01

    def draw(self, screen):
        if not self.pocketed:
            pygame.draw.circle(screen, self.color, self.pos.astype(int), BALL_RADIUS)

# Set up pygame window
def setup_game():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT + INFO_HEIGHT))  # Add space for info
    pygame.display.set_caption("Pool Simulation")
    clock = pygame.time.Clock()
    return screen, clock

# Pocket detection logic
def is_in_pocket(ball):
    for px, py in POCKETS:  # Use the global POCKETS constant
        dist = np.linalg.norm(ball.pos - np.array([px, py]))
        if dist < POCKET_RADIUS:
            return True
    return False

# --- Collision Handling --- 
def resolve_collision(b1, b2): 
    if b1.pocketed or b2.pocketed: 
        return 
    # Calculate vector between ball centers: Δp = p₁ - p₂
    delta = b1.pos - b2.pos 
    # Calculate distance between balls: |Δp|
    dist = np.linalg.norm(delta) 
    if dist == 0 or dist > 2 * BALL_RADIUS: 
        return 
    
    # Calculate unit normal vector: n = Δp/|Δp|
    normal = delta / dist
    # Relative velocity vector: Δv = v₁ - v₂
    rel_vel = b1.vel - b2.vel 
    # Project relative velocity onto normal: Δv·n
    # If positive, balls are moving apart
    vel_along_normal = np.dot(rel_vel, normal)

    if vel_along_normal > 0:  # Balls are separating
        return 

    # Elastic collision impulse: J = -2m₁m₂Δv·n/(m₁+m₂)
    # Since m₁ = m₂ = 1, simplified to: J = -2(Δv·n)/2
    impulse = -2 * vel_along_normal / 2
    
    # Apply impulse: v₁' = v₁ + (J/m₁)n, v₂' = v₂ - (J/m₂)n
    b1.vel += impulse * normal
    b2.vel -= impulse * normal
    
    # Position correction to prevent overlap
    # x = (2R - |Δp|)/2 where R is ball radius
    overlap = 2 * BALL_RADIUS - dist
    # Move each ball by x/2 in opposite directions
    correction = normal * (overlap / 2)
    b1.pos += correction
    b2.pos -= correction

# --- Cue Drawing --- 
def draw_cue(screen, cue_ball, mouse_pos, dragging): 
    if not dragging or cue_ball.is_moving(): 
        return 
    # Calculate direction vector from mouse to ball: d = p_ball - p_mouse
    direction = cue_ball.pos - mouse_pos 
    # Limit cue length between 0 and 120 pixels: min(|d|, 120)
    length = np.clip(np.linalg.norm(direction), 0, 120) 
    if length < 10: 
        return 
    # Calculate unit vector for direction: d/|d|
    unit = direction / np.linalg.norm(direction) 
    # Calculate end point: p_end = p_ball + length * unit
    end_pos = cue_ball.pos + unit * length 
    pygame.draw.line(screen, BLACK, cue_ball.pos.astype(int), end_pos.astype(int), 4) 

# --- Restart Button --- 
def draw_restart_button(screen, font): 
    rect = pygame.Rect(WIDTH // 2 - 60, HEIGHT // 2 - 25, 120, 50) 
    pygame.draw.rect(screen, GRAY, rect) 
    pygame.draw.rect(screen, BLACK, rect, 2) 
    text = font.render("RESTART", True, BLACK) 
    screen.blit(text, (rect.x + 20, rect.y + 12)) 
    return rect

# Main game logic
def main():
    screen, clock = setup_game()

    # Balls setup
    balls = [
        Ball(200, 200, WHITE),  # Cue ball
        Ball(500, 180, RED),     # First colored ball
        Ball(540, 220, BLUE),    # Second colored ball
    ]
    cue_ball = balls[0]

    dragging = False
    font = pygame.font.SysFont("Arial", 16)
    game_over = False

    running = True
    while running:
        screen.fill(GREEN)  # Fill screen with green (table color)
        mouse_pos = np.array(pygame.mouse.get_pos())

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_over:
                    restart_rect = draw_restart_button(screen, font)
                    if restart_rect.collidepoint(event.pos):
                        # Reset game
                        balls = [
                            Ball(200, 200, WHITE),
                            Ball(500, 180, RED),
                            Ball(540, 220, BLUE),
                        ]
                        cue_ball = balls[0]
                        game_over = False
                elif not any(b.is_moving() for b in balls):
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
            # Check collisions with other balls
            for j, other_ball in enumerate(balls[i+1:]):
                resolve_collision(ball, other_ball)
            if is_in_pocket(ball):
                ball.pocketed = True

        # Check if game is over (all balls except cue ball are pocketed)
        if not game_over and all(b.pocketed for b in balls[1:]):
            game_over = True

        # Draw pockets
        for px, py in POCKETS:
            pygame.draw.circle(screen, BLACK, (px, py), POCKET_RADIUS)

        # Draw cue
        if not game_over:
            draw_cue(screen, cue_ball, mouse_pos, dragging)

        # Draw balls
        for ball in balls:
            ball.draw(screen)

        # Draw restart button if game is over
        if game_over:
            draw_restart_button(screen, font)

        # Draw diagnostics at the bottom
        pygame.draw.rect(screen, BLACK, (0, HEIGHT, WIDTH, INFO_HEIGHT))
        info = f"Cue Pos: {cue_ball.pos.astype(int)} Vel: {np.round(cue_ball.vel, 2)}"
        screen.blit(font.render(info, True, WHITE), (10, HEIGHT + 15))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
