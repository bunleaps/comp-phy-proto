import pygame
import numpy as np
import math
from ball import Ball

# data visualization
class Visualizer():
    
    @staticmethod
    def draw_ball_data(screen:pygame.Surface, ball:Ball, font:pygame.font.Font, font_color:pygame.color.Color) -> None:
        if ball.pocketed:
            return
        
        x,y = ball.pos
        vx,vy = ball.vel
        mass = ball.mass # to be added

        speed = math.hypot(vx,vy)
        momentum = speed * mass
        kinetic_energy = 0.5 * mass * speed ** 2

        if speed > 0.01:
            angle_deg = (math.degrees(math.atan2(vy, vx)) + 360) % 360
            direction_str = f"dir: {angle_deg:.1f}°"
        else:
            direction_str = "dir: 0.0°"

        text_infos = [
            f"speed: {speed:.2f}",
            f"mmtm: {momentum:.2f}",
            f"KE: {kinetic_energy:.2f}",
            direction_str
        ]

        for i, text in enumerate(text_infos):
            label = font.render(text, True, font_color)
            screen.blit(label, (x + 15, y + i * 15 - 20))

        return 