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

    if vel_along_normal > 0:  # Balls are already separating
        return 

    # Get masses
    m1 = b1.mass
    m2 = b2.mass

    # Prevent division by zero if total mass is zero (though masses should be positive)
    total_mass = m1 + m2
    if total_mass <= 0:
        return

    # Calculate new velocities after 1D elastic collision along the normal vector
    # v1_new = v1 - (2 * m2 / (m1 + m2)) * vel_along_normal * normal
    # v2_new = v2 + (2 * m1 / (m1 + m2)) * vel_along_normal * normal
    # (where vel_along_normal = dot(v1 - v2, normal))
    b1.vel -= (2 * m2 / total_mass) * vel_along_normal * normal
    b2.vel += (2 * m1 / total_mass) * vel_along_normal * normal

    # Position correction to prevent overlap (simple method, independent of mass for now)
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