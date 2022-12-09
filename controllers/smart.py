from math import atan2, pi

from .sinusoidal_off_90 import controller as sinusoidal_off_90
from .negative_sinusoidal_off_90 import controller as negative_sinusoidal_off_90
from .sinusoidal import controller as sinusoidal

# def controller(r, v, t, parameters, satellite):

#     range   = parameters.sidereal_day*8
#     cutoff  = parameters.sidereal_day*3.75

#     if (t % range) < cutoff:
#         return sinusoidal_off_90(r, v, t, parameters, satellite)
#     else:
#         return negative_sinusoidal_off_90(r, v, t, parameters, satellite)

def controller(r, v, t, parameters, satellite):

    # change   = parameters.sidereal_day*42
    # change2  = parameters.sidereal_day*55

    range   = parameters.sidereal_day*8
    cutoff  = parameters.sidereal_day*7.35

    # if t < change:
    #     cutoff  = parameters.sidereal_day*3.75
    # elif t < change2:
    #     cutoff  = parameters.sidereal_day*5
    # else:
    #     cutoff  = parameters.sidereal_day*3.75


    if (t % range) < cutoff:
        return 0
    else:
        return sinusoidal_off_90(r, v, t, parameters, satellite)