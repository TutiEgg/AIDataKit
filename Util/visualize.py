# NOT FINISHED

# TODO: This file should have classes, which other child-classes can inherit from
# TODO: Generalize it so it visualize x and y values (not signal). THis file is not only for signals

import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import scipy.signal as sig
from matplotlib.ticker import MultipleLocator, FormatStrFormatter, MaxNLocator


# Here should be several visualization function for every project

def visualize_onePlot_oneSignal():
    pass
def visualize_mulitplePlots_oneSignal_perPlot():
    pass
def visualize_onePlot_multipleSignals():
    pass

# TODO: temporary_function
def visualize_MVA(content):
    content



def visualize(content):
    # TODO: Check for Dimension_lenght, no ndarray, no list
    # Check content if type=dict
    if isinstance(content, dict):
        # Check type of content, split it and check the dimension of it -----------------------------------------------
        type_content_str = ut.get_type_nested_obj(content)
        custom_split_indicator = "<,>"
        splitted_type_list = ut.split_string_custom(type_content_str, custom_split_indicator)
        count_dimension = splitted_type_list.count("dict") + splitted_type_list.count("list")
        print(type_content_str, " = ", count_dimension)
        print(content)

        # Check if there is a list of dictionaries, if so change it to a nested Dict (list<dict> to dict<dict>) --------

        if count_dimension == 2:
            # Add one dictionary_dimension (Subplot)
            if splitted_type_list.count("list") > 0:
                pass
            new_content = dict()


        if count_dimension > 3:
            error_string = "[ERROR] content dimension should be exactly 3 (dict/list). " \
                           "[Dim:{}] Type: {} ".format(count_dimension, type_content_str)
            if "?" in splitted_type_list:
                error_string = error_string + "\nValues on the same level have different types, " \
                                              "if u are aware of it set check_dim to False"
            raise ValueError(error_string)
    # Change the dimension of content to a 3-dim
    # call function which visualizes content
    pass


def visualize_multiplePlots_multipleSignals(content, label_amount=[], sharex=True, sharey="col", filename="test"):
    """

    Parameters
    ----------
    content:        dict/list of Content to plot (has to be a nested/multidimensional one)
                    Format: subplot0: {
                                signal0: {
                                    key:value, # x, value= y
                                    key:value,
                                    key:value
                                },
                                signal1: {}
                            },
                            subplot1: {}

    label_amount:   Amount of x and y labels in one plot
                    list[x,y], x,y=int

    sharex:         decides whether all plots share their x-axis

    sharey:         decides whether all plots share their y-axis
                    possible values:    - 'row': each subplot row will share an y-axis.
                                        - 'col': each subplot column will share an y-axis.
                                        - True/False

    Returns
    -------

    """
    # Check type of content, split it and check the dimension of it ---------------------------------------------------
    type_content_str = ut.get_type_nested_obj(content)
    custom_split_indicator = "<,>"
    splitted_type_list = ut.split_string_custom(type_content_str, custom_split_indicator)
    print("asdsad", splitted_type_list)
    count_dimension = splitted_type_list.count("dict") + splitted_type_list.count("list")
    print(type_content_str, " = ", count_dimension)
    if count_dimension > 3:
        error_string = "[ERROR] content dimension should be 3 or less (dict/list). " \
                       "[Dim:{}] Type: {} ".format(count_dimension, type_content_str)
        raise ValueError(error_string)
    elif count_dimension == 2:
        if isinstance(content, dict):
            # Change content to 3_dim_dict
            temp_dict = dict()
            index = 0
            for signal in content:
                temp = dict()
                temp[signal] = content[signal]
                keyname = "Plot" + str(index)
                temp_dict[keyname] = temp
                index += 1
            content.clear()
            content = temp_dict

    # Check for same type on one Level
    if "?" in splitted_type_list:
        error_string = "\n[Warning] Values on the same level have different types, " \
                       "if u are aware of it set check_dim to False"


    color_list = ["blue", "green", "red", "orange", "purple", "brown", "yellow"]

    # Get and set amount of subplots ----------------------------------------------------------------------------------
    amount_subplots = 0
    if isinstance(content, dict):
        amount_subplots = len(content.keys())
    elif isinstance(content, list):
        amount_subplots = len(content)
    else:
        raise ValueError("[ERROR] content format is wrong: {}".format(type_content_str))

    fig, axs = plt.subplots(amount_subplots, sharex=sharex, sharey=sharey, squeeze=False)
    axs = axs.flatten()
    for single_plot in range(0, amount_subplots):
        color_index = 0

        for single_signal in content[list(content.keys())[single_plot]]:
            x_list = list(content[list(content.keys())[single_plot]][single_signal].keys())
            y_list = list(content[list(content.keys())[single_plot]][single_signal].values())

            color = color_list[color_index % len(color_list)]
            color_index += 1
            axs[single_plot].plot(x_list, y_list, color=color)

        if label_amount:
            axs[single_plot].xaxis.set_major_locator(MaxNLocator(label_amount[0]))
            axs[single_plot].yaxis.set_major_locator(MaxNLocator(label_amount[1]))

        axs[single_plot].grid(axis="y", alpha=0.5, color="black", linewidth="0.2")

        plt.xticks(rotation=50)


    plt.title(filename)
    fig.tight_layout()
    plt.show()



if __name__ == '__main__':
    print("Finished")


    #visualize_multiplePlots_multipleSignals()

