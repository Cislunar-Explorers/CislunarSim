import numpy as np
import matplotlib.pyplot as plt
from utils.astropy_util import get_body_position
from utils.constants import BodyEnum, R_EARTH, R_MOON, R_SUN


class Plot:
    def __init__(self, xlocs, ylocs, zlocs, state):
        fig = plt.figure()
        self.ax = fig.add_subplot(projection="3d")
        self.ax.set_xlim(-10000000, 10000000)
        self.ax.set_ylim(-10000000, 10000000)
        self.ax.set_zlim(-10000000, 10000000)
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.set_zlabel("z")
        # self.ax = plt.axes(projection='3d')
        self.xlocs = xlocs
        self.ylocs = ylocs
        self.zlocs = zlocs
        self.state = state

    def plot_data(self) -> None:
        """Procedure that plots a model of the earth, moon and the craft's trajectory in R3"""
        # 3D scatter plot of craft's trajectory
        self.ax.scatter3D(self.xlocs, self.ylocs, self.zlocs, cmap="Greens")

        # Calculation and plotting of earth's position
        u, v = np.mgrid[0 : 2 * np.pi : 20j, 0 : np.pi : 10j]
        earth_x = R_EARTH * np.cos(u) * np.sin(v)
        earth_y = R_EARTH * np.sin(u) * np.sin(v)
        earth_z = R_EARTH * np.cos(v)
        self.ax.plot_surface(earth_x, earth_y, earth_z, color="g")

        # Calculation and plotting of moon's position
        moon_cx, moon_cy, moon_cz = get_body_position(self.state.time, BodyEnum.Moon)
        moon_x = moon_cx + R_MOON * np.cos(u) * np.sin(v)
        moon_y = moon_cy + R_MOON * np.sin(u) * np.sin(v)
        moon_z = moon_cz + R_MOON * np.cos(v)
        self.ax.plot_surface(moon_x, moon_y, moon_z, color="gray")

        # Calculation and plotting of sun's position
        sun_cx, sun_cy, sun_cz = get_body_position(self.state.time, BodyEnum.Sun)
        sun_x = sun_cx + R_SUN * np.cos(u) * np.sin(v)
        sun_y = sun_cy + R_SUN * np.sin(u) * np.sin(v)
        sun_z = sun_cz + R_SUN * np.cos(v)
        self.ax.plot_surface(sun_x, sun_y, sun_z, color="y")

        plt.show()
