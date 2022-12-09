from math import atan2, sin, cos, pi
from numpy import zeros, concatenate, array, sqrt, where
from scipy.integrate import solve_ivp

from .sun import sun_angle

thetas = []

def propagate(r0, v0, ts, parameters, earth, sun, satellite):
    global thetas

    rs          = zeros((len(ts),3))
    vs          = zeros((len(ts),3))
    thetas      = []

    y0      = concatenate((r0, v0))

    # res = odeint(two_body_with_srp, y0, ts,
    #                 args=(earth, sun, satellite, controller),
    #                 rtol=1e-13,
    #                 atol=1e-13)
    # Nx6 array
    # for i in range(0, len(res)):
    #     rs[i] = res[i][:3]
    #     vs[i] = res[i][3:]

    res = solve_ivp(two_body_with_srp,
                    (ts[0], ts[-1]),
                    y0,
                    dense_output=True,
                    t_eval=ts,
                    # events=control,
                    args=(parameters, earth, sun, satellite),
                    atol=1e-10,
                    rtol=1e-10)

    # 6xN array
    ys = res.y
    for i in range(0, len(ts)):
        rs[i] = ys[:3,i]
        vs[i] = ys[3:,i]

    # prop = ode(two_body_with_srp,
    #             args=(earth, sun, satellite, controller))
    # prop.set_initial_value(y0)
    # for i in range(0, ts):
    #     res = prop.integrate(ts[i])
    #     print(res)

    return (rs, vs, thetas)

def two_body_with_srp(t, y, parameters, earth, sun, satellite):
    global thetas

    mu              = earth.mu
    p               = sun.p_km
    e_solar         = satellite.epsilon_solar
    e_comm          = satellite.epsilon_comm

    r               = y[:3]
    v               = y[3:]

    incidence_command   = satellite.controller(r, v, t, parameters, satellite)
    satellite.incidence = incidence_command
    thetas.append((t,incidence_command))

    r_norm          = sqrt(r@r)
    # print(r/r_norm)

    # two body propagation
    two_body        = (-mu/r_norm**3) * r


    # TODO: account for sun direction
    # print(sun_angle( t, sun))
    

        # Montenbruck and Gill
    solar_srp_direction = array(
        [   (1-e_solar) * cos(incidence_command) + 2 * e_solar * cos(incidence_command)**2, \
            2 * e_solar * sin(incidence_command) * cos(incidence_command), \
            0
        ])

    orbit_theta = atan2(r[1], r[0])
    if pi/2 < orbit_theta < pi:
        comm_angle = pi-orbit_theta
    elif -pi < orbit_theta < -pi/2:
        comm_angle = abs(orbit_theta)-pi
    else:
        comm_angle = orbit_theta

    # correct for sun rotation


    comm_srp_direction = array(
        [   (1-e_comm) * cos(comm_angle) + 2 * e_comm * cos(comm_angle)**2, \
            2 * e_comm * sin(comm_angle) * cos(comm_angle), \
            0
        ])

    srp             = (-p * satellite.area_to_mass_solar * solar_srp_direction) + \
                        (-p * satellite.area_to_mass_comm * comm_srp_direction)
    # srp=(-p * satellite.area_to_mass_comm * comm_srp_direction)
    


    # TODO: comm dish SRP
    # theta_comm = 

    total = two_body + srp

    return concatenate((v, total))