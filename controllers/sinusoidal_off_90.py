from math import atan2, pi

def controller(r, v, t, parameters, satellite):
    angle = atan2(r[1], r[0])

    # 1st quad
    if 0 < angle <= pi/2:
        angle = pi/2-angle

    # 2nd quad
    elif pi/2 < angle <= pi:
        angle = pi/2-angle

    # 3rd quad
    elif -pi < angle <= -pi/2:
        angle = angle+pi/2

    # 4th quad
    elif -pi/2 < angle <= 0:
        angle = angle+pi/2

    return angle
