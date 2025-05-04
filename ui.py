import pygame
import numpy as np
from constants import WIDTH, HEIGHT, BLACK, GRAY

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

def draw_restart_button(screen, font): 
    rect = pygame.Rect(WIDTH // 2 - 60, HEIGHT // 2 - 25, 120, 50) 
    pygame.draw.rect(screen, GRAY, rect) 
    pygame.draw.rect(screen, BLACK, rect, 2) 
    text = font.render("RESTART", True, BLACK) 
    screen.blit(text, (rect.x + 20, rect.y + 12)) 
    return rect