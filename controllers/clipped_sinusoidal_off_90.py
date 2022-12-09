from .sinusoidal_off_90 import controller as sinusoidal_off_90

def controller(r, v, t, parameters, satellite):

    angle = sinusoidal_off_90(r, v, t, parameters, satellite)

    if angle >= satellite.clip:
        return satellite.clip
    
    if angle <= -satellite.clip:
        return -satellite.clip

    return angle
