# opnav camera field of view calculations
import numpy as np
from dataclasses import dataclass
from typing import List, Tuple

DEG_2_RAD = np.pi / 180


@dataclass
class CameraFov:
    orientation: np.ndarray  # 3x3 direction cosine matrix
    vertical: float = 40 * DEG_2_RAD  # y-axis, radians
    horizontal: float = 60 * DEG_2_RAD  # x-axis, radians


def vec_in_fov(cam: CameraFov, vector_array: np.ndarray):
    # convert vectors to the camera frame
    vector_array_in_camera_frame = np.matmul(cam.orientation, vector_array.T).T
    # convert vectors into elevation/azimuth angles relative to -Z in the camera frame
    xs = vector_array_in_camera_frame[:, 0]
    ys = vector_array_in_camera_frame[:, 1]
    zs = vector_array_in_camera_frame[:, 2]

    # compute angles x/y angles as observed by the camera boresight
    # Use the -Z vector as the boresight to get a sane camera frame
    x_angle_cam = np.arctan2(xs, -zs)
    y_angle_cam = np.arctan2(ys, -zs)

    # filter which vectors are good
    x_good = np.abs(x_angle_cam) <= cam.horizontal/2
    y_good = np.abs(y_angle_cam) <= cam.vertical/2
    boolean_map = np.logical_and(x_good, y_good)
    
    return np.matmul(cam.orientation.T, vector_array_in_camera_frame[boolean_map].T).T


def fibonacci_sphere(samples=1000) -> List[Tuple[float, float, float]]:
    """Fibonacci Sphere

    Generates points that are somewhat equally spaced on a unit sphere.
    Stolen from https://stackoverflow.com/questions/9600801/evenly-distributing-n-points-on-a-sphere

    Args:
        samples (int, optional): number of points to put on the sphere. Defaults to 1000.

    Returns:
        List[Tuple[float, float, float]]: List of 3D coordinates of points on the sphere
    """
    points = []
    phi = np.pi * (3.0 - np.sqrt(5.0))  # golden angle in radians

    for i in range(samples):
        y = 1 - (i / float(samples - 1)) * 2  # y goes from 1 to -1
        radius = np.sqrt(1 - y * y)  # radius at y

        theta = phi * i  # golden angle increment

        x = np.cos(theta) * radius
        z = np.sin(theta) * radius

        points.append((x, y, z))

    return points


if __name__ == "__main__":
    DCM = np.eye(3)
    sphere_points = fibonacci_sphere()
    sphere_array = np.array(sphere_points)
    viewable_angles = vec_in_fov(CameraFov(DCM), sphere_array)

