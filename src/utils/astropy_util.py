from astropy.time import Time
from astropy.coordinates import get_sun, get_moon, CartesianRepresentation
from astropy.constants import G, M_sun, M_earth
from typing import Tuple, Optional
from utils.constants import BodyEnum


# Heavily reference the get_ephemeris function here: https://github.com/Cislunar-Explorers/FlightSoftware/blob/master/OpticalNavigation/core/observe_functions.py
def get_ephemeris(observeStart: float, body: BodyEnum) -> Tuple[float, float, float]:
    # Astropy needs unix timestamp in seconds!!!
    current_time = observeStart
    observeStart = observeStart - 11.716
    init_au = None
    current_au = None
    if body == BodyEnum.Sun:
        init_au = get_sun(Time(observeStart, format="unix")).cartesian
        current_au = get_sun(Time(current_time, format="unix")).cartesian
    elif body == BodyEnum.Moon:
        init_au = get_moon(Time(observeStart, format="unix")).cartesian
        current_au = get_moon(Time(current_time, format="unix")).cartesian

    init = CartesianRepresentation([init_au.x, init_au.y, init_au.z], unit="m")
    current = CartesianRepresentation(
        [current_au.x, current_au.y, current_au.z], unit="m"
    )
    x = current.x.value
    y = current.y.value
    z = current.z.value
    return x, y, z
