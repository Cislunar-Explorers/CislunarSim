import math
from typing import Dict
from core.state.state import State
from core.parameters import Parameters

s_0 = {
    "fill_frac": 0.0,
    "ang_vel_x": 0.0,
    "ang_vel_y": 0.0,
    "ang_vel_z": 0.0,
    "quat_v1": 0.0,
    "quat_v2": 0.0,
    "quat_v3": 0.0,
    "quat_r": 0.0,
    "vel_x": 0.0,
    "vel_y": 0.0,
    "vel_z": 0.0,
    "x": 0.0,
    "y": 0.0,
    "z": 0.0,
    "cgt_pressure": 0.0,
    "force_propulsion_thrusters": 0.0,
    "fuel_mass": 0.0,
    "force_earth": 0.0,
    "force_moon": 0.0,
    "propulsion_on": False,
    "solenoid_actuation_on": False,
}

s_1 = {
    "fill_frac": 1.0,
    "ang_vel_x": 2.0,
    "ang_vel_y": 3.0,
    "ang_vel_z": 4.0,
    "quat_v1": 5.0,
    "quat_v2": 6.0,
    "quat_v3": 7.0,
    "quat_r": 8.0,
    "vel_x": 9.0,
    "vel_y": 10.0,
    "vel_z": 11.0,
    "x": 12.0,
    "y": 13.0,
    "z": 14.0,
    "cgt_pressure": 15.0,
    "force_propulsion_thrusters": 16.0,
    "fuel_mass": 17.0,
    "force_earth": 18.0,
    "force_moon": 19.0,
    "propulsion_on": True,
    "solenoid_actuation_on": False,
}

state_1 = State(**s_1)


d3456_dict: Dict = {
        "gyro_bias": [0.497625, -0.10821875, 0.77490625],
        "gyro_noise": [0.1824535, 0.11738579, 0.19192256],
        "gyro_sensitivity": 0.015625 * (math.pi / 180),
        "dry_mass": 3,
        "com": 4,
        "tank_volume": 5,
        "thruster_force": 6,
        "max_iter": 1000000
}


d3456: Parameters = Parameters(d3456_dict)

