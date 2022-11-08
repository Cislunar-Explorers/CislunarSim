# opnav camera field of view calculations

from dataclasses import dataclass


@dataclass
class CameraFov:
    vertical: float  # y-axis, degrees
    horizontal: float  # x-axis, degrees
