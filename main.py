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
    samples             = 5000                          # number of samples of the orbit to take


# # INCIDENCE 0
# Satellite.controller    = static_incidence
# Satellite.incidence     = radians(0.0)
# test = run(    
#     earth=Earth,
#     sun=Sun,
#     satellite=Satellite,
#     parameters=Parameters,
#     output="/run/output/static_0.png"
# )

# # INCIDENCE 45
# Satellite.controller    = static_incidence
# Satellite.incidence     = radians(60.0)
# test = run(    
#     earth=Earth,
#     sun=Sun,
#     satellite=Satellite,
#     parameters=Parameters,
#     output="/run/output/static_60.png"
# )

# # INCIDENCE -45
# Satellite.controller    = static_incidence
# Satellite.incidence     = radians(-60.0)
# test = run(    
#     earth=Earth,
#     sun=Sun,
#     satellite=Satellite,
#     parameters=Parameters,
#     output="/run/output/static_neg60.png"
# )

# # AREA DENSITY COMPARISON
# num_thetas      = 181
# thetas          = linspace(-90, 90, num_thetas)

# # 5
# generation      = zeros(num_thetas)
# for i in range(0,num_thetas):
#     Satellite.controller            = static_incidence
#     Satellite.incidence             = radians(thetas[i])
#     Satellite.area_density_comm     = 5
#     Satellite.area_density_solar    = 5

#     generation[i] = run(    
#         earth=Earth,
#         sun=Sun,
#         satellite=Satellite,
#         parameters=Parameters,
#     )
# plt.plot(thetas, generation)
# plt.title(f"static_incidence controller at area density 5, peak at {round(thetas[argmax(generation)],2)} deg")
# plt.xlim([-90,90])
# plt.gca().set_ylim(bottom=0.0)
# plt.ylabel("Power generation (W)")
# plt.xlabel("static_incidence controller alpha")
# plt.savefig("/run/output/area_density_5.png")
# plt.close()

# # 1
# generation      = zeros(num_thetas)
# for i in range(0,num_thetas):
#     Satellite.controller            = static_incidence
#     Satellite.incidence             = radians(thetas[i])
#     Parameters.plot                 = False
#     Satellite.area_density_comm     = 1
#     Satellite.area_density_solar    = 1

#     generation[i] = run(    
#         earth=Earth,
#         sun=Sun,
#         satellite=Satellite,
#         parameters=Parameters,
#     )
# plt.plot(thetas, generation)
# plt.title(f"static_incidence controller at area density 1, peak at {round(thetas[argmax(generation)],2)} deg")
# plt.xlim([-90,90])
# plt.gca().set_ylim(bottom=0.0)
# plt.ylabel("Power generation (W)")
# plt.xlabel("static_incidence controller alpha")
# plt.savefig("/run/output/area_density_1.png")
# plt.close()

# # 0.1
# generation      = zeros(num_thetas)
# for i in range(0,num_thetas):
#     Satellite.controller            = static_incidence
#     Satellite.incidence             = radians(thetas[i])
#     Parameters.plot                 = False
#     Satellite.area_density_comm     = 0.1
#     Satellite.area_density_solar    = 0.1
#     generation[i] = run(    
#         earth=Earth,
#         sun=Sun,
#         satellite=Satellite,
#         parameters=Parameters,
#     )
# plt.plot(thetas, generation)
# plt.title(f"static_incidence controller at area density 0.1, peak at {round(thetas[argmax(generation)],2)} deg")
# plt.xlim([-90,90])
# plt.gca().set_ylim(bottom=0.0)
# plt.ylabel("Power generation (W)")
# plt.xlabel("static_incidence controller alpha")
# plt.savefig("/run/output/area_density_0.1.png")
# plt.close()


# # SINUSOIDAL
# Satellite.controller    = sinusoidal_incidence
# test = run(    
#     earth=Earth,
#     sun=Sun,
#     satellite=Satellite,
#     parameters=Parameters,
#     output="/run/output/sinusoidal.png"
# )



# # SINUSOIDAL_OFF_90
# Satellite.controller    = sinusoidal_off_90
# test = run(    
#     earth=Earth,
#     sun=Sun,
#     satellite=Satellite,
#     parameters=Parameters,
#     output="/run/output/off90.png"
# )

# # NEG OFF 90
# Satellite.controller    = negative_sinusoidal_off_90
# test = run(    
#     earth=Earth,
#     sun=Sun,
#     satellite=Satellite,
#     parameters=Parameters,
#     output="/run/output/negoff90.png"
# )


# OPTIMAL CUTOFF FINDING
# num_thetas      = 91
# thetas          = linspace(0, 90, num_thetas)
# generation      = zeros(num_thetas)
# for i in range(0,num_thetas):
#     Satellite.controller            = clipped_sinusoidal_off_90
#     Satellite.clip                  = radians(thetas[i])
#     generation[i] = run(    
#         earth=Earth,
#         sun=Sun,
#         satellite=Satellite,
#         parameters=Parameters,
#     )
# plt.plot(thetas, generation)
# plt.title(f"Varying cutoff angles, max generation at {round(thetas[argmax(generation)],2)} deg")
# plt.xlim([0,90])
# plt.gca().set_ylim(bottom=0.0)
# plt.ylabel("Power generation (W)")
# plt.xlabel("clipped_sinusoidal_off_90 controller angle")
# plt.savefig("/run/output/optimal_cutoff.png")
# plt.close()

# # OPTIMAL CUTOFF
# Satellite.controller            = clipped_sinusoidal_off_90
# Satellite.clip                  = radians(8.0)
# test = run(    
#     earth=Earth,
#     sun=Sun,
#     satellite=Satellite,
#     parameters=Parameters,
#     output="/run/output/cutoff_authority.png"
# )

# SMART CUTOFF
Satellite.controller            = smart_controller
Satellite.clip                  = radians(8.0)
Parameters.days                 = 60
test = run(    
    earth=Earth,
    sun=Sun,
    satellite=Satellite,
    parameters=Parameters,
    output="/run/output/smart.png"
)