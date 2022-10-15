from enum import Enum, IntEnum
from typing import Union
from pathlib import Path


SIM_ROOT = (Path(__file__).parent / "../..").resolve()
SRC_ROOT = (Path(__file__).parent / "..").resolve()


class StringEnum(str, Enum):
    """Similar to the built-in IntEnum, but with strings!
    See https://docs.python.org/3/library/enum.html#others for inspiration."""

    pass


class ModelEnum(StringEnum):
    AttitudeModel = "att"
    PositionModel = "pos"

    GyroModel = "gyro"

    UnittestModel = "unittest"


DEFAULT_MODELS = [ModelEnum.AttitudeModel, ModelEnum.PositionModel]

# The union of the different types of fields within State.
State_Type = Union[int, float, bool]


class BodyEnum(IntEnum):
    def __str__(self):
        return str(self.name)

    Earth = 0
    Moon = 1
    Sun = 2


# mu values of the body, where mu = G * m_body
G = 6.6743e-11
mu_moon = G * 7.34767309e22
mu_sun = G * 1.988409870698051e30
mu_earth = G * 5.972167867791379e24

EARTH_SMA = 149.60e9  # semi-major axis of Earth's orbit around the Sun

EARTH_SOI = EARTH_SMA * (mu_earth / mu_sun) ** (2 / 5)
R_EARTH = 6_378_137  # Average Radius of the Earth, meters
R_MOON = 1_737_100  # Average Radius of the Moon, meters
R_SUN = 696_340_000

D_T = 200  # timestep in seconds
