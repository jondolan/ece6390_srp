from math import degrees
from numpy import array, linspace, zeros, average, trapz, sqrt, interp
import matplotlib.pyplot as plt

from scipy.signal import resample

from .propagation       import propagate
from .latlong           import r_to_latlong

from solar_power_sim    import solar_power_efficiency
from comm_sim           import transmission_efficiency

def run(earth, sun, satellite, parameters):
    # print(controller(0, 0, 0, 0, math.radians(90.0)))
    
    ts                          = linspace(0, parameters.days*satellite.period, parameters.samples)
    parameters.dt               = ts[1]-ts[0]

    r0                          = array([1, 0, 0]) * satellite.initial_r                    # km
    v0                          = array([0, 1, 0]) * sqrt(earth.mu / satellite.initial_r)   # km/s

    # fix units
    sun.p_km                        = sun.p / 1000.0                        # convert from (kg*m/s^2)/m^2 to (kg*km/s^2)/m^2
    satellite.area_to_mass_solar    = 1.0/satellite.area_density_solar      # equation requires area to mass ratio
    satellite.area_to_mass_comm     = 1.0/satellite.area_density_comm

    # initial condition
    satellite.incidence             = satellite.controller(r0, v0, ts[0], parameters, satellite)

    rs, _, thetas  = propagate(r0, v0, ts, parameters, earth, sun, satellite)

    longs               = zeros(len(ts))
    generation_factor   = zeros(parameters.samples)
    transmission_factor = zeros(parameters.samples)
    power               = zeros(parameters.samples)

    # resample thetas
    thetas_t    = [x[0] for x in thetas]
    thetas_vals = [x[1] for x in thetas]
    thetas      = interp(ts, thetas_t, thetas_vals)
    # thetas      = resample(thetas_vals, len(ts), thetas_t)[0]

    for i in range(0, parameters.samples):
        _, longs[i]             = r_to_latlong(ts[i], rs[i], earth)
        distance                = sqrt( rs[i][0]**2 + rs[i][1]**2 + rs[i][2]**2 )
        transmission_factor[i]  = transmission_efficiency(longs[i], distance, earth, satellite)
        generation_factor[i]    = solar_power_efficiency(thetas[i])
        power[i]                = transmission_factor[i]*generation_factor[i]*satellite.peak_power    # W

    energy          = (trapz(power, ts, parameters.dt) / ts[-1]) / 1000 # kWh
    total_power     = energy * (parameters.days*24) # kW
    prefect_total   = (satellite.peak_power / 1000) * (parameters.days*24) #kW

    if parameters.plot:
        # plot results!
        days    = ts/earth.sidereal_day

        fig = plt.figure()
        fig.suptitle(f"{parameters.days} days, total={round(total_power,3)}kW, {round(energy,3)}kWh, {round((total_power/prefect_total)*100,1)}% of max", y=0.95)
        fig.set_size_inches(10, 10)
        plt.subplots_adjust(wspace=0.4, hspace=0.6)

        ax = fig.add_subplot(321)
        ax.set_title("Perifocal orbital diagram")
        ax.set_ylabel("y position (km)")
        ax.set_xlabel("x position (km)")
        ax.set_aspect('equal', adjustable='box')
        ax.plot(rs[:,0], rs[:,1])
        ax.plot(0,0,'b+')
        ax.plot(rs[:,0][0], rs[:,1][0],'g+')
        ax.plot(rs[:,0][-1], rs[:,1][-1],'r+')

        ax = fig.add_subplot(322)
        ax.set_title("Controller")
        ax.set_ylabel("Solar incidence angle (deg)")
        ax.set_xlabel("Elapsed time (days)")
        ax.plot(days, [degrees(x) for x in thetas])

        ax = fig.add_subplot(323)
        ax.set_title("SSP longitude")
        ax.set_ylabel("Longitude (deg)")
        ax.set_xlabel("Elapsed time (days)")
        ax.axhline(degrees(satellite.max_long_drift), color='red')
        ax.axhline(degrees(-satellite.max_long_drift), color='red')
        ax.plot(days, longs)

        ax = fig.add_subplot(324)
        ax.set_title("Ground station power receipt (no FSPL)")
        ax.set_ylabel("Power (W)")
        ax.set_xlabel("Elapsed time (days)")
        # ax.set_ylim([-0.05,1.05])
        ax.plot(days, power)

        ax = fig.add_subplot(325)
        ax.set_title("Satellite solar power generation")
        ax.set_ylabel("Efficiency (%)")
        ax.set_xlabel("Elapsed time (days)")
        ax.set_ylim([-0.05,1.05])
        ax.plot(days, generation_factor)

        ax = fig.add_subplot(326)
        ax.set_title("Satellite comm transmission")
        ax.set_ylabel("Efficiency (%)")
        ax.set_xlabel("Elapsed time (days)")
        ax.set_ylim([-0.05,1.05])
        ax.plot(days, transmission_factor)

        fig.savefig(f"/run/output/output.png")
        plt.close()

        # plt.plot(ts/earth.sidereal_day, longs)
        # plt.savefig("/run/long.png")
        # plt.close()

        # plt.plot(rs[:,0], rs[:,1])
        # plt.savefig("/run/xy.png")
        # plt.close()

        # plt.plot(ts/earth.sidereal_day, thetas)
        # plt.savefig("/run/thetas.png")
        # plt.close()

        # plt.plot(ts/earth.sidereal_day, transmission)
        # plt.savefig("/run/transmission.png")
        # plt.close()

        # plt.plot(ts/earth.sidereal_day, power)
        # plt.savefig("/run/power.png")
        # plt.close()

    # TODO: power generation, transmission efficency
    return total_power
