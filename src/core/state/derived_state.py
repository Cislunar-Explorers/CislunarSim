from dataclasses import dataclass
import numpy as np
from typing import Dict


@dataclass
class DerivedState:
    """Container class for derived state variables needed for state determination.
    TODO: Concretely document these somewhere.
    """

    # inertia matrix components (kg * m^2). Structure is
    # [[Ixx, Ixy, Ixz],
    #  [Iyx, Iyy, Iyz],
    #  [Izx, Izy, Izz]].
    Ixx: float = 0.0
    Ixy: float = 0.0
    Ixz: float = 0.0
    Iyx: float = 0.0
    Iyy: float = 0.0
    Iyz: float = 0.0
    Izx: float = 0.0
    Izy: float = 0.0
    Izz: float = 0.0

    # angular velocity (rad/s)
    ang_vel_x: float = 0.0
    ang_vel_y: float = 0.0
    ang_vel_z: float = 0.0

    # Kane damping constant
    kane_c: float = 0.0

    # Position column vectors from moon/sun/earth/craft to the origin, where the origin is # the Earth's center of mass.
    # craft to origin
    r_co: np.ndarray = np.array((0.0, 0.0, 0.0))
    # moon to origin
    r_mo: np.ndarray = np.array((0.0, 0.0, 0.0))
    # sun to origin
    r_so: np.ndarray = np.array((0.0, 0.0, 0.0))
    # earth to origin
    r_eo: np.ndarray = np.array((0.0, 0.0, 0.0))

    # Position column vectors from body to the craft.
    # moon to the craft
    r_mc: np.ndarray = np.array((0.0, 0.0, 0.0))
    # sun to the craft
    r_sc: np.ndarray = np.array((0.0, 0.0, 0.0))
    # earth to the craft
    r_ec: np.ndarray = np.array((0.0, 0.0, 0.0))

    # attitude (unit) vector of spacecraft in ECI
    attitude_vector: np.ndarray = np.array((0.0, 0.0, 0.0))

    # Azimuth angle of the spacecraft frame in ECI. "Theta" angle in spherical coords
    azimuth: float = 0  # radians

    # Elevation angle of the spacecraft frame in ECI. "phi" angle in spherical coords
    elevation: float = 0  # radians

    def update(self, derived_state_dict: Dict) -> None:
        """
        update() is a procedure that updates the fields of the derived state with specified
            key/value pairs in derived_state_dict.
        If a key in the `derived_state_dict` is not defined as an attribute in DerivedState.
            __init__, it will be ignored.
        """
        for key, value in derived_state_dict.items():
            if key in self.__dict__.keys():
                setattr(self, key, value)
