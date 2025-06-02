import numpy as np
from constants import BALL_RADIUS, POCKET_RADIUS, POCKETS, MATERIAL_COR

def resolve_collision(b1, b2, col_sound): 
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
    
    if col_sound is not None:
        volume = min(1.0, abs(vel_along_normal) / 20)  # volume scaled by collision speed
        col_sound.set_volume(volume)
        col_sound.play()

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

def resolve_inelastic_collision(b1, b2, col_sound):
    if b1.pocketed or b2.pocketed: 
        return 

    delta = b1.pos - b2.pos 
    dist = np.linalg.norm(delta) 
    if dist == 0 or dist > 2 * BALL_RADIUS: 
        return 
    
    normal = delta / dist
    rel_vel = b1.vel - b2.vel 
    vel_along_normal = np.dot(rel_vel, normal)

    if vel_along_normal > 0:
        return 

    # Sound scaled to impact speed
    if col_sound is not None:
        volume = min(1.0, abs(vel_along_normal) / 20)
        col_sound.set_volume(volume)
        col_sound.play()

    m1, m2 = b1.mass, b2.mass
    total_mass = m1 + m2
    if total_mass <= 0:
        return

    # Get restitution from materials
    e1 = MATERIAL_COR.get(b1.material, 0.5)
    e2 = MATERIAL_COR.get(b2.material, 0.5)
    cor = min(e1, e2)  # conservative estimate: lower COR dominates

    # Compute impulse scalar (based on COR)
    impulse = -(1 + cor) * vel_along_normal / (1/m1 + 1/m2)
    impulse_vec = impulse * normal

    b1.vel += impulse_vec / m1
    b2.vel -= impulse_vec / m2

    # Correct overlap
    overlap = 2 * BALL_RADIUS - dist
    correction = normal * (overlap / 2)
    b1.pos += correction
    b2.pos -= correction

def is_in_pocket(ball):
    for px, py in POCKETS:
        dist = np.linalg.norm(ball.pos - np.array([px, py]))
        if dist < POCKET_RADIUS:
            return True
    return False