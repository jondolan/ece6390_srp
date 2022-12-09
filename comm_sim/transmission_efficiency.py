from math import radians, pi, log10

c = 299792458

def beam_pattern(angle):
    return 0

def transmission_efficiency(long, distance, earth, satellite):

    # model FSPL
    fspl            = 20*log10( (4*pi*distance*1000*satellite.frequency) / c )
    # print(fspl)
    # fspl            = 20**(fspl/20)
    # print(fspl)

    # model antenna pattern as a parabola
    gain_pattern    = 1 - (1/satellite.max_long_drift)**2 * radians(long)**2
    
    res             = gain_pattern

    return (0 if res < 0 else res)