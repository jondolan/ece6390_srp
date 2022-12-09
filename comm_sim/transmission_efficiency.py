from math import degrees, pi, log10

c = 299792458

def beam_pattern(angle):
    return 0

def transmission_efficiency(drift, distance, earth, satellite):

    # model FSPL
    # fspl            = 20*log10( (4*pi*distance*1000*satellite.frequency) / c )
    # print(fspl)
    # fspl            = 20**(fspl/20)
    # print(fspl)

    # model antenna pattern as a parabola
    gain_pattern    = 1 - (5/(degrees(satellite.max_long_drift))) * drift**2

    # outside the box
    if abs(drift) > degrees(satellite.max_long_drift):
        return 0
    else:
        return gain_pattern