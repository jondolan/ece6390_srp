from math import degrees, radians, pi, ceil
from numpy import linspace, zeros, argmax
import matplotlib.pyplot as plt

# import simulation propagation logic
from orbital_sim import run

# import controllers
from controllers import *

# SIMULATION PARAMETERS

## CONSTANTS
class Earth:
    mu                  = 398600.4415                   # km^3/s^2
    sidereal_day        = 86164.0905                    # sidereal day in seconds
    omega               = 2.0*pi / sidereal_day         # earth rotation rate, rad/sec
    

class Sun:
    p                   = 4.560e-6                      # solar radiation pressure at 1AU (N/m^2)
    sidereal_year       = Earth.sidereal_day*365.256    # sidereal year
    omega               = 2.0*pi / sidereal_year        # earth rotation about sun, rad/sec 

## SATELLITE
class Satellite:
    period              = Earth.sidereal_day            # geostationary orbit, period = 1 sidereal day
    initial_r           = ((period / (2*pi))**2 * Earth.mu)**(1/3)
    max_long_drift      = radians(0.1)
    peak_power          = 1                             # peak power generation, W
    frequency           = 4e9                           # transmission frequency in Hz

    epsilon_solar       = 0.21                          # reflectivity coef for solar panel
    area_density_solar  = 5.0                           # mass to area ratio for solar panel, kg/m^2
    epsilon_comm        = 0.3                           # reflectivity coef for high gain antenna
    area_density_comm   = 5.0                           # mass to area ratio for comm antenna, kg/m^2

class Parameters:
    days                = 30                            # days to run the sim
    sidereal_day        = Earth.sidereal_day
    samples             = 8000                          # number of samples of the orbit to take
    plot                = True

class MonteCarlo:
    theta_resolution    = 1.0                           # resolution for theta recordings, deg
    theta_range         = [-90, 90]                     # range for theta, [min, max] deg


# SETUP SIM

## generate theta list
t_min           = MonteCarlo.theta_range[0]
t_max           = MonteCarlo.theta_range[1]
num_thetas      = ceil((t_max-t_min)/MonteCarlo.theta_resolution)+1
thetas          = linspace(t_min, t_max, num_thetas)
# print(thetas)

## pregenerate power generation and transmission efficiency arrays
generation      = zeros(num_thetas)

# for each solar incidence angle
# for i in range(0,num_thetas):
#     Satellite.initial_incidence = radians(thetas[i])
#     generation[i] = run(    
#         earth=Earth,
#         sun=Sun,
#         satellite=Satellite,
#         parameters=Parameters,
#         controller=static_incidence
#     )
#     print(f"{thetas[i]} deg: {generation[i]}")


Satellite.controller    = sinusoidal_off_90
Satellite.incidence     = radians(0.0)
generation = run(    
    earth=Earth,
    sun=Sun,
    satellite=Satellite,
    parameters=Parameters,
)
print(generation)

# plt.plot(thetas, generation)
# plt.title(f"Max power generation at theta={round(thetas[argmax(generation)],2)} deg")
# plt.xlim([t_min,t_max])
# plt.gca().set_ylim(bottom=0.0)
# plt.savefig("/run/output/curve.png")
# plt.close()