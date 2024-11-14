""" This class is for visualization of time series data"""

# todo:
# - more configurations : width zoomed field
# buttons for saving different party of the image
# button to step to next x values or something like that
# text fields for giving xmin and xmax
# slider for configuration of the down_sampling rate
# visualization of the labels in differen colors with a hrizontalo color bar chart etc.
# .... other optimizations


import os
import scipy, matplotlib
from scipy.fft import fft, fftfreq
from scipy import signal
import pandas as pd
import numpy as np
import math
from win32api import GetSystemMetrics
from tkinter import *
from matplotlib import pyplot as plt
from matplotlib.widgets import CheckButtons
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Rectangle
from matplotlib.widgets import Slider
from matplotlib.widgets import TextBox

from SWAI.DSP.filter import downsampling


def get_screen_size(unit='px'):
    """returns the size of the screen in px (width, height)
    Parameters
    unit : string ('px','mm','in')
    specifies the unit for the width and height
    """
    f_mm_to_inch = 1/25.4
    # creating tkinter window
    root = Tk()
    if unit == 'px':
        height = root.winfo_screenheight()
        width = root.winfo_screenwidth()
    elif unit == 'mm':
        height = root.winfo_screenmmheight()
        width = root.winfo_screenmmwidth()
    elif unit == 'in':
        height = root.winfo_screenmmheight()
        width = root.winfo_screenmmwidth()
        height = round(height * f_mm_to_inch, 2)
        width = round(width * f_mm_to_inch, 2)
    else:
        raise ValueError(" wrong unit")

    return width, height


class PlotWithCheckBoxes():
    """ plotting all data with checkboxes"""
    def __init__(self,
                 lst_data,
                 lst_data_name):
        """

        Parameters
        ----------
        lst_data : list with numpy arrays
        numpy array [0] is the x axis (e.g. sample number or time), [1] is the y axis
        """
        self.lst_data = lst_data
        self.lst_data_name = lst_data_name

    def plot(self):
        # create fig
        fig, ax = plt.subplots()
        lines = []
        for idx, data in enumerate(self.lst_data):
            line, = ax.plot(data[0], data[1], label=self.lst_data_name[idx])
            lines.append(line)
        fig.subplots_adjust(right=0.8)  # get space for the checkbox on the left side

        # create new axes object for the checkboxes
        rax = fig.add_axes([0.8, 0.7, 0.15, 0.2])  # [x_pos, y_pos, width, height]
        rax.axes.set_aspect('equal')
        labels = [str(line.get_label()) for line in lines]
        visibility = [line.get_visible() for line in lines]

        check = CheckButtons(rax, labels, visibility)

        def handleClick(label):
            index = labels.index(label)
            lines[index].set_visible(not lines[index].get_visible())
            plt.draw()

        check.on_clicked(handleClick)
        plt.show()


class ReducedDataset():
    """ for getting slices out of the full dataset"""
    def __init__(self,lst_data):
        """

        Parameters
        ----------
        lst_data : list
        includes numpy arrays with x and y values
        """
        self.lst_data = lst_data

    def get_idx_next_lower_data_value(self,data, value, direction='lower'):
        """
        Finds the idx next to the searched data value
        Parameters
        ----------
        data : numpy
        array with data [x,y]
        value : value which should be searched
        direction : 'lower or 'higher'

        Returns
        -------

        """
        #search for the first idx where the value is higher then target value
        idx, = np.where(data[0] >= value)
        if len(idx) > 0:
            if direction == 'lower':
                idx = idx[0]-1
            elif direction == 'higher':
                idx = idx[0]
        return idx


    def get_data_between_limit_values(self, x_min, x_max):
        """
        Returns a list with the data between the limits x_min and x_max of the x values (not indexes)
        Parameters
        ----------
        x_min : float
        value (not idx) in array for min
        x_max : float
        value (not idx) in array for min

        Returns
        -------

        """
        if x_min >= x_max:
            raise ValueError("min higher the max")

        lst_data_cutted = []
        for i, data in enumerate(self.lst_data):
            idx_min, = np.where(data[0] == x_min)
            # check if return value is empty
            if len(idx_min) == 0:
                idx_min = self.get_idx_next_lower_data_value(data,x_min,direction='higher')
            else:
                idx_min = idx_min[0]

            idx_max, = np.where(data[0] == x_max)
            if len(idx_max) == 0:
                idx_max = self.get_idx_next_lower_data_value(data,x_max,direction='lower')
            else:
                idx_max = idx_max[0]

            data_cutted = data[:, idx_min:idx_max]
            lst_data_cutted.append(data_cutted)

        return lst_data_cutted


class VisualizerTimeseriesData():
    """
    This class is for plotting time series data
    """
    def __init__(self,
                 lst_data,
                 lst_data_name):
        """

        Parameters
        ----------
        lst_data : list with numpy arrays
        numpy array [0] is the x axis (e.g. sample number or time), [1] is the y axis
        """
        self.lst_data = lst_data
        self.lst_data_name = lst_data_name
        self.lst_data_downsampled = self._downsampling_list(self.lst_data, number_samples=50000)
        self.lst_data_downsampled = lst_data#self._downsampling_list(self.lst_data, number_samples=5000)
        self.max_number_samples = self._get_number_max_samples()
        self._get_min_and_max_value(self.lst_data)
        self.main_x_min_value = 0

    def _get_number_max_samples(self):
        """get the max number of samples out of all data"""
        max_number_samples = 0
        for i, data in enumerate(self.lst_data):
            number_samples = data.shape[1]
            if number_samples > max_number_samples:
                max_number_samples = number_samples
        return max_number_samples

    def _get_min_and_max_value(self,lst_data):
        """
        get the min and max value for list of data
        Parameters
        ----------
        data : list
        list with data in it

        Returns
        -------
        """
        max_value = None
        min_value = None
        for i, data in enumerate(lst_data):
            dmax = data[1].max()
            dmin = data[1].min()
            if max_value == None:
                max_value = dmax
            elif dmax > max_value:
                max_value = dmax

            if min_value == None:
                min_value = dmin
            elif dmin < min_value:
                min_value = dmin
        return max_value, min_value


    def _downsampling_list(self,lst_data, number_samples):
        """Down sampling a list aof data with numpy arrays"""
        lst_data_downsampled = []
        for data in lst_data:
            data = downsampling(data, number_samples)
            lst_data_downsampled.append(data)
        return lst_data_downsampled

    def visulize_downsampled_output_data(self):
        """Visualized all the down sampled data"""
        checkbox_plot = PlotWithCheckBoxes(lst_data=self.lst_data_downsampled,
                                           lst_data_name=self.lst_data_name)
        checkbox_plot.plot()

    def visualize_output_timeseries(self):
        """
        Visualizes all the time series data in one plot where every data can be selected
        Returns
        -------

        """
        reduced_dataset = ReducedDataset(self.lst_data)

        def make_ticks_invisble(lst_axes):
            for i, ax in enumerate(lst_axes):
                #ax.tick_params(labelbottom=False, labelleft=False)
                ax.set_xticks([])
                ax.set_yticks([])

        # define fig size
        screen_width, screen_height = get_screen_size(unit='in')
        fig_height = 0.8 * screen_height
        fig_width = screen_height * 1.8
        if fig_width > screen_width:
            fig_width = screen_width

        ### create Layout ###
        fig = plt.figure(constrained_layout=True, figsize=(fig_width,fig_height))
        gs = GridSpec(10, 10, figure=fig)

        # first column
        ax_main = fig.add_subplot(gs[0:6, :8])
        ax_main_slider = fig.add_subplot(gs[6, :8])
        ax_overview = fig.add_subplot(gs[7:9, :8])
        ax_overview_slider = fig.add_subplot(gs[9, :8])

        # 2nd column
        ax_checkboxes = fig.add_subplot(gs[0:3, 8:])
        ax_conf_0 = fig.add_subplot(gs[3, 8:])
        ax_conf_1 = fig.add_subplot(gs[4, 8:])
        ax_conf_2 = fig.add_subplot(gs[5, 8:])
        ax_conf_3 = fig.add_subplot(gs[6, 8:])
        ax_conf_4 = fig.add_subplot(gs[7, 8:])
        ax_conf_5 = fig.add_subplot(gs[8, 8:])
        ax_conf_6 = fig.add_subplot(gs[9, 8:])

        make_ticks_invisble([ax_main_slider, ax_overview_slider, ax_checkboxes, ax_conf_0, ax_conf_1, ax_conf_2, ax_conf_3,
                             ax_conf_4, ax_conf_5, ax_conf_6])

        ### plot the data ###
        lines_main = []
        lines_overview =[]
        for idx, data in enumerate(self.lst_data_downsampled):
            line, = ax_main.plot(data[0], data[1], label=self.lst_data_name[idx])
            line2, = ax_overview.plot(data[0], data[1], label=self.lst_data_name[idx])
            lines_main.append(line)
            lines_overview.append(line2)



        # create checkboxes and add them
        labels = [str(line.get_label()) for line in lines_main]
        visibility = [line.get_visible() for line in lines_main]
        lines_by_label = {l.get_label(): l for l in lines_main}
        line_colors = [l.get_color() for l in lines_by_label.values()]

        check = CheckButtons(ax = ax_checkboxes,
                             labels= labels,
                             actives=visibility,
                             label_props = {'color': line_colors},
                             frame_props = {'edgecolor': line_colors},
                             check_props = {'facecolor': line_colors},
        )

        labels_overview = [str(line.get_label()) for line in lines_overview]
        visibility_overview = [line.get_visible() for line in lines_overview]
        check_overview = CheckButtons(ax = ax_conf_4,
                                      labels= labels_overview,
                                      actives = visibility_overview,
                                      label_props={'color': line_colors},
                                      frame_props={'edgecolor': line_colors},
                                      check_props={'facecolor': line_colors},
                                      )

        # create slider
        slider_overview = Slider(ax= ax_overview_slider,
                                 label='',
                                 valmin=ax_overview.get_xlim()[0],
                                 valmax=ax_overview.get_xlim()[1],
                                 valinit=0,
                                 valstep=1000)  # configuration depending on the length of the data

        slider_main = Slider(ax=ax_main_slider,
                             label='',
                             valmin=-500,
                             valmax=500,
                             valinit=0,
                             valstep=10)

        # create rectangle for showing the current position in the overview
        # define width of the rectangle by the amount of data
        max_value_input_data, min_value_input_data = self._get_min_and_max_value(self.lst_data)
        rect_overview_height = max_value_input_data - min_value_input_data
        rectangle_overview = Rectangle(xy=(0,min_value_input_data), # coordinates of lower left corner
                                       width=1,
                                       height = rect_overview_height,
                                       edgecolor='red',
                                       facecolor='None',
                                       fill=True,
                                       lw=5,
                                       zorder=2)

        # add the rectangles to diagrams
        ax_overview.add_patch(rectangle_overview)

        def update_plot_view(ax):
            # recompute the ax.dataLim
            ax.relim()
            # update ax.viewLim using the new dataLim
            ax.autoscale_view()

        def update_all_plots_by_new_data(start_value):
            data_cutted = reduced_dataset.get_data_between_limit_values(start_value,start_value+100000)
            for num, line in enumerate(lines_main):
                data = data_cutted[num]
                line.set_data(data[0],data[1])
            update_plot_view(ax_main)

        def handle_slider_overview(val):
            rectangle_overview.set_x(val)
            self.main_x_min_value = val
            update_all_plots_by_new_data(start_value=val)

        def handle_slider_main(val):
            val_new = self.main_x_min_value + val
            rectangle_overview.set_x(val_new)
            update_all_plots_by_new_data(start_value=val_new)

        def handle_main_checkbuttons_clicked(label):
            index = labels.index(label)
            lines_main[index].set_visible(not lines_main[index].get_visible())
            plt.draw()

        def handle_overview_checkbuttons_clicked(label):
            index = labels_overview.index(label)
            lines_overview[index].set_visible(not lines_overview[index].get_visible())
            plt.draw()

        check.on_clicked(handle_main_checkbuttons_clicked)
        check_overview.on_clicked(handle_overview_checkbuttons_clicked)
        slider_overview.on_changed(handle_slider_overview)
        slider_main.on_changed(handle_slider_main)

        plt.show()

