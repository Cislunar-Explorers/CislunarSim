import unittest
from core import config
from main import SimRunner
import numpy as np
import logging
from utils.log import log
from utils.data_handling import states_to_df


def magnitude(x, y, z):
    return np.sqrt(x**2 + y**2 + z**2)


def magnitude4(x, y, z, zz):
    return np.sqrt(x**2 + y**2 + z**2 + zz**2)


class AttDynamicsModelTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # setup sim and run for a little bit
        log.setLevel(logging.CRITICAL)
        _config = config.Config.make_config("configs/attitude_dynamics_test.json")
        sim_runner = SimRunner(_config)
        states = sim_runner._run()  # want to avoid shared memory not working
        cls.df = states_to_df(states)

        # extract data and verify it's physically sound
        # stuff to look for:
        # - the vector norm of the attitude quaternion must always be 1
        # - the vector norm of the angular momentum vector must not change (unless
        #   there is energy added to the system, i.e. by an ACS thruster firing)
        # 
        # The above checks don't really test if the model works, they just ensure that the model doesn't break physics

    def test_constant_angular_moment_norm(self):
        # apply the magnitude function to each row of the dataframe to create a new column
        # add column which calculates vector norm of angular momentum at every timestep
        self.df["angular_momentum_magnitude"] = self.df.apply(
            lambda row: magnitude(
                row["true_state.state.h_x"], row["true_state.state.h_y"], row["true_state.state.h_z"]
            ),
            axis=1,
        )

        magnitudes = self.df["angular_momentum_magnitude"].to_numpy()
        # get first element
        norm = magnitudes[0]
        # make a list with n elements
        expected = np.array([norm] * len(self.df))
        np.testing.assert_allclose(magnitudes, expected, rtol=3e-7)

    def test_unity_quaternion_norm(self):
        # add column which calculates vector norm of quaternion at every timestep
        self.df["quaternion_norm"] = self.df.apply(
            lambda row: magnitude4(
                row["true_state.state.quat_v1"],
                row["true_state.state.quat_v2"],
                row["true_state.state.quat_v3"],
                row["true_state.state.quat_r"],
            ),
            axis=1,
        )

        norms = self.df["quaternion_norm"].to_numpy()
        # make a list with n elements of 1.0 (expected)
        expected = np.array([1.0] * len(self.df))
        np.testing.assert_allclose(norms, expected, rtol=2e-7)
