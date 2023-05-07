from abc import abstractmethod
from core.state.state import State
from utils.astropy_util import get_body_position
import numpy as np
from utils.constants import BodyEnum
from core.models.model_base import Model
from typing import Union, Tuple, List, Dict
import logging


class DerivedStateModel(Model):
    """Abstract Base class for all models this sim uses."""

    def __init__(self) -> None:
        pass

    @abstractmethod
    def evaluate(self, time: float, state: State) -> Dict[str, Union[float, int, bool]]:
        """Evaluates the model based on the current state.
        An instance of State is required to evaluate the model, (because each
            model should be dependent on the state of the system.)
        Args:
            state (State): a instance of a State class.

        Returns:
            _type_: Defined in concrete instantiation of subclasses.
        """
        ...


def quat_to_rotvec(q: Tuple[float, float, float, float]) -> np.ndarray:
    """Converts a 4-tuple representation of a quaternion into a 3-tuple Euler angle rotation vector.

    Uses the vector/scalar convention used in Markley and Crassidis (vector is the first 3 elements,
    scalar is the 4th element)"""
    norm = np.linalg.norm(q[:3])
    if not norm:
        return np.array([0, 0, 0])

    rotvec = np.array(q[:3]) / norm
    return rotvec


def cartesian_to_spherical(x: float, y: float, z: float) -> Tuple[float, float, float]:
    """Converts a cartesian vector into a spherical coordinates"""

    r = np.sqrt(x * x + y * y + z * z)
    phi = np.arctan2(y, x)  # azimuth angle
    if r == 0:
        theta = 0
    else:
        theta = np.arccos(z / r)  # elevation angle

    return (r, phi, theta)


class DerivedAttitude(DerivedStateModel):
    def evaluate(self, _: float, state: State):
        spin_vector = quat_to_rotvec((state.quat_v1, state.quat_v2, state.quat_v3, state.quat_r))
        spherical_coordinates = cartesian_to_spherical(*spin_vector)

        return {
            "attitude_vector": np.array(spin_vector),
            "azimuth": spherical_coordinates[1],
            "elevation": spherical_coordinates[2],
        }


class DerivedPosition(DerivedStateModel):
    """Updates position column vectors for use in the position dynamics model."""

    def evaluate(self, t: float, state: State) -> Dict[str, np.ndarray]:

        # Position column vectors from moon/sun/earth/craft to the origin, where the origin is
        # the Earth's center of mass.
        # Craft to origin
        r_co = np.array([state.x, state.y, state.z])
        # Moon to origin
        r_mo = np.array(get_body_position(10 * t // 10, BodyEnum.Moon))
        # Sun to origin
        r_so = np.array(get_body_position(10 * t // 10, BodyEnum.Sun))
        # Earth to origin (Note: Earth is at the origin in GCRS)
        r_eo = np.array((0.0, 0.0, 0.0))

        # Position column vectors from body to the craft.
        # Moon to the craft
        r_mc = np.subtract(r_mo, r_co)
        # Sun to the craft
        r_sc = np.subtract(r_so, r_co)
        # Earth to the craft
        r_ec = np.subtract(r_eo, r_co)

        return {
            "r_co": r_co,
            "r_mo": r_mo,
            "r_so": r_so,
            "r_eo": r_eo,
            "r_mc": r_mc,
            "r_sc": r_sc,
            "r_ec": r_ec,
        }


class InertiaModel(DerivedStateModel):
    def evaluate(self, _: float, state: State) -> Dict[str, Union[float, int, bool]]:
        """ the _b postfix means the value is in the spacecraft's body frame"""
        fill_frac = state.fill_frac

        dcm = np.array([[0, 1, 0], [0, 0, -1], [-1, 0, 0]], dtype=np.int32)
        dcmT = np.transpose(dcm)
        # not sure why we do the above. Did i do that?
        # probably to get the (incorrect) solidworks frame into the spacecraft
        # body frame

        # Inertia tensor when full. Structure is:
        # [[Ixx, Ixy, Ixz],
        #  [Iyx, Iyy, Iyz],
        #  [Izx, Izy, Izz]].
        # Units are (kg * m^2).
        idf = (
            np.array(
                [
                    [933513642.20, 260948256.18, 430810000.30],
                    [260948256.18, 1070855457.07, 387172545.62],
                    [430810000.30, 387172545.62, 629606813.62],
                ],
                dtype=np.float64,
            )
            * 1e-9
        )
        # inertia tensor in correct body frame
        idf_b = np.matmul(np.matmul(dcm, idf), dcmT)

        # Inertia tensor at 125 mL. Structure is:
        # [[Ixx, Ixy, Ixz],
        #  [Iyx, Iyy, Iyz],
        #  [Izx, Izy, Izz]].
        # Units are (kg * m^2).
        idi = (
            np.array(
                [
                    [855858994.14, 229481961.55, 377087149.13],
                    [229481961.55, 963124288.81, 353943859.15],
                    [377087149.13, 353943859.15, 559805590.96],
                ],
                dtype=np.float64,
            )
            * 1e-9
        )
        # inertia tensor in correct body frame
        idi_b = np.matmul(np.matmul(dcm, idi), dcmT)

        # Determine inertia tensor for Oxygen via linear interpolation as a function of fill
        # fraction.

        # TODO: determine whether linear fit is accurate enough
        ineria_matrix_b = (idf_b - idi_b) * fill_frac + idi_b

        # now that we know our moment of inertia (I matrix), we can calculate our angular
        # velocities:
        # page 14 of the 4060 Attitude Dynamics handout:
        # h = I dot omega
        # --> omega = inverse(I) matmul h

        angular_momentum = np.array([[state.h_x, state.h_y, state.h_z]])
        
        angular_velocity = np.matmul(np.linalg.inv(ineria_matrix_b), angular_momentum.T)
        logging.info(f"Inv: {np.linalg.inv(ineria_matrix_b)}")
        logging.info(f"h: {angular_momentum}")
        logging.info(f"w: {angular_velocity}")
        return {
            "Ixx": ineria_matrix_b[0][0],
            "Ixy": ineria_matrix_b[0][1],
            "Ixz": ineria_matrix_b[0][2],
            "Iyx": ineria_matrix_b[1][0],
            "Iyy": ineria_matrix_b[1][1],
            "Iyz": ineria_matrix_b[1][2],
            "Izx": ineria_matrix_b[2][0],
            "Izy": ineria_matrix_b[2][1],
            "Izz": ineria_matrix_b[2][2],
            "ang_vel_x": angular_velocity[0][0],
            "ang_vel_y": angular_velocity[1][0],
            "ang_vel_z": angular_velocity[2][0],
        }
    

DERIVED_MODEL_LIST: List[DerivedStateModel] = [DerivedPosition(), DerivedAttitude(), InertiaModel()]
