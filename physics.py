import numpy as np
from constants import BALL_RADIUS, POCKET_RADIUS, POCKETS

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

def is_in_pocket(ball):
    for px, py in POCKETS:
        dist = np.linalg.norm(ball.pos - np.array([px, py]))
        if dist < POCKET_RADIUS:
            return True
    return False