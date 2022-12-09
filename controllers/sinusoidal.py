from math import atan2, pi

def controller(r, v, t, parameters, satellite):
#    return atan(r[1]/r[0])
    angle = atan2(r[1], r[0])
    if pi/2 < angle < pi:
        return pi-angle
    elif -pi < angle < -pi/2:
        return abs(angle)-pi
    else:
        return angle