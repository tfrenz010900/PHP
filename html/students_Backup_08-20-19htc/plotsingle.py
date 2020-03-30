import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import string
import argparse
import matplotlib.image as mpimg
# 12-03-18 htc PYVer2.x Wiggy using - casued error in my PyCharm 3.x setup:  from StringIO import StringIO
from io import StringIO
import scipy as sp
import math
from scipy import interpolate

from matplotlib._png import read_png
from matplotlib.cbook import get_sample_data
from datetime import datetime as dt


# Disabling copy warning
pd.options.mode.chained_assignment = None

class BallPlot:
    """ Represents creation and storage of a 3d Line Plot representing pitch data """
    def __init__(self, x=[], y=[], z=[], angle="Front", title="", outf="", color="r"):
        self.data = {
            "x": x,
            "y": y,
            "z": z
        }
 #       self.x_range = [0, 48]
 #       self.y_range = [-12.5, 0]
 #       self.z_range = [0, 72]
#12/03/18 htc changed ranges to be realistic size of LED
        self.x_range = [40, 0]
        self.y_range = [-12.5, 0]
        self.z_range = [0, 70]

        self.color = color
        self.angle = angle
        self.outf = outf
        self.title = title
        """
        self.pitch = pitch
        self.file_path = file_path
        self.color = color
        
        # Reading in the pitch data
        self.data = self.read_pitch_data(int(num_frames))
        """
        # Creating the base plot
        self.fig = plt.figure(figsize=(4, 6))

        self.ax = self.fig.gca(projection='3d')
        im = plt.imread("target.png")

        x0,x1 = self.ax.get_xlim()
        y0,y1 = self.ax.get_ylim()
        self.ims = self.ax.imshow(im, extent=[x0-0.045, x1-0.957, y0-0.0415, y1-0.959], aspect='auto', zorder=-2)
        
        self.ax.set_xlim(self.x_range)
        self.ax.set_ylim(self.y_range)
        self.ax.set_zlim(self.z_range)

        self.views = {
            "Front": {
                "elev": 2,
                "azim": 90,
            },
            "Side": {
                "elev": 1,
                "azim": 0
            },
            "Top": {
                "elev": 90,
                "azim": 90
            }
        }


    def calc_coordinates(self, x, y, z):
        """ Calculates coordinates using custom calculations """
        alphabets = string.ascii_uppercase
        x = map(lambda val: float(alphabets.index(val)) * 1.3 if val != 0 else 0, x)
        y = map(lambda val: float(self.z_range[-1]) - (float(val) * 2.5), y)
        z = map(lambda val: float(val) * 2.5, z)
        return x, y, z


    def read_pitch_data(self, num_frames):
        """ Reads the pitch data file and returns an array of objects representing each pitch """
        df = pd.read_excel(filepath)

        row = df.iloc[self.pitch]
        # Turning in row NaN values to 0
        row.fillna(0, inplace=True)

        # Starting of x, y and z from x[0], y[0] and z[0]
        x, y, z = [row["X"]], [row["Y"]], [row["Z"]]
        for i in range(1, num_frames+1):
            x.append(row["X-{}".format(i)])
            y.append(row["Y-{}".format(i)])
            z.append(row["Z-{}".format(i)])

        # Reversing x, y, and z so that we're going from z[-1] to z[0] etc.
        x, y, z = map(lambda val: list(reversed(val)), [x, y, z])
        # Mapping x, y and z to specific calculations to get correct values
        x, y, z = self.calc_coordinates(x, y, z)
        # Creating the row data dictionary
        row_data = {
            "x": x,
            "y": z,
            "z": y,
            "pitch_num": row["PitchNumber"],
            "session_num": row["SessionNumber"],
            "pitch_speed": row["MPHPlateSpeed"],
            "customer": row["CustomerID"]
        }

        self.speed = row["MPHPlateSpeed"]
        self.customer = row["CustomerID"]
        self.session = row["SessionNumber"]
        self.pitch_num = row["PitchNumber"]

        return row_data


    def interpolate_data(self, x, y, z, movements, new_length=300):
        """ Interpolates the data using scipy """
        new_x = np.linspace(x.min(), x.max(), new_length)
        new_y = np.linspace(y.min(), y.max(), new_length)
        new_z = sp.interpolate.interp1d(y, z, kind='cubic')(new_y)

        return new_x, new_y, new_z


    def get_center_index(self, arr):
        return len(arr) // 2


    def curve_line(self, arr):
        """ Finds the median of the arr, and increase the value of the points as the 
            points get closer to the median; i.e. increase based on distance from median
            the lower the distance, the higher the increase in value
            ONLY IF THE STANDARD DEVIATION IN THE DATASET IS NOT ABOVE A CERTAIN VALUE
        """
        pass

    def mean(self, arr):
        return float(sum(arr)) / float(len(arr))

    def std_deviation(self, arr):
        mean = self.mean(arr)
        elems = [(i-mean)**2 for i in arr]
        return math.sqrt(sum(elems) / len(elems))

    def curve_intensity(self, arr):
        """ Measures how intense a curve is; i.e. the average of all slopes in a given line (p2-p1 for all points) """
        #mean = self.mean(arr)
        slopes = []
        for index in range(len(arr)):
            if index == 0:
                slopes.append(0)
            else:
                slopes.append(arr[index] - arr[index-1])
        return self.std_deviation(slopes)
        #elems = sum([(i-mean) ** 2 for i in arr])
        #return elems / len(arr)

    def imitated_curve_base(self, arr):
        """ Creates a curve by adding to the datapoints based on their close-ness to the middle """
        center_index = len(arr) // 2
        mean = self.mean(arr)
        for index in range(len(arr)):
            if index == 0 or index == len(arr)-1:
                continue
            distance_from_center = abs(center_index - index)
            to_add = float(mean) / 7
            if distance_from_center == 0:
                distance_from_center = 0.8
            to_add = to_add / distance_from_center
            arr[index] += to_add
        return arr


    def imitated_curve_splined(self, arr):
        """ Creates a curve by adding to the datapoints based on their close-ness to the middle """
        center_index = len(arr) // 2
        mean = self.mean(arr)
        start, end = arr[0], arr[-1]
        for index in range(len(arr)):
            if index == 0 or index == len(arr)-1:
                continue
            if index < center_index:
                distance_from_edge = abs(index)
            else:
                distance_from_edge = abs(len(arr)-index)
            distance_from_center = abs(center_index - index)
            to_add = mean-arr[index]
            #to_add = self.mean([start, end])
            #to_add = to_add / float(distance_from_center)
            arr[index] += distance_from_edge / mean
        return arr


    def generate_plot(self):
        row = self.data

        x, y, z = row["x"], row["y"], row["z"]
        # Turning arrays to nparrays
        x, y, z = np.asarray(x), np.asarray(y), np.asarray(z)
        # Calculating movement (total change in columns at start at beginning)
        movements = {
            "x": (x[0] - x[-1]) * 1.5,
            "y": (y[0] - y[-1]),
            "z": z[-1] - z[0]
        }


        if self.curve_intensity(z) < 1.0:
            new_z = self.imitated_curve_base(z)





  #      interpolation_enabled = True
        interpolation_enabled = False







        if len(x) > 1 and interpolation_enabled:
            new_x, new_y, new_z = self.interpolate_data(x, y, z, movements)
        else:
            new_x, new_y, new_z = x, y, z
        # If curve intesity of new_z is less than 0.01, apply a rolling function to create a fake curve
        """
        print("Pitch {}; Start {}; End {}; Std Dev Z {}.".format(self.pitch_num, z[0], z[-1], self.curve_intensity(new_z)))
        if self.curve_intensity(new_z) < 0.01:
            new_z = self.imitated_curve_splined(new_z)
            new_x, new_y, new_z = self.interpolate_data(x, y, new_z, movements)
        """

        # Plotting the x, y and z values
        self.ax.plot(new_x, new_y, new_z, zorder=-1, linewidth=3, color=self.color)
        #plt.show()
        # Drawing the ball (sphere) at the last point)
        self.ax.scatter(new_x[-1], new_y[-1], new_z[-1], color=self.color, s=100, zorder=1)
        # Adding no data to plot text
        if len(z) <= 1:
            self.ax.text(new_x[-1]-5, new_y[-1], new_z[-1], "No data to plot", color="red", fontSize=14)
        self.fig.tight_layout()
        self.write_plot_to_file(movements=movements)
        return


    def write_plot_to_file(self, movements=None):
        """ Writes the final plot in two angles to output files """
        """
        self.fig.text(0.8, 0.8, "\nCustomer #{}\nSession #{}\nPitch #{}\nSpeed {}".format(self.customer,
            self.session, self.pitch_num, self.speed), fontsize=10)
        """
        # Only create side plot if we only have one point
        # self.fig.suptitle("{view} View - Movement (X, Y, Z) - ({x}, {y}, {z})".format(view=out, **movements), fontsize=12)
        #if len(self.data["z"]) <= 1:
            #elf.fig.suptitle("No data to plot", fontsize=14)
        self.fig.suptitle(self.title.replace(r"\n", "\n"), fontsize=12)
        self.ax.view_init(**self.views[self.angle])
        view = StringIO()
        """
        filename = "images\\{customer}{session}{start}{date}{side}.png".format(
            side=out, customer=self.customer, session=self.session, date=dt.now().strftime("%Y%m%d"),
            start="P%s" % str(self.pitch_num).zfill(3))
        """
        if "front" not in self.angle.lower():
            self.ims.remove()

        self.fig.savefig(self.outf, bbox_inches="tight")
        return


if __name__ == "__main__":
    filepath = "TRF-EZ-PitchingData20180801.xlsx"         #12/5/18 htc - this file NOT used anymore, direct args on command line now.
    # Creating command line arguments
    ap = argparse.ArgumentParser()
    """
    ap.add_argument("-inp", "--input_file", help="Path to PitchData file", required=True)
    ap.add_argument("-p", "--pitches", type=int, nargs="+", help="Space separated pitch numbers", required=True)
    ap.add_argument("-c", "--color", type=str, help="Space separated color strings", required=True)
    ap.add_argument("-n", "--num_frames", type=str, help="Number of frames provided", required=True, default=5)
    """
    ap.add_argument("-o", "--outf", help="Path to the output ", required=True)
    ap.add_argument("-p", "--pitch_data", type=str, help="Comma + | separated pitch data in the form of (X,Y,Z)|(X2,Y2,Z2)|...",
        required=True)
    ap.add_argument("-a", "--angle", help="Angle for generated outf. Values must be Top|Side|Front", required=True)
    ap.add_argument("-c", "--color", type=str, help="Color string", required=True)
    ap.add_argument("-t", "--title", type=str, help="Figure title for the plot", required=True)

    args = ap.parse_args()
    """
    for pitch in args.pitches:
        plot = BallPlot(args.input_file, pitch=pitch, color=args.color, num_frames=args.num_frames)
        plot.generate_plot()
    """
    pitches = args.pitch_data.split("|")
    pitches = [i.split(",") for i in pitches]
    x = [float(i[0]) for i in pitches]
    y = [float(i[1]) for i in pitches]
    z = [float(i[2]) for i in pitches]

    plot = BallPlot(x=x, y=y, z=z, angle=args.angle, color=args.color, title=args.title, outf=args.outf)
    plot.generate_plot()