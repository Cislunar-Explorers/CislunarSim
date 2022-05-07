import numpy as np
import matplotlib.pyplot as plt
from utils.astropy_util import get_body_position
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
from utils.constants import BodyEnum, R_EARTH, R_MOON
from datetime import datetime


class Plot:

   

    def __init__(self, df):
        self.fig_2d = plt.figure()
        self.ax_vel = plt.subplot(221)
        self.ax_pos = plt.subplot(222)

        self.fig_3d = plt.figure("CislunarSim")
        self.ax = self.fig_3d.gca(projection='3d')

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

        self.xlocs = df["true_state.state.x"].to_numpy()
        self.ylocs = df["true_state.state.y"].to_numpy()
        self.zlocs = df["true_state.state.z"].to_numpy()
        self.ts = df["true_state.time"].to_numpy()
        self.vel_xs = df["true_state.state.vel_x"].to_numpy()
        self.vel_ys = df["true_state.state.vel_y"].to_numpy()
        self.vel_zs = df["true_state.state.vel_z"].to_numpy()

        self.times = df["true_state.time"].to_numpy()

        self.locs = np.array([self.xlocs, self.ylocs, self.zlocs])

        self.annot = self.ax.annotate(
            "",
            xy=(0, 0),
            xytext=(20, 20),
            textcoords="offset points",
            bbox=dict(boxstyle="round", fc="w"),
            arrowprops=dict(arrowstyle="->"),
        )
        self.annot.set_visible(False)

    def plot_data(self) -> None:
        self.plot_data_2d()
        self.plot_data_3d()
        plt.tight_layout()
        #plt.show()

    def plot_data_2d(self) -> None:
        """Procedure that displays 2d plots of spacecraft data"""
        self.ax_vel.plot(self.ts, self.vel_xs, "--", c="hotpink", label="x")
        self.ax_vel.plot(self.ts, self.vel_ys, "--", c="green", label="y")
        self.ax_vel.plot(self.ts, self.vel_zs, "--", c="blue", label="z")

        self.ax_pos.plot(self.ts, self.xlocs, "--", c="hotpink", label="x")
        self.ax_pos.plot(self.ts, self.ylocs, "--", c="green", label="y")
        self.ax_pos.plot(self.ts, self.zlocs, "--", c="blue", label="z")

        self.ax_vel.legend()
        self.ax_pos.legend()

    def plot_data_3d(self):
        """Procedure that plots a model of the earth, moon and the craft's trajectory in R3"""

        locs = np.array([self.xlocs, self.ylocs, self.zlocs])
        traj = plt.plot(self.xlocs, self.ylocs, self.zlocs, lw=2, c="blue")[0]
        #self.ax.plot3D(self.xlocs, self.ylocs, self.zlocs, "blue")
        
        line_ani = animation.FuncAnimation(
            self.fig_3d,
            self.animate_traj,
            frames=len(self.xlocs),
            fargs=(locs, traj),
            interval=1,
            blit=False,
        )

        self.ax.set_box_aspect(aspect = (1,1,1))
        # 3D scatter plot of craft's trajectory
        #self.sc = self.ax.scatter3D(self.xlocs, self.ylocs, self.zlocs, cmap="Greens")

        # Calculation and plotting of earth's position
       
        earth_x = R_EARTH * np.outer(np.cos(self.u), np.sin(self.v))
        earth_y = R_EARTH * np.outer(np.sin(self.u), np.sin(self.v))
        earth_z = R_EARTH * np.outer(np.ones(np.size(self.u)), np.cos(self.v))

        self.earth = self.ax.plot_surface(earth_x, earth_y, earth_z, color="g")

        # Calculation and plotting of moon's position
        moon_cx, moon_cy, moon_cz = get_body_position(self.ts[-1], BodyEnum.Moon)
        moon_x = moon_cx + R_MOON * np.outer(np.cos(self.u), np.sin(self.v))
        moon_y = moon_cy + R_MOON * np.outer(np.sin(self.u), np.sin(self.v))
        moon_z = moon_cz + R_MOON * np.outer(np.ones(np.size(self.u)), np.cos(self.v))

        self.ax.plot_surface(moon_x, moon_y, moon_z, color="gray")

        #moon = self.plot_moon()

        # moon_ani = animation.FuncAnimation(
        #     self.fig_3d,
        #     self.animate_moon,
        #     frames=len(self.xlocs),
        #     fargs=(locs, moon),
        #     interval=100,
        #     blit=False
        # )

        plt.show()

    def animate_traj(self, num, locs, line):
        #print(self.ts)
        #self.ax.clear()

        #self.ax.plot3D(self.locs[0, :num+1], self.locs[1, :num+1], self.locs[2, :num+1], c='blue')
        #self.ax.scatter(self.locs[0, num], self.locs[1, num], self.locs[2, num], c='blue', marker='o')
        #self.ax.plot3D(self.locs[0, 0], self.locs[1, 0], self.locs[2, 0], c='black', marker='o')
        self.ax.set_title('Trajectory \nTime = ' + datetime.utcfromtimestamp(self.times[num]).strftime('%Y-%m-%d %H:%M:%S'))
        
        line.set_data(locs[0:2, :num])
        line.set_3d_properties(locs[2, :num])
        return line

    # def animate_moon(self, num, locs, moon):
        
    #     moon_cx, moon_cy, moon_cz = get_body_position(self.ts[-1], BodyEnum.Moon)
    #     moon_x = moon_cx + R_MOON * np.outer(np.cos(self.u), np.sin(self.v))
    #     moon_y = moon_cy + R_MOON * np.outer(np.sin(self.u), np.sin(self.v))
    #     moon_z = moon_cz + R_MOON * np.outer(np.ones(np.size(self.u)), np.cos(self.v))

    #     moon[0].remove()
    #     moon[0] = self.ax.plot_surface(moon_x, moon_y, moon_z, color="gray")


        #moon = self.plot_moon()
        #return moon

    # def plot_moon(self):
    #     u = np.linspace(0, 2 * np.pi, 60)
    #     v = np.linspace(0, np.pi, 60)
    #     moon_cx, moon_cy, moon_cz = get_body_position(self.ts[-1], BodyEnum.Moon)
        
    #     moon_x = moon_cx + R_MOON * np.outer(np.cos(u), np.sin(v))
    #     moon_y = moon_cy + R_MOON * np.outer(np.sin(u), np.sin(v))
    #     moon_z = moon_cz + R_MOON * np.outer(np.ones(np.size(u)), np.cos(v))
    #     return self.ax.plot_surface(moon_x, moon_y, moon_z, color="gray")



    # def update_annot(self, ind):

    #     pos = self.sc.get_offsets()[ind["ind"][0]]
    #     self.annot.xy = pos
    #     # text = " ".join([str(self.ts[n]) for n in ind["ind"]])
    #     text = " ".join([str(self.ts[ind["ind"][0]])])

    #     self.annot.set_text(text)

    # def hover(self, event) -> None:
    #     """Procedure that displays the annotation associated with the point that is hovered."""
    #     vis = self.annot.get_visible()
    #     if event.inaxes == self.ax:
    #         cont, ind = self.sc.contains(event)
    #         if cont:
    #             self.update_annot(ind)
    #             self.annot.set_visible(True)
    #             self.fig_2d.canvas.draw_idle()
    #         else:
    #             if vis:
    #                 self.annot.set_visible(False)
    #                 self.fig_2d.canvas.draw_idle()
