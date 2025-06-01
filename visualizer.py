import pygame
import numpy as np
import math
from ball import Ball

# data visualization
class Visualizer():
    
    @staticmethod
    def draw_ball_data(screen, ball:Ball, font, font_color) -> None:
        if ball.pocketed:
            return
        
        x,y = ball.pos
        vx,vy = ball.vel
        mass = None # to be added

        speed = math.hypot(vx,vy)

        if speed > 0.01:
            angle_deg = (math.degrees(math.atan2(vy, vx)) + 360) % 360
            direction_str = f"dir={angle_deg:.1f}°"
        else:
            direction_str = "dir=0.0°"

        text_infos = [
            f"speed: {speed:.2f}",
            direction_str
        ]

        for i, text in enumerate(text_infos):
            label = font.render(text, True, font_color)
            screen.blit(label, (x + 10, y + i * 15))

        return 