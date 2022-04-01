from astropy.time import Time
from astropy.coordinates import get_sun, get_moon, CartesianRepresentation
from typing import Tuple, Optional


def get_ephemeris(
    observeStart: float, body: BodyEnum
) -> Tuple[float, float, float, float, float, float]:
    pass
