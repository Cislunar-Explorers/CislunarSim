import numpy as np
from typing import Tuple


def cross_product_matrix(vector: np.ndarray) -> np.ndarray:  # type: ignore
    """Creates a cross-multiplication matrix for a length 3 vector
    See bottom of page 2 of https://cornell.app.box.com/file/809903125394
    for brief reference.


    Args:
        vector (np.array): a 3x1 vector

    Returns:
        np.ndarray: a 3x3 matrix which when matrix multiplied with another vector, b, has the same results as the input
        vector cross-product with b
    """
    vector.shape = (3,)
    return np.array(
        [[0, -vector[2], vector[1]], [vector[2], 0, -vector[0]], [-vector[1], vector[0], 0]]  # type: ignore
    )


def calc_xi(v: np.ndarray, r: float) -> np.ndarray:
    """Xi function as defined on page 7 of https://cornell.app.box.com/file/809903125394

    Args:
        v (np.ndarray): 3-by-1 numpy array (column vector) representing the vector component of a quaternion.
        r (float): scalar component of the quaternion

    Returns:
        Numpy matrix: 4-by-3 Xi matrix
    """
    top = r * np.eye(3) + cross_product_matrix(v)  # 3-by-3 matrix
    bot = -v.T  # 1-by-3 matrix
    return np.vstack((top, bot))  # stacked to be a 4-by-3


def calc_psi(v: np.ndarray, r: float) -> np.ndarray:
    """Psi function as defined on page 7 of https://cornell.app.box.com/file/809903125394

    Args:
        v (np.ndarray):  3-by-1 numpy array (column vector) representing the vector component of a quaternion.
        r (float): scalar component of the quaternion

    Returns:
        np.ndarray: 4-by-3 Psi matrix
    """
    top = r * np.eye(3) - cross_product_matrix(v)  # 3-by-3 matrix
    bot = -v.T  # 1-by-3 matrix
    return np.vstack((top, bot))  # stacked to be a 4-by-3


def quat_to_dcm(quat: np.ndarray) -> np.ndarray:
    """Calculates the direction cosine matrix (DCM) associated with the input quaternion.
    The math in this function is based off of page 17 of https://cornell.app.box.com/file/809903002605
    Args:
        quat (np.ndarray): 4x1 quaternion

    Returns:
        np.ndarray: 3x3 Direction Cosine Matrix
    """

    v = quat[0:3]
    r = quat[3]

    xi = calc_xi(v, r)
    psi = calc_psi(v, r)

    dcm = np.matmul(xi.T, psi)

    return dcm


def dcm_to_spherical_coords(
    dcm: np.ndarray, spacecraft_frame_vector: np.ndarray = np.array((1, 0, 0))
) -> Tuple[float, float]:
    """Calculates the spherical coordinate components (theta, phi) of the `spacecraft_frame_vector` from the input
    spacecraft-body DCM.

    Args:
        dcm (np.ndarray): the DCM of an ECI to spacecraft body frame transformation
        spacecraft_frame_vector (np.ndarray, optional): vector in the spacecraft body
        frame that is converted into ECI and then transformed into spherical coordinates.
        Defaults to np.array((1, 0, 0)), the X-axis of the spacecraft .

    Returns:
        Tuple[float, float]: (theta, phi) angles corresponding to the spherical coordinates
    """
    vector_in_ECI_frame = np.matmul(dcm.T, spacecraft_frame_vector)
    normed_vec = vector_in_ECI_frame / np.linalg.norm(vector_in_ECI_frame)

    phi = np.arccos(normed_vec[2])
    theta = np.arctan2(normed_vec[1], normed_vec[0])
    return phi, theta


def quaternion_derivative(current_quat: np.ndarray, angular_velocity: np.ndarray) -> np.ndarray:
    """Calculates the time derivative of a given quaternion based on angular velocity.
    The algo implemented here is based off the math on page 17 of
    https://cornell.app.box.com/file/809903002605

    Args:
        current_quat (np.ndarray): length-4 array describing the quaternion of the spacecraft's angular position in ECI.
        (first 3 elements describe the vector, last one describes the scalar component)

        angular_velocity (np.ndarray): length-3 array of the angular velocities in rad/s (in the body frame, i think)

    Returns:
        np.ndarray: the time derivative of each element of the quaternion
    """

    current_quat.shape = (4, 1)  # enforces a column vector
    angular_velocity.shape = (3, 1)

    v = current_quat[0:3]
    r = current_quat[3]

    xi = calc_xi(v, r)

    quat_derivative = 0.5 * np.matmul(xi, angular_velocity)  # 4x3 times a 3x1 = 4x1

    return quat_derivative
