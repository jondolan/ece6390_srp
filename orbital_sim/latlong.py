from math import asin, atan2, cos, sin, degrees
from numpy import array, sqrt, dot


def r_to_latlong(t, r, earth):

    # print(r)
    omega = earth.omega

    r_ecef  = dot(M3r(omega*t), r)
    r_norm = sqrt(r_ecef@r_ecef)
    r_ecef  = r_ecef / r_norm

    lat = degrees(asin(r_ecef[2]))
    long = degrees(atan2(r_ecef[1], r_ecef[0]))
    
    return (lat, long)


def M3r(angle):

    c = cos(angle)
    s = sin(angle)

    return array([[c, s, 0], [-s, c, 0], [0, 0, 1]])