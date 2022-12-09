from math import atan2, pi

from .clipped_sinusoidal_off_90 import controller as clipped_sinusoidal_off_90

# def controller(r, v, t, parameters, satellite):

#     range   = parameters.sidereal_day*8
#     cutoff  = parameters.sidereal_day*3.75

#     if (t % range) < cutoff:
#         return sinusoidal_off_90(r, v, t, parameters, satellite)
#     else:
#         return negative_sinusoidal_off_90(r, v, t, parameters, satellite)

def controller(r, v, t, parameters, satellite):

    range   = parameters.sidereal_day*8
    cutoff  = parameters.sidereal_day*7.3

    if (t % range) < cutoff:
        return 0
    else:
        return clipped_sinusoidal_off_90(r, v, t, parameters, satellite)