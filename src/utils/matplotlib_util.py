import numpy as np
import matplotlib.pyplot as plt
from utils.astropy_util import get_body_position
import matplotlib.animation as animation
from utils.constants import D_T, BodyEnum, R_EARTH, R_MOON
from datetime import datetime
from matplotlib.widgets import Slider


class Plot:
    """Handles all data output, processing, and visual representation in matplotlib."""

    def __init__(self, df):
        self.df = df

        self.ts = df["true_state.time"].to_numpy()

        self.xlocs = df["true_state.state.x"].to_numpy()
        self.ylocs = df["true_state.state.y"].to_numpy()
        self.zlocs = df["true_state.state.z"].to_numpy()
        self.vel_xs = df["true_state.state.vel_x"].to_numpy()
        self.vel_ys = df["true_state.state.vel_y"].to_numpy()
        self.vel_zs = df["true_state.state.vel_z"].to_numpy()

        self.locs = np.array([self.xlocs, self.ylocs, self.zlocs])
        self.ang_x = df["true_state.state.ang_vel_x"].to_numpy()
        self.ang_x_obs = df["observed_state.ang_vel_x"].to_numpy()

        self.fig_2d = plt.figure()
        self.ax_vel = plt.subplot(421)
        self.ax_pos = plt.subplot(422)
        self.ax_ang_vel_x = plt.subplot(425)

        self.ax_vel.set_xlim(xmin=self.ts[0], xmax=self.ts[-1])
        self.ax_pos.set_xlim(xmin=self.ts[0], xmax=self.ts[-1])
        self.ax_ang_vel_x.set_xlim(xmin=self.ts[0], xmax=self.ts[-1])

        axcolor = "lightgoldenrodyellow"
        axfreq = plt.axes([0.1, 0.1, 0.5, 0.01], facecolor=axcolor)
        self.t_max = Slider(
            axfreq,
            "t",
            self.ts[0],
            self.ts[-1],
            valinit=self.ts[-1],
            valstep=D_T,
        )
        self.t_max.on_changed(self.update)

        self.fig_3d = plt.figure("CislunarSim")
        self.ax = self.fig_3d.gca(projection="3d")

        self.u = np.linspace(0, 2 * np.pi, 60)
        self.v = np.linspace(0, np.pi, 60)

        self.ax.set_xlim(-10000000, 10000000)
        self.ax.set_ylim(-10000000, 10000000)
        self.ax.set_zlim(-10000000, 10000000)
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.set_zlabel("z")

        self.ax_vel.set_xlabel("t")
        self.ax_vel.set_ylabel("Velocity")

        self.ax_pos.set_xlabel("t")
        self.ax_pos.set_ylabel("Position")

        self.annot = self.ax.annotate(
            "",
            xy=(0, 0),
            xytext=(20, 20),
            textcoords="offset points",
            bbox=dict(boxstyle="round", fc="w"),
            arrowprops=dict(arrowstyle="->"),
        )
        self.annot.set_visible(False)
        self.lines_2d = []

    def plot_data(self) -> None:
        self.plot_data_2d()
        self.plot_data_3d()
        plt.tight_layout()

    def update(self, _):
        """Updates plotted data in response to slider value change"""

        t_selected_range = self.t_max.val - self.ts[0]
        t_max_index = int(t_selected_range // D_T)

        self.vel_xs_line.set_ydata(self.vel_xs[:t_max_index:])
        self.vel_ys_line.set_ydata(self.vel_ys[:t_max_index:])
        self.vel_zs_line.set_ydata(self.vel_zs[:t_max_index:])
        self.xlocs_line.set_ydata(self.xlocs[:t_max_index:])
        self.ylocs_line.set_ydata(self.ylocs[:t_max_index:])
        self.zlocs_line.set_ydata(self.zlocs[:t_max_index:])
        self.ang_x_line.set_ydata(self.ang_x[:t_max_index:])
        self.ang_x_obs_line.set_ydata(self.ang_x_obs[:t_max_index:])

        for line in self.lines_2d:
            line.set_xdata(self.ts[:t_max_index:])

        self.fig_2d.canvas.draw()
        self.fig_2d.canvas.flush_events()

    def plot_data_2d(self) -> None:
        """Displays 2d plots of spacecraft data"""

        (self.vel_xs_line,) = self.ax_vel.plot(
            self.ts, self.vel_xs, "--", c="hotpink", label="x"
        )
        (self.vel_ys_line,) = self.ax_vel.plot(
            self.ts, self.vel_ys, "--", c="green", label="y"
        )
        (self.vel_zs_line,) = self.ax_vel.plot(
            self.ts, self.vel_zs, "--", c="blue", label="z"
        )

        (self.xlocs_line,) = self.ax_pos.plot(
            self.ts, self.xlocs, "--", c="hotpink", label="x"
        )
        (self.ylocs_line,) = self.ax_pos.plot(
            self.ts, self.ylocs, "--", c="green", label="y"
        )
        (self.zlocs_line,) = self.ax_pos.plot(
            self.ts, self.zlocs, "--", c="blue", label="z"
        )

        (self.ang_x_line,) = self.ax_ang_vel_x.plot(
            self.ts, self.ang_x, "--", c="hotpink", label="x (true)"
        )
        (self.ang_x_obs_line,) = self.ax_ang_vel_x.plot(
            self.ts, self.ang_x_obs, "--", c="green", label="x (observed)"
        )
        self.lines_2d = [
            self.vel_xs_line,
            self.vel_ys_line,
            self.vel_zs_line,
            self.xlocs_line,
            self.ylocs_line,
            self.zlocs_line,
            self.ang_x_line,
            self.ang_x_obs_line,
        ]

        self.ax_vel.legend()
        self.ax_pos.legend()

        self.ax_ang_vel_x.legend()

    def plot_data_3d(self):
        """Plots a model of the earth, moon and the craft's trajectory in R3"""

        locs = np.array([self.xlocs, self.ylocs, self.zlocs])
        traj = plt.plot(self.xlocs, self.ylocs, self.zlocs, lw=2, c="blue")[0]

        traj_ani = animation.FuncAnimation(
            self.fig_3d,
            self.animate_traj,
            frames=len(self.xlocs),
            fargs=(locs, traj),
            interval=1,
            blit=False,
        )

        self.ax.set_box_aspect(aspect=(1, 1, 1))

        # Calculation and plotting of earth's position

        earth_x = R_EARTH * np.outer(np.cos(self.u), np.sin(self.v))
        earth_y = R_EARTH * np.outer(np.sin(self.u), np.sin(self.v))
        earth_z = R_EARTH * np.outer(np.ones(np.size(self.u)), np.cos(self.v))

        earth = [self.ax.plot_surface(earth_x, earth_y, earth_z, color="g")]

        # Calculation and plotting of moon's position
        moon_cx, moon_cy, moon_cz = get_body_position(self.ts[-1], BodyEnum.Moon)
        moon_x = moon_cx + R_MOON * np.outer(np.cos(self.u), np.sin(self.v))
        moon_y = moon_cy + R_MOON * np.outer(np.sin(self.u), np.sin(self.v))
        moon_z = moon_cz + R_MOON * np.outer(np.ones(np.size(self.u)), np.cos(self.v))

        moon = [self.ax.plot_surface(moon_x, moon_y, moon_z, color="gray")]

        moon_ani = animation.FuncAnimation(
            self.fig_3d, self.animate_moon, frames=len(self.xlocs), fargs=(locs, moon)
        )
        plt.show()

    def animate_traj(self, num, locs, line):
        """Handles trajectory line positioning and updating

        Args:
            num (int): counter that increments on each call to this function
            locs (npt.ArrayLike): the trajectory location data
            line (_type_): the trajectory that is being modified and plotted

        Returns:
            line: the updated trajectory
        """

        self.ax.set_title(
            "Cislunar Sim \nTime = "
            + datetime.utcfromtimestamp(self.ts[num]).strftime("%Y-%m-%d %H:%M:%S")
        )
        line.set_data(locs[0:2, :num])
        line.set_3d_properties(locs[2, :num])
        return line

    def animate_moon(self, num, locs, moon):
        """Handles moon positioning and updating

        Args:
            num (int): counter that increments on each call to this function
            locs (npt.ArrayLike): the moon trajectory location data
            moon (list): the moon object at the current location (should be a list of size 1, may change this in the future)
        """

        moon_cx = float(
            self.df["true_state.derived_state.r_mo"][num].strip("[]").split(" ")[1]
        )
        moon_cy = float(
            self.df["true_state.derived_state.r_mo"][num].strip("[]").split(" ")[2]
        )
        moon_cz = float(
            self.df["true_state.derived_state.r_mo"][num].strip("[]").split(" ")[3]
        )

        moon_x = moon_cx + R_MOON * np.outer(np.cos(self.u), np.sin(self.v))
        moon_y = moon_cy + R_MOON * np.outer(np.sin(self.u), np.sin(self.v))
        moon_z = moon_cz + R_MOON * np.outer(np.ones(np.size(self.u)), np.cos(self.v))

        moon[0].remove()
        moon[0] = self.ax.plot_surface(moon_x, moon_y, moon_z, color="gray")

    def plot_quat(self):
        """Plots true state quaternion versus time"""

        quat_v1s = self.df["true_state.state.quat_v1"]
        quat_v2s = self.df["true_state.state.quat_v2"]
        quat_v3s = self.df["true_state.state.quat_v3"]
        quat_rs = self.df["true_state.state.quat_r"]

        fig = plt.figure()
        plt.plot(self.ts, quat_v1s, alpha=0.8, label="v1")
        plt.plot(self.ts, quat_v2s, alpha=0.8, label="v2")
        plt.plot(self.ts, quat_v3s, alpha=0.8, label="v3")
        plt.plot(self.ts, quat_rs, "--", alpha=0.8, label="r")
        plt.xlabel("Time")
        plt.ylabel("")
        plt.title("Attitude Quaternion")
        plt.legend()
        plt.savefig(fname="attitude_plot.png")
