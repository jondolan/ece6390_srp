from .sinusoidal_off_90 import controller as sinusoidal_off_90

def controller(r, v, t, parameters, satellite):

    return -sinusoidal_off_90(r, v, t, parameters, satellite)
