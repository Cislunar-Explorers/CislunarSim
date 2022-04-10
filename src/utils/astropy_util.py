from astropy.time import Time
from astropy.coordinates import get_sun, get_moon, CartesianRepresentation
from typing import Tuple
from utils.constants import BodyEnum
from astropy.coordinates import SkyCoord


# Heavily reference the get_ephemeris function here: https://github.com/Cislunar-Explorers/FlightSoftware/blob/master/OpticalNavigation/core/observe_functions.py
def get_body_position(time: float, body: BodyEnum) -> Tuple[float, float, float]:
    """

    Gets position vector of [body] based on [time]

    Args:
        time (float): the current time being queried
        body (BodyEnum): body (earth, moon, sun)

    Returns:
        Tuple[float, float, float]: position vector of the specified body
    """
    current_time = time
    current_au = SkyCoord(
        0, 0, 0, unit="m", frame="gcrs", representation_type="cartesian"
    )
    if body == BodyEnum.Sun:
        current_au = get_sun(Time(current_time, format="unix")).cartesian
    elif body == BodyEnum.Moon:
        current_au = get_moon(Time(current_time, format="unix")).cartesian
    current = CartesianRepresentation(
        [current_au.x, current_au.y, current_au.z], unit="m"
    )
    x = current.x.value
    y = current.y.value
    z = current.z.value
    return x, y, z
