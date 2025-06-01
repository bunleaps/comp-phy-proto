import pygame
import numpy as np
from constants import (WIDTH, HEIGHT, BLACK, GRAY, MAXIMUM_FORCE, WHITE,
                     HIT_SPOT_SELECTOR_CENTER_X, HIT_SPOT_SELECTOR_CENTER_Y, HIT_SPOT_BG_RADIUS, HIT_SPOT_BUTTON_RADIUS, HIT_SPOT_BUTTON_OFFSET, HIT_SPOT_EFFECTS)

def draw_cue(screen, cue_ball, mouse_pos, dragging): 
    if not dragging or cue_ball.is_moving(): 
        return 
    # Calculate direction vector from mouse to ball: d = p_ball - p_mouse
    direction = cue_ball.pos - mouse_pos 
    # Limit cue length between 0 and 120 pixels: min(|d|, 120)
    length = np.clip(np.linalg.norm(direction), 0, MAXIMUM_FORCE) 
    if length < 10: 
        return 
    # Calculate unit vector for direction: d/|d|
    unit = direction / np.linalg.norm(direction) 
    # Calculate end point: p_end = p_ball + length * unit
    end_pos = cue_ball.pos + unit * length 
    pygame.draw.line(screen, BLACK, cue_ball.pos.astype(int), end_pos.astype(int), 4) 

def draw_restart_button(screen, font): 
    rect = pygame.Rect(WIDTH // 2 - 60, HEIGHT // 2 - 25, 120, 50) 
    pygame.draw.rect(screen, GRAY, rect) 
    pygame.draw.rect(screen, BLACK, rect, 2) 
    text = font.render("RESTART", True, BLACK) 
    screen.blit(text, (rect.x + 20, rect.y + 12)) 
    return rect

def draw_hit_spot_selector(screen, font, selected_spot_key):
    """Draws the hit spot selector UI and returns a dict of spot_key: pygame.Rect."""
    base_x, base_y = HIT_SPOT_SELECTOR_CENTER_X, HIT_SPOT_SELECTOR_CENTER_Y
    
    # Draw background for the selector
    pygame.draw.circle(screen, GRAY, (base_x, base_y), HIT_SPOT_BG_RADIUS)
    pygame.draw.circle(screen, BLACK, (base_x, base_y), HIT_SPOT_BG_RADIUS, 1)

    clickable_spots = {}

    for spot_key, props in HIT_SPOT_EFFECTS.items():
        rel_x, rel_y, label, _ = props
        
        spot_center_x = base_x + rel_x * HIT_SPOT_BUTTON_OFFSET
        spot_center_y = base_y + rel_y * HIT_SPOT_BUTTON_OFFSET
        
        spot_rect = pygame.Rect(
            spot_center_x - HIT_SPOT_BUTTON_RADIUS,
            spot_center_y - HIT_SPOT_BUTTON_RADIUS,
            2 * HIT_SPOT_BUTTON_RADIUS,
            2 * HIT_SPOT_BUTTON_RADIUS
        )
        clickable_spots[spot_key] = spot_rect

        color = WHITE if spot_key == selected_spot_key else BLACK
        pygame.draw.circle(screen, color, (spot_center_x, spot_center_y), HIT_SPOT_BUTTON_RADIUS)
        if spot_key == selected_spot_key: # Border for selected
             pygame.draw.circle(screen, BLACK, (spot_center_x, spot_center_y), HIT_SPOT_BUTTON_RADIUS, 1)
    return clickable_spots