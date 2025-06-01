import pygame
import numpy as np
import math
from ball import Ball

# data visualization
class Visualizer():
    
    @staticmethod
    def draw_ball_data(
        screen:pygame.Surface,
        ball:Ball, 
        font:pygame.font.Font, 
        font_color:pygame.color.Color
    ) -> None:
        
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
    
    @staticmethod
    def draw_velocity_vector(
        screen: pygame.Surface,
        ball: Ball,
        color: pygame.Color = (0,255,0),
        scale: float = 20,
        arrow_size: int = 5,
    ) -> None:
        if ball.pocketed:
            return
        
        x, y = ball.pos
        vx, vy = ball.vel
        speed = math.hypot(vx, vy)

        if speed < 0.01:
            return
        
        end_x = x + vx * scale
        end_y = y + vy * scale

        # Velocity line
        pygame.draw.line(
            screen,
            color,
            (int(x), int(y)),
            (int(end_x), int(end_y)),
            2
        )

        angle = math.atan2(vy, vx)
        left = (
            end_x - arrow_size * math.cos(angle - math.pi / 6),
            end_y - arrow_size * math.sin(angle - math.pi / 6)
        )
        right = (
            end_x - arrow_size * math.cos(angle + math.pi / 6),
            end_y - arrow_size * math.sin(angle + math.pi / 6)
        )

        # Arrowhead
        pygame.draw.polygon(
            screen,
            color,
            [
                (int(end_x), int(end_y)),
                (int(left[0]), int(left[1])),
                (int(right[0]), int(right[1]))
            ]
        )

        ...