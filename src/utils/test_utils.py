import math
from core.state import State

s_0 = {
    "ang_vel_x": 0.0,
    "ang_vel_y": 0.0,
    "ang_vel_z": 0.0,
    "gnc_pos_q1": 0.0,
    "gnc_pos_q2": 0.0,
    "gnc_pos_q3": 0.0,
    "gnc_pos_q4": 0.0,
    "vel_x": 0.0,
    "vel_y": 0.0,
    "vel_z": 0.0,
    "x": 0.0,
    "y": 0.0,
    "z": 0.0,
    "force_propulsion_thrusters": 0.0,
    "fuel_mass": 0.0,
    "force_earth": 0.0,
    "force_moon": 0.0,
    "propulsion_on": False,
    "solenoid_actuation_on": False,
}
s_1 = {
    "ang_vel_x": 2.0,
    "ang_vel_y": 3.0,
    "ang_vel_z": 4.0,
    "gnc_pos_q1": 5.0,
    "gnc_pos_q2": 6.0,
    "gnc_pos_q3": 7.0,
    "gnc_pos_q4": 8.0,
    "vel_x": 9.0,
    "vel_y": 10.0,
    "vel_z": 11.0,
    "x": 12.0,
    "y": 13.0,
    "z": 14.0,
    "force_propulsion_thrusters": 15.0,
    "fuel_mass": 16.0,
    "force_earth": 17.0,
    "force_moon": 18.0,
    "propulsion_on": True,
    "solenoid_actuation_on": False,
}
state_1 = State(s_1)

d3456 = {
    "gyro_bias": [0.497625, -0.10821875, 0.77490625],
    "gyro_noise": [0.1824535, 0.11738579, 0.19192256],
    "gyro_sensitivity": 0.015625 * (math.pi / 180),
    "dry_mass": 3,
    "com": 4,
    "tank_volume": 5,
    "thruster_force": 6,
}
