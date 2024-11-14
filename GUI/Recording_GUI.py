# Gui Imports
import math
import copy
import random
import tkinter as tk
from tkinter import messagebox, ttk, VERTICAL, HORIZONTAL, N, S, E, W, END
from tkinter.scrolledtext import ScrolledText
import tkinter.font as tkFont
# ToF Serialimports


import serial
import serial.tools.list_ports
# KWS imports
# import pyaudio
import wave

# Threading for Recordings imports
import threading
import multiprocessing as mp
import queue

# General imports
import time
import datetime
import os
import numpy as np

from tqdm import tqdm
# WICHTIG es fehlen die Imports aus dem AIDataKit-Projekt

# LINUX USER #
# sudo apt-get install fonts-symbola


# TODO: Serial_devices müssen beim connecten gelabeld werden und später in der Dateierstellung miteingebracht werden
# TODO: Bei Fehler prints soll ein TOPlevel-gui erstellt werden mit der Fehlermeldung und der Informationen + Pfad im COde
# Global save variables
connected_devices = list()
allDevices = dict()
btnDevices = dict()  # To Check if a button of this specific devices exist, also includes boolean if its connected or not
recording_dict = dict()
device_dict = dict()

# Bool-value: is recording or not (Update devices or not)
global recording_bool
recording_bool = False
# Bool-value: stop recording_process manually, without waiting until 'time_passed is over max_time'
global stop_recording
stop_recording = False

MODE_LIST = ["tof", "kws", "mva"]  # List of all Options
BAUDRATE_list = [57600, 115200, 230400, 460800, 921600]
RYTHM_INTERVAL = 1  # in seconds
fun_mode = False

# Global Variables
RECORDING_MODE = "mva"

# Global Variables ToF
# BAUDRATE = 460800
BAUDRATE = 115200
RYTHM_INTERVAL = 1  # in seconds
fun_mode = False

# Global Variables KWS
# FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 16000
CHUNK = 1024
RECORD_SECONDS = 2

# Global Variables MVA
SAMPLERATE = 400  # sample per seconds

# Global placeholder Variables
to_round_value = 3  # n digits to round
interval_update_gui = 1
interval_recording = 0.01

# Global Colors
Color_bg = {
    # General
    "bg": "#00496c",
    "border_frame": "#86dcf9",
    "button": "#375a7f",
    "label": "#00496c",
    "entry": "#d0f9fd",
    "dropdown": "#375a7f",
    "scrolled_text": "#82c6ee",
    "tooltip": "#F1ED71",

    "green": "#42e2b8",
    "red": "#eb8a90",

    # Help Gui related
    "help_button": "#d64161",
    "help_frame": "#eca1a6",

    # Main-Gui related
    "open_button_on": "#375a7f",
    "open_button_off": "#eb8a90",

    # Serial-Gui related
    "close_button": "#d64161",

    # Recording-Gui related
    "filename": "#82c6ee",
    "show_time": "#00496c",
    "start_button_on": "#42e2b8",
    "start_button_off": "#42e2b8",
    "stop_button_on": "#eb8a90",
    "stop_button_off": "#eb7a90",

}
Color_fg = {
    # General
    "label_frame": "#ffffff",
    "button": "#ffffff",
    "label": "#ffffff",
    "entry": "#222222",
    "dropdown": "#ffffff",
    "help_button": "#222222",
    "scrolled_text": "#ffffff",
    "tooltip": "#222222",

    "red": "#ff8080",
    "green": "#80ff80",

    # Main-Gui related
    "open_button_on": "#ffffff",
    "open_button_off": "#222222",

    # Serial-Gui related
    "close_button": "#222222",

    # Recording-Gui related
    "filename": "#ffffff",
    "show_time": "#ffffff",
    "start_button_on": "#ffffff",
    "start_button_off": "#ffffff",
    "stop_button_on": "#ffffff",
    "stop_button_off": "#ffffff",

}


def set_styles(gui):
    style = ttk.Style(gui)

    style.configure("TFrame", background=Color_bg["bg"], bordercolor=Color_bg["border_frame"],
                    fieldbackground="black", foreground=Color_fg["label_frame"])
    style.configure("TLabelframe", background=Color_bg["bg"], bordercolor=Color_bg["border_frame"],
                    fieldbackground="black", foreground=Color_fg["label_frame"])
    style.configure("TLabelframe.Label", background=Color_bg["bg"], font=tkFont.Font(family="Lucida Grande", size=12),
                    fieldbackground="black", foreground=Color_fg["label_frame"])
    style.configure('TPanedwindow', background=Color_bg["bg"])

    return style


# Main Class of Recording =============================================================================================
class recording:

    def __init__(self, path):
        self.gui = tk.Tk()
        self.path = path

        # Recording
        self.recording_thread_list = list()
        self.time_label_text = tk.StringVar()
        self.time_label_text.set("")
        self.time_passed = datetime.timedelta(seconds=0)
        self.show_time_text = tk.StringVar()
        self.show_time_text.set("")
        self.start_stop_button = tk.Button
        self.running = False

        self.audio = None
        self.isHelp = False

        # Entry
        self.duration_options = None
        self.duration_entry = None
        self.filename_idtype_options = None
        self.filename_entry = None

        self.main_GUI()

    # Start function --------------------------------------------------------------------------------------------------
    def main_GUI(self):
        """
        Main Gui
        Returns
        -------

        """

        # Init GUI #
        self.gui.title("Recording GUI")
        self.gui.columnconfigure(0, weight=1, uniform="fred")
        self.gui.rowconfigure(0, weight=1, uniform="fred")
        width = 800
        height = 400
        self.gui.geometry("{}x{}".format(width, height))
        self.gui.minsize(700, 350)
        self.gui.configure(bg=Color_bg["bg"])

        # Reset ishelp boolean everytime a new gui is opend
        self.isHelp = False

        # Styles
        style = set_styles(self.gui)

        font_list = {
            "connected_serial": tkFont.Font(family="Lucida Grande", size=12),
            "serial_button": tkFont.Font(family="Lucida Grande", size=12),
            "label": tkFont.Font(family="Lucida Grande", size=16),
            "start_button": tkFont.Font(family="Lucida Grande", size=15),
            "help_button": tkFont.Font(family="Lucida Grande", size=20),
            "help_frame": tkFont.Font(family="Lucida Grande", size=15)
        }

        # Create the panes and frames ---------------------------------------------------------------------------------
        main_frame = ttk.Frame(self.gui)
        main_frame.columnconfigure(0, weight=1, uniform="fred")
        main_frame.rowconfigure(0, weight=1, uniform="fred")
        main_frame.pack(fill="both")

        help_frame = ttk.Frame(self.gui, width=width, height=height)
        help_frame.columnconfigure(0, weight=1, uniform="fred")
        help_frame.rowconfigure(1, weight=1, uniform="fred")
        help_frame.grid_propagate(0)
        mult_value = 0.36
        help_frame.place(anchor="w", relwidth=1, rely=1, y=height * mult_value)  # Start position

        vertical_pane = ttk.PanedWindow(main_frame, orient=VERTICAL)
        vertical_pane.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        style.configure('Treeview', background='orange', foreground='grey',
                        fieldbackground='orange')
        horizontal_pane = ttk.PanedWindow(vertical_pane, orient=HORIZONTAL)
        vertical_pane.add(horizontal_pane)
        frame_serialize = ttk.Labelframe(vertical_pane, text="Choose Serials to Connect", padding=20)
        frame_serialize.columnconfigure(1, weight=1)
        horizontal_pane.add(frame_serialize, weight=1)

        frame_entry = ttk.Labelframe(horizontal_pane, text="Entrys", padding=10)
        frame_entry.columnconfigure(0, weight=1)
        frame_entry.columnconfigure(1, weight=2)
        frame_entry.columnconfigure(2, weight=1)
        frame_entry.rowconfigure(0, weight=1)
        horizontal_pane.add(frame_entry, weight=1)

        frame_open_recordings = ttk.Labelframe(vertical_pane, text="Start Recording", height=height / 3)
        frame_open_recordings.columnconfigure(0, weight=1)
        frame_open_recordings.grid_propagate(0)
        vertical_pane.add(frame_open_recordings, weight=1)

        self.gui.protocol('WM_DELETE_WINDOW', self.gui.destroy)
        self.gui.bind('<Control-q>', self.gui.destroy)

        # Start Button ------------------------------------------------------------------------------------------------
        open_Button = tk.Button(master=frame_open_recordings, text="Open Gui", state=tk.DISABLED, padx=5, pady=5,
                                font=font_list["start_button"], command=lambda: self.recording_GUI())

        # Serialize --------------------------------------------------------------------------------------------------

        # serial Connection List
        serialConnectionButton = tk.Button(master=frame_serialize, text="Serial Connection Setup", height=3,
                                           bg=Color_bg["button"],
                                           fg=Color_fg["button"], font=font_list["serial_button"],
                                           command=lambda: self.serial_GUI())
        # Connected serials Label_list
        connected_serial_label = tk.Label(master=frame_serialize, fg=Color_fg["red"], bg=Color_bg["bg"],
                                          font=font_list["connected_serial"],
                                          text='Connected serials: ' + ','.join(connected_devices))

        # Duration Label ----------------------------------------------------------------------------------------------

        duration_label_before = tk.Label(master=frame_entry, text="Duration", bg=Color_bg["label"], fg=Color_fg["label"]
                                         , font=font_list["label"])
        self.duration_entry = tk.Entry(master=frame_entry, bg=Color_bg["entry"], fg=Color_fg["entry"])
        self.duration_entry.insert(0, "9")

        duration_time_list = ["seconds", "minutes"]  # List of all Options
        self.duration_options = tk.StringVar(master=frame_entry)  # SringVar
        self.duration_options.set(duration_time_list[0])  # Default
        duration_dropdown = tk.OptionMenu(frame_entry, self.duration_options, *duration_time_list)  # DropMenu Object
        duration_dropdown.config(bg=Color_bg["dropdown"], fg=Color_fg["dropdown"])
        duration_dropdown["menu"].config(bg=Color_bg["entry"])

        # Filename label ----------------------------------------------------------------------------------------------

        filename_label = tk.Label(master=frame_entry, text="Filename", bg=Color_bg["label"], fg=Color_fg["label"],
                                  font=font_list["label"])
        self.filename_entry = tk.Entry(master=frame_entry, bg=Color_bg["entry"], fg=Color_fg["entry"])
        self.filename_entry.insert(0, "username")

        filename_idtype_list = ["date", "numbers"]  # List of all Options
        self.filename_idtype_options = tk.StringVar(master=frame_entry)  # SringVar
        self.filename_idtype_options.set(filename_idtype_list[0])  # Default
        filename_idtype_dropdown = tk.OptionMenu(frame_entry, self.filename_idtype_options,
                                                 *filename_idtype_list)  # DropMenu Object
        filename_idtype_dropdown.config(bg=Color_bg["dropdown"], fg=Color_fg["dropdown"])
        filename_idtype_dropdown["menu"].config(bg=Color_bg["entry"])

        # rhythm-Interval label ---------------------------------------------------------------------------------------

        rhythm_label = tk.Label(master=frame_entry, text="Rhythm", bg=Color_bg["label"], fg=Color_fg["label"],
                                font=font_list["label"])
        self.rhythm_entry = tk.Entry(master=frame_entry, bg=Color_bg["entry"], fg=Color_fg["entry"])
        self.rhythm_entry.insert(0, "1")

        # Help Button -------------------------------------------------------------------------------------------------

        help_button = tk.Button(master=help_frame, text="❔",
                                font=font_list["help_button"], bg=Color_bg["help_button"], fg=Color_fg["help_button"],
                                command=lambda: self.helping_GUI_verti(help_frame, mult_value, height=height))

        help_content_frame = tk.Frame(master=help_frame, bg=Color_bg["help_frame"])
        help_content = tk.Label(master=help_content_frame, bg=Color_bg["help_frame"],
                                fg=Color_fg["help_button"], font=font_list["help_frame"],
                                text="[Step1] click on the 'Serial Connection Setup'-Button and connect your devices\n"
                                     "[Step2] Set a record-duration by typing any Number of your liking\n"
                                     "[Step3] Set a Name and Format of the created File at the end\n"
                                     "[Step4] Set a Rhythm, which will help you stay in tact\n"
                                     "[Step5] click on 'Open GUI'-Button")

        # set Hover Event on every Label/Button -----------------------------------------------------------------------
        createToolTip(open_Button, text="Opens Recording GUI"
                                        "\n[Requirements] "
                                        "\n - At least one connected Device,"
                                        "\n - Every Entry filled correctly")
        createToolTip(serialConnectionButton, text="Opens Serial Connecting GUI"
                                                   "\nconnect Devices")
        createToolTip(duration_label_before, text="Set the Duration of one Recording"
                                                  "\n[Format] = Number (float, int)")
        createToolTip(duration_dropdown, text="Choose in which format your entry is"
                                              "\n[Format] = seconds/minutes")
        createToolTip(filename_label, text="Set the name of the created File"
                                           "\n[Format] = String")
        createToolTip(filename_idtype_dropdown, text="Choose which format-ending "
                                                     "\nyour filename should have"
                                                     "\n[Format] = Date/numbers")
        createToolTip(rhythm_label, text="Set rhythm of Impulsevisualization")

        # Place Labels ------------------------------------------------------------------------------------------------

        # Start Button
        open_Button.grid(column=0, row=0, sticky="ew", padx=10, pady=10)

        # serialize
        serialConnectionButton.grid(column=1, row=0, sticky=(W, E), padx=10, pady=5)
        connected_serial_label.grid(column=1, row=1, sticky=W, padx=10, pady=5)
        # Duration
        duration_label_before.grid(column=0, row=0, sticky="nw", padx=10, pady=5)
        self.duration_entry.grid(column=1, row=0, sticky="nw", padx=10, pady=5)
        duration_dropdown.grid(column=2, row=0, sticky="nw", padx=10)
        # Filename
        filename_label.grid(column=0, row=1, sticky="nw", padx=10, pady=5)
        self.filename_entry.grid(column=1, row=1, sticky="nw", padx=10, pady=5)
        filename_idtype_dropdown.grid(column=2, row=1, sticky="nw", padx=10)
        # Rhythm
        rhythm_label.grid(column=0, row=2, sticky="nw", padx=10, pady=10)
        self.rhythm_entry.grid(column=1, row=2, sticky="nw", padx=10, pady=12)
        # Help Button
        help_button.grid(column=0, row=0, sticky="nesw")
        help_content_frame.grid(column=0, row=1, sticky="nesw")
        help_content.pack(side="top", padx=5, pady=5)

        # Start Thread ------------------------------------------------------------------------------------------------
        tr_con = updateThread(update_main_GUI,
                              interval=interval_update_gui,
                              gui=self.gui,
                              serial_label=connected_serial_label,
                              open_Button=open_Button
                              )
        self.gui.mainloop()

    # GUI's -----------------------------------------------------------------------------------------------------------
    def serial_GUI(self):
        """
        GUI where devices (serials) can be connected/disconnected

        Returns
        -------

        """
        # Serial init
        serialConnectionWindow = tk.Toplevel(self.gui)
        serialConnectionWindow.title("Serial Connection")

        width = 500
        height = 350
        serialConnectionWindow.minsize(width - 50, height - 50)

        serialConnectionWindow.geometry("{}x{}".format(width, height))
        serialConnectionWindow.config(background=Color_bg["bg"])

        main_frame = ttk.Frame(serialConnectionWindow)
        main_frame.columnconfigure(0, weight=1, uniform="fred")
        main_frame.rowconfigure(0, weight=1, uniform="fred")
        main_frame.pack(fill="both")

        # Reset ishelp boolean everytime a new gui is opend
        self.isHelp = False

        # Style
        set_styles(serialConnectionWindow)
        font_list = {
            "list_serial": tkFont.Font(family="Lucida Grande", size=12),
            "serial_button": tkFont.Font(family="Lucida Grande", size=12),
            "close_button": tkFont.Font(family="Lucida Grande", size=12),
            "help_button": tkFont.Font(family="Lucida Grande", size=12),
            "help_frame": tkFont.Font(family="Lucida Grande", size=12)
        }
        # Serial label ------------------------------------------------------------------------------------------------
        frame_serial = ttk.Frame(main_frame)

        serial_list_label = tk.Label(frame_serial, text='List of all serials: ' + ','.join(allDevices.keys()),
                                     bg=Color_bg["bg"], fg=Color_fg["label"], font=font_list["list_serial"])

        # Help Frame --------------------------------------------------------------------------------------------------
        help_frame = ttk.Frame(serialConnectionWindow, width=width, height=height)
        help_frame.columnconfigure(0, weight=1, uniform="fred")
        help_frame.rowconfigure(1, weight=1, uniform="fred")
        help_frame.grid_propagate(0)
        # help_frame.place(x=0, y=height-height/10) # Start position
        mult_value = 0.41
        help_frame.place(anchor="w", relwidth=1, rely=1, y=height * mult_value)  # Start position

        # Mode label --------------------------------------------------------------------------------------------------
        frame_mode = ttk.Frame(main_frame)

        self.mode_options = tk.StringVar(master=frame_mode)  # StringVar
        self.mode_options.set(MODE_LIST[0])  # Default
        mode_dropdown = tk.OptionMenu(frame_mode, self.mode_options,
                                      *MODE_LIST)  # DropMenu Object
        mode_dropdown.config(bg=Color_bg["dropdown"], fg=Color_fg["dropdown"])
        mode_dropdown["menu"].config(bg=Color_bg["entry"])

        mode_label = tk.Label(frame_mode, text="Choose Mode", bg=Color_bg["bg"], fg=Color_fg["label"],
                              font=font_list["list_serial"])

        # Baudrate Label -----------------------------------------------------------------------------
        frame_baud = ttk.Frame(main_frame)

        self.baud_options = tk.StringVar(master=frame_baud)  # StringVar
        self.baud_options.set(BAUDRATE_list[-1])  # Default
        baud_dropdown = tk.OptionMenu(frame_baud, self.baud_options,
                                      *BAUDRATE_list)  # DropMenu Object
        baud_dropdown.config(bg=Color_bg["dropdown"], fg=Color_fg["dropdown"])
        baud_dropdown["menu"].config(bg=Color_bg["entry"])

        baud_label = tk.Label(frame_baud, text="Choose Baudrate", bg=Color_bg["bg"], fg=Color_fg["label"],
                              font=font_list["list_serial"])

        # Thread ------------------------------------------------------------------------------------------------------
        # Updates the Gui every interval
        tr = updateThread(update_serial_GUI,
                          interval=1,
                          gui=frame_serial,
                          label=serial_list_label
                          )
        serialConnectionWindow.wm_protocol("WM_DELETE_WINDOW",
                                           lambda: self.on_closing_serial_gui(serialConnectionWindow, tr))

        # Close Button ------------------------------------------------------------------------------------------------
        frame_close = ttk.Frame(main_frame)
        close_button = tk.Button(master=frame_close, text="❌ Close",
                                 font=font_list["close_button"], bg=Color_bg["close_button"],
                                 fg=Color_fg["close_button"],
                                 command=lambda: self.on_closing_serial_gui(serialConnectionWindow, tr))

        # Help Button -------------------------------------------------------------------------------------------------
        help_button = tk.Button(master=help_frame, text="❔",
                                font=font_list["help_button"], bg=Color_bg["help_button"], fg=Color_fg["help_button"],
                                command=lambda: self.helping_GUI_verti(help_frame, mult_value, height=height))

        help_content_frame = tk.Frame(master=help_frame, bg=Color_bg["help_frame"])
        help_content = tk.Label(master=help_content_frame, bg=Color_bg["help_frame"],
                                fg=Color_fg["help_button"], font=font_list["help_frame"],
                                text="[Step1] Connect Devices and wait until they are shown up on the GUI\n"
                                     "[Step2] Connect Devices by clicking on the Button until it turns green\n"
                                     "[Step3] Choose a Mode for the Type of Device you connected\n"
                                     "[Step4] Close the GUI\n")

        # set Hover Event on every Label/Button -----------------------------------------------------------------------
        createToolTip(mode_dropdown, text="Choose between Modes of Devices"
                                          "\n[Modes] "
                                          "\n - ToF"
                                          "\n - KWS")
        createToolTip(close_button, text="Save and close this GUI")

        # pack Label/Buttons on Gui -----------------------------------------------------------------------------------

        close_button.pack(side="bottom", padx=10, pady=5)

        serial_list_label.pack(side="top", padx='5', pady='20')

        mode_label.pack(side="top", padx="5", pady=(20, 5))
        mode_dropdown.pack(side="top", padx="5", pady=(5, 5))

        baud_label.pack(side="top", padx="5", pady=(5, 5))
        baud_dropdown.pack(side="top", padx="5", pady=(5, 20))

        frame_serial.pack()
        frame_mode.pack()
        frame_baud.pack()
        frame_close.pack()

        help_button.grid(column=0, row=0, sticky="nesw")
        help_content_frame.grid(column=0, row=1, sticky="nesw")
        help_content.pack(side="top", padx=5, pady=5)

    def recording_GUI(self):
        """
        GUI where recording are visualized and can be stopped/saved

        Returns
        -------

        """
        global RECORDING_MODE

        # Check if Audio is Null
        if not self.audio and RECORDING_MODE == "KWS":
            self.audio = pyaudio.PyAudio()

        error_msg = None
        # Check if all entrys were made
        if self.duration_options.get() and self.duration_entry.get() \
                and self.filename_idtype_options.get() and self.filename_entry.get() and self.rhythm_entry.get():
            if check_If_Number(self.duration_entry.get()) and check_If_Number(self.rhythm_entry.get()):

                # Recodring_gui init ----------------------------------------------------------------------------------
                recordingWindow = tk.Toplevel(self.gui)
                recordingWindow.title("Recording Gui")
                width = 900
                height = 600
                recordingWindow.geometry("{}x{}".format(width, height))
                recordingWindow.minsize(800, 550)
                recordingWindow.columnconfigure(0, weight=1)
                recordingWindow.rowconfigure(0, weight=1)
                recordingWindow.configure(bg=Color_bg["bg"])

                # Styles
                style = set_styles(recordingWindow)

                font_list = {
                    "filename": tkFont.Font(family="Lucida Grande", size=12),
                    "start_button": tkFont.Font(family="Lucida Grande", size=12),
                    "label": tkFont.Font(family="Lucida Grande", size=10),
                    "scrolled_text": tkFont.Font(family="TkFixedFont", size=10),
                    "entry": tkFont.Font(family="TkFixedFont", size=10),
                    "show_time": tkFont.Font(family="TkFixedFont", size=16),
                    "help_button": tkFont.Font(family="Lucida Grande", size=20),
                    "help_frame": tkFont.Font(family="Lucida Grande", size=16)
                }

                # Reset ishelp boolean everytime a new gui is opend
                self.isHelp = False

                # Set MODE and BAUDRATE
                RECORDING_MODE = self.mode_options.get()

                global BAUDRATE
                BAUDRATE = self.baud_options.get()

                # Recording GUI ---------------------------------------------------------------------------------------
                main_frame = ttk.Frame(recordingWindow)
                main_frame.columnconfigure(0, weight=1, uniform="fred")
                main_frame.rowconfigure(0, weight=1, uniform="fred")
                main_frame.pack(fill="both", padx=(5, 50))

                # Create the panes and frames
                help_frame = ttk.Frame(recordingWindow, width=width, height=height)
                help_frame.columnconfigure(1, weight=1, uniform="fred")
                help_frame.rowconfigure(0, weight=1, uniform="fred")
                help_frame.grid_propagate(0)
                mult_value = 0.95

                help_frame.place(anchor="e", relheight=1, relx=1, x=width * mult_value, y=height / 2)  # Start position
                # help_frame.place(anchor="w", relwidth=1, rely=1, y=height * mult_value)  # Start position

                vertical_pane = ttk.PanedWindow(main_frame, orient=VERTICAL)
                vertical_pane.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
                horizontal_pane = ttk.PanedWindow(vertical_pane, orient=HORIZONTAL)
                vertical_pane.add(horizontal_pane)

                frame_entrys = ttk.Labelframe(horizontal_pane, text="[Mode] " + self.mode_options.get())

                horizontal_pane.add(frame_entrys, weight=1)

                frame_start = ttk.Labelframe(horizontal_pane, text="Start/stop")
                frame_start.columnconfigure(0, weight=1)
                frame_start.rowconfigure(0, weight=1)
                horizontal_pane.add(frame_start, weight=1)

                frame_log = ttk.Labelframe(vertical_pane, text="Logs")
                vertical_pane.add(frame_log, weight=1)

                frame_save = ttk.Labelframe(vertical_pane, text="Save/Discard", height=200)
                vertical_pane.add(frame_save, weight=1)
                frame_save.rowconfigure(0, weight=1)
                frame_save.columnconfigure(0, weight=1)
                frame_save.columnconfigure(1, weight=1)
                # ttk.Label(frame_save, text="").grid(column=1, row=1, sticky=W, pady=50, padx=30)  # label_placeholder

                recordingWindow.wm_protocol("WM_DELETE_WINDOW",
                                            lambda: self.on_closing_recording_gui(recordingWindow,
                                                                                  self.recording_thread_list))

                # Create Device dict ----------------------------------------------------------------------------------
                # TODO: 2 different scroll-logs
                if self.mode_options.get() == "MVA":
                    column_index = 0
                    for con_dev in connected_devices:
                        device_dict[con_dev] = dict()

                        # Create log_queue and add to dict
                        log_queue = queue.Queue()
                        device_dict[con_dev]["log_queue"] = log_queue

                        # create scrolled_text and add to dict
                        def create_scrolled_text():
                            scrolled_text = ScrolledText(frame_log, state='disabled')
                            scrolled_text.configure(bg=Color_bg["scrolled_text"], fg=Color_fg["scrolled_text"],
                                                    font=font_list["scrolled_text"])
                            scrolled_text.grid(column=column_index, row=0, sticky="nsew")
                            # Makes it stretchy
                            frame_log.columnconfigure(column_index, weight=1)
                            frame_log.rowconfigure(column_index, weight=1)
                            return scrolled_text

                        device_dict[con_dev]["scrolled_text"] = create_scrolled_text()
                        column_index += 1

                else:
                    column_index = 0
                    for con_dev in connected_devices:
                        device_dict[con_dev] = dict()

                        # Create log_queue and add to dict
                        log_queue = queue.Queue()
                        device_dict[con_dev]["log_queue"] = log_queue

                        # create scrolled_text and add to dict
                        def create_scrolled_text():
                            scrolled_text = ScrolledText(frame_log, state='disabled')
                            scrolled_text.configure(bg=Color_bg["scrolled_text"], fg=Color_fg["scrolled_text"],
                                                    font=font_list["scrolled_text"])
                            scrolled_text.grid(column=column_index, row=0, sticky="nsew")
                            # Makes it stretchy
                            frame_log.columnconfigure(column_index, weight=1)
                            frame_log.rowconfigure(column_index, weight=1)
                            return scrolled_text

                        device_dict[con_dev]["scrolled_text"] = create_scrolled_text()
                        column_index += 1

                # Filename label --------------------------------------------------------------------------------------

                filename_label = tk.Label(master=frame_entrys, bg=Color_bg["label"], fg=Color_fg["label"],
                                          font=font_list["label"],
                                          text="Filename: ")
                filename_entry_label = tk.Label(master=frame_entrys, bg=Color_bg["filename"], fg=Color_fg["filename"],
                                                font=font_list["filename"],
                                                text=self.filename_entry.get())

                # Recording_time label --------------------------------------------------------------------------------

                self.time_label_text.set('Recording time: 0.000' + " of ")
                time_entry_label = tk.Entry(master=frame_entrys, bg=Color_bg["entry"], fg=Color_fg["entry"],
                                            font=font_list["entry"])
                time_entry_label.insert(0, str(self.duration_entry.get()))
                recording_label = tk.Label(master=frame_entrys, bg=Color_bg["label"], fg=Color_fg["label"],
                                           font=font_list["label"], textvariable=self.time_label_text)
                time_format = tk.Label(master=frame_entrys, bg=Color_bg["label"], fg=Color_fg["label"],
                                       font=font_list["label"], text="in " + str(self.duration_options.get()))

                # Show Time Label -------------------------------------------------------------------------------------
                self.show_time_text.set("⌛ 0.000")
                show_time_label = tk.Label(master=frame_entrys, textvariable=self.show_time_text,
                                           bg=Color_bg["show_time"], fg=Color_fg["show_time"],
                                           font=font_list["show_time"])

                # Circle Progressbar Label ----------------------------------------------------------------------------
                x0, y0, x1, y1 = 0, 0, 150, 150
                # Create main Canvas
                canvas = tk.Canvas(master=frame_entrys, width=x1, height=y1, bg=Color_bg["bg"])

                # Create Impulse circle
                impluse_width = (x1 - x0) * (y1 - y0) / 2.5 / 1000  # To scale thicknes of outline
                impulse_obj = ImpulseClass(canvas, x0, y0, x1, y1, width=impluse_width)
                impulse_obj.start(int(self.rhythm_entry.get()))

                # Create progressCircle
                self.progressbar = CircleProgressbar(canvas, x0, y0, x1, y1, 20)
                self.progressbar.start(
                    float(self.duration_entry.get()))  # Has to be an Integer, duration_entry(main-gui)
                # After Starting Progressbar instantly pause it, becuase only the start_recording function should start it
                self.progressbar.toggle_pause()

                # Rhythm Label ----------------------------------------------------------------------------------------

                rhythm_label = tk.Label(master=frame_entrys, bg=Color_bg["label"], fg=Color_fg["label"],
                                        font=font_list["label"],
                                        text="Rhythm interval: ")

                sv = tk.StringVar()
                sv.trace("w", lambda name, index, mode, sv=sv: self.checkForEntryChanges(sv, impulse_obj))
                rhythm_entry = tk.Entry(master=frame_entrys, bg=Color_bg["entry"], fg=Color_fg["entry"],
                                        font=font_list["entry"], textvariable=sv)

                # Help Button -------------------------------------------------------------------------------------------------

                help_button = tk.Button(master=help_frame, text="❔",
                                        font=font_list["help_button"], bg=Color_bg["help_button"],
                                        fg=Color_fg["help_button"],
                                        command=lambda: self.helping_GUI_hori(help_frame, mult_value,
                                                                              height=int(height / 2), width=width))

                help_content_frame = tk.Frame(master=help_frame, bg=Color_bg["help_frame"])
                help_content = tk.Label(master=help_content_frame, bg=Color_bg["help_frame"],
                                        fg=Color_fg["help_button"], font=font_list["help_frame"],
                                        text="[Step1] Connect Devices and wait until they are shown up on the GUI\n"
                                             "[Step2] Connect Devices by clicking on the Button until it turns green\n"
                                             "[Step3] Choose a Mode for the Type of Device you connected\n"
                                             "[Step4] Close the GUI\n")

                # set Hover Event on every Label/Button -----------------------------------------------------------------------
                createToolTip(rhythm_label, text="Change the Rhythm of the Impulse")
                createToolTip(self.rhythm_entry, text="Change the Rhythm of the Impulse")
                createToolTip(recording_label, text="Change the time in seconds")
                createToolTip(self.duration_entry, text="Change the time in seconds")

                # Function that calls a thread which constantly updates the time --------------------------------------

                self.start_stop_button = tk.Button(master=frame_start, text="Start", state=tk.NORMAL,
                                                   bg=Color_bg["start_button_on"], fg=Color_fg["start_button_on"],
                                                   command=lambda: self.start_recording(recordingWindow, frame_save,
                                                                                        time_entry_label))

                # Set/pack Labels on Gui ------------------------------------------------------------------------------
                # Filename
                filename_label.grid(column=1, row=0, sticky="nw", pady=10, padx=10, ipadx=8, ipady=4)
                filename_entry_label.grid(column=2, row=0, sticky="nw", pady=10, padx=10, ipadx=8, ipady=4)
                # Rhythm
                rhythm_label.grid(column=1, row=1, sticky="nw", pady=10, padx=10, ipadx=8, ipady=4)
                rhythm_entry.grid(column=2, row=1, sticky="nw", pady=10, padx=10, ipadx=8, ipady=4)
                # rhythm_format.grid(column=2, row=1, sticky="nw", pady=10, padx=10, ipadx=8, ipady=4)
                # Recording
                recording_label.grid(column=1, row=2, sticky="nw", pady=10, padx=10, ipadx=8, ipady=4)
                time_entry_label.grid(column=2, row=2, sticky="ne", pady=10, padx=10, ipadx=8, ipady=4)
                time_format.grid(column=2, row=2, sticky="ne", pady=10, padx=10, ipadx=8, ipady=4)
                show_time_label.grid(column=3, row=3, rowspan=2, sticky="nsew", pady=10, padx=10)

                canvas.grid(column=3, row=0, rowspan=3, sticky="nsew", pady=10, padx=10)
                self.start_stop_button.grid(column=0, row=0, sticky="nsew", pady=10, padx=10)
                # Help Button
                help_button.grid(column=0, row=0, sticky="nesw")
                help_content_frame.grid(column=1, row=0, sticky="nesw")
                help_content.pack(side="top", padx=5, pady=5)


            else:
                error_msg = "Duration/Rhythm entry is not an int/float"
        else:
            error_msg = "Not all entrys were filled"

        if error_msg:
            messagebox.showerror("Error", error_msg)
            """
            error_recording_gui = tk.Toplevel(self.gui, bg="yellow")
            error_recording_gui.title("Error Messages")
            error_label = tk.Label(master=error_recording_gui, fg="red", text=error_msg, bg="yellow")
            error_label.pack(fill="none", expand=True, pady=30, padx=30)
            """

    def helping_GUI_verti(self, help_frame, mult_value, height=0, width=0):
        # for
        self.isHelp = not self.isHelp
        if self.isHelp:
            print("true")
            help_frame.place(y=0, x=width)  # Open
        else:
            help_frame.place(y=height * mult_value)  # Close

    def helping_GUI_hori(self, help_frame, mult_value, height=0, width=0):
        # for
        self.isHelp = not self.isHelp
        if self.isHelp:
            print("true")
            help_frame.place(y=height, x=0)  # Open
        else:
            print("False", width)
            help_frame.place(y=height, x=width * mult_value)  # Closen

    # on GUI closing --------------------------------------------------------------------------------------------------
    def on_closing_serial_gui(self, gui_to_close, thread):
        """
        Closing tab and thread, also changes the existance of all buttons to False

        Parameters
        ----------
        gui_to_close: which gui should be closed
        thread      : thread of this gui (serial)

        Returns
        -------

        """
        # Close Tab
        gui_to_close.destroy()
        # Set Baudrate
        global BAUDRATE
        BAUDRATE = self.baud_options.get()

        for port in allDevices:
            allDevices[port].baudrate = self.baud_options.get()
        # Stop thread
        if thread:
            thread.stop_thread()
        # Set button of serial_devices on not Exist  (False)
        for btn in btnDevices:
            btnDevices[btn]["Exist"] = False

    def on_closing_recording_gui(self, gui_to_close, thread_list):
        """
        Closing tab and thread, also changes the existance of all buttons to False

        Parameters
        ----------
        gui_to_close: which gui should be closed
        thread_list : threadlist with all threads to close (recording-Threads, update_label-thread)

        Returns
        -------

        """
        # Close Tab
        gui_to_close.destroy()
        # Stop thread
        if thread_list:
            for thread in thread_list:
                thread.stop_thread()

        # Reset Audio and circle_progressbar
        if RECORDING_MODE == "KWS":
            self.audio.terminate()
            self.audio = pyaudio.PyAudio()
        self.canvas = tk.Canvas
        self.progressbar = object

        # Set button of serial_devices on not Exist  (False)
        for btn in btnDevices:
            btnDevices[btn]["Exist"] = False

    def on_closing_gui_during_recording(self, ask_msg, gui_to_close, thread_list):
        """
        Closing tab and thread during a recording, also changes the existance of all buttons to False

        Parameters
        ----------
        gui_to_close: which gui should be closed
        thread_list : threadlist with all threads to close (recording-Threads, update_label-thread)

        Returns
        -------

        """
        close = False
        # If ask_msg True, the user will be asked whether he want to close the gui or not, otherwise the programm will auto-delete it
        if ask_msg:
            if messagebox.askokcancel("Quit", "Do you want to quit?"):
                close = True
        else:
            close = True
        if close:
            # Close Tab
            gui_to_close.destroy()
            # Stop thread
            for thread in thread_list:
                thread.stop_thread()
            # Unconnect BUtton
            # self.check_conDevices_plugged()
            self.unconnect_all_Buttons()
            # Reset Audio and circle_progressbar
            if RECORDING_MODE == "KWS":
                self.audio.terminate()
                self.audio = pyaudio.PyAudio()
            self.canvas = tk.Canvas
            self.progressbar = object

            # Reset recording_dict
            recording_dict.clear()

            # Reset time_passed
            self.time_passed = datetime.timedelta(seconds=0)

            # Reset Stop_recording
            global stop_recording
            stop_recording = False
            # Reverse recording_bool at the end
            global recording_bool
            recording_bool = False

    # Recording functions ---------------------------------------------------------------------------------------------
    def start_recording(self, recordingWindow, frame_save, time_entry_label):
        """
        This function is called after clicking on Start in Recording-gui

        Its starting all threads for reading every connected device and also one which updates Information-labels
        Parameters
        ----------
        recordingWindow:    gui-window of Recording
        frame_save:         frame where labels are getting updated during recording
        time_entry_label:   time_entry_label which has the time duration of one recording

        Returns
        -------

        """
        error_msg = None
        if check_If_Number(time_entry_label.get()):  # Check if entry is float/int
            if connected_devices:  # Check if at least one deivce is connected
                # Reverse recording_bool
                global recording_bool
                recording_bool = not recording_bool
                # check audio variable for KWS
                if not self.audio and RECORDING_MODE == "KWS":
                    self.audio = pyaudio.PyAudio

                if recording_bool:  # after reverse, if True start recording, otherwise stop recording

                    # Change label of Start_stop_button to "Stop"
                    self.start_stop_button.config(text="Stop", bg=Color_bg["stop_button_on"],
                                                  fg=Color_fg["stop_button_on"])
                    # Start Threads for every connected device
                    for devicename in allDevices.keys():
                        if devicename in connected_devices:

                            if RECORDING_MODE == "tof":
                                self.recording_thread_list.append(
                                    RecordThread(device=allDevices[devicename], devicename=devicename, interval=1))
                            elif RECORDING_MODE == "kws":
                                stream = self.audio.open(format=pyaudio.paInt16, channels=CHANNELS,
                                                         rate=RATE, input=True,
                                                         frames_per_buffer=CHUNK)
                                self.recording_thread_list.append(
                                    RecordThread(device=stream, devicename=devicename, interval=1))

                            elif RECORDING_MODE == "mva":
                                print('testtestest')
                                self.recording_thread_list.append(
                                    RecordThread(device=allDevices[devicename], devicename=devicename, interval=1))
                            else:
                                print("[RECORDING_MODE] '", RECORDING_MODE, "' is wrong, try: tof,kws")

                    # Add thread for label_update
                    tr = threading.Thread(target=self.update_label, args=(frame_save, time_entry_label, recordingWindow)
                                          , daemon=True)
                    tr.start()

                    # Start/Stop  ProgressCircle
                    self.progressbar.set_time(float(time_entry_label.get()))  # Update time entry
                    self.progressbar.toggle_pause()

                    # Setup on_close_window-event, which deletes all threads after closing window
                    recordingWindow.wm_protocol("WM_DELETE_WINDOW",
                                                lambda: self.on_closing_gui_during_recording(True, recordingWindow,
                                                                                             self.recording_thread_list))
                    print("threads created!")



                # if start/stop-Button got clicked again, end all Threads and save logs
                else:
                    global stop_recording
                    stop_recording = True
            else:
                error_msg = "No Device plugged in"
                self.on_closing_gui_during_recording(False, recordingWindow, self.recording_thread_list)

        else:
            error_msg = "Its not an integer/float"

        if error_msg:
            messagebox.showerror("Error", error_msg)
            """
            error_recording_gui = tk.Toplevel(self.gui, bg="yellow")
            error_recording_gui.title("Error Messages")
            error_label = tk.Label(master=error_recording_gui, fg="red", text=error_msg, bg="yellow")
            error_label.pack(fill="none", expand=True, pady=30, padx=30)
            """

    def display(self, record, device):
        """
        display recordings on Gui (scrolled_text)

        Parameters
        ----------
        record: Record Message
        device: decides on which scrolled_text it should be visualized in

        Returns
        -------

        """

        msg = "[{}] {}".format(device, record)

        device_dict[device]["scrolled_text"].configure(state='normal')
        device_dict[device]["scrolled_text"].insert(tk.END, msg + '\n')
        device_dict[device]["scrolled_text"].configure(state='disabled')
        device_dict[device]["scrolled_text"].yview(tk.END)

    def update_label(self, frame_save, time_entry_label, record_window):
        """
        This function is updating all Information-labels on the recording-gui

        Its called constantly within a thread.
        Parameters
        ----------
        frame_save :        frame where all Information_labels are placed
        time_entry_label:   time_entry_label which will be constanly changed
        record_windoxw:      recording_gui-Object

        Returns
        -------

        """
        start_time = time.time()
        max_time = datetime.timedelta(seconds=0)

        if self.duration_options.get() == "seconds":
            max_time = datetime.timedelta(seconds=float(time_entry_label.get()))
        elif self.duration_options.get() == "minutes":
            max_time = datetime.timedelta(minutes=float(time_entry_label.get()))

        # During recordings, the time_entry is disabled
        time_entry_label.config(state=tk.DISABLED)

        # Changes format to onlyshow a specific amount of digits
        def format_td(time):
            TotalDuration = str(time).split('.', 2)[0]
            return TotalDuration

        # As long as time_passed is below max_time AND stop_recording is FALSE
        # while self.time_passed <= max_time and not stop_recording:
        global stop_recording
        while self.time_passed <= max_time + datetime.timedelta(milliseconds=200) and not stop_recording:
            # Check for device changes
            didnt_change_bool = get_all_devices()

            # If devices didnt change during recording
            if not didnt_change_bool:
                formatted_time = format_td(self.time_passed)
                # Change Label ----------------------------------------------------------------
                self.time_label_text.set('Recording time: ' + str(formatted_time) + " of ")
                self.show_time_text.set("⌛ " + str(formatted_time))
                # Change Logtext --------------------------------------------------------------
                # Check if a new Log is in queue to display

                for device in device_dict.keys():

                    # Only Illiterate through currently content of Queue (not live)
                    for index_queue in range(0, device_dict[device]["log_queue"].qsize()):
                        try:
                            # record = self.log_queue.get(block=False)
                            record = device_dict[device]["log_queue"].get(block=False)
                        except queue.Empty:
                            pass
                        else:
                            if record:
                                self.display(record, device)

                global interval_recording
                if interval_recording:
                    time.sleep(interval_recording)

                # Update time_passed
                self.time_passed = datetime.timedelta(seconds=time.time() - start_time)

            # If device changed during recording
            else:
                messagebox.showerror("TEST Device_list Changed", "Devices got un/plugged during recording \n "
                                                                 "Recording_window will be closed after saving/discarding the recorded Data until now!")
                stop_recording = True

        time_entry_label.config(state=tk.NORMAL)
        self.delete_threads()

        # process all recordings
        self.edit_recordings(frame_save, record_window, time_entry_label)

    def delete_threads(self):
        """
        Deletes all Treads in recording_thread_list

        Returns
        -------

        """
        for thread in self.recording_thread_list:
            thread.stop_thread()

    # Check/Update - changes functions --------------------------------------------------------------------------------
    def check_conDevices_plugged(self):
        """
        Checks if all connected Devices are still plugged in

        Returns
        -------

        """
        ports = serial.tools.list_ports.comports()
        # Update dictionary with all_devices which are plugged in
        allDevices.clear()
        for port, desc, hwid in sorted(ports):
            try:
                ser = serial.Serial(
                    port=port,
                    baudrate=BAUDRATE,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    timeout=0)
                allDevices[port] = ser
            except:
                print("Error, cant open serial. Wait few seconds to recover test")
                time.sleep(1)
        # if connected_device not in all_devices -> delete it out of list
        for con_dev in connected_devices:
            # if connected_Serials are no longer plugged in,
            # delete it out of connected_devices
            if con_dev not in allDevices.keys():
                connected_devices.remove(con_dev)

    def unconnect_all_Buttons(self):
        """
        Unconnects every Button (resets its state)

        Returns
        -------

        """
        for serv_dev in btnDevices.keys():
            btnDevices[serv_dev]["Connected"] = False

            if serv_dev in connected_devices:
                connected_devices.remove(serv_dev)

    def checkForEntryChanges(self, sv, impulseObj):
        """
        This function checks the entry for correctness

        Its called through an event-listener (If entry is changing)

        Parameters
        ----------
        sv
        impulseObj

        Returns
        -------

        """
        try:
            sv_float = float(sv.get())  # Convert StringVar to int
            if sv_float > 0:
                impulseObj.set_impulse_time(sv_float)
                return sv.get()
        except:
            return "ERROR"

    # Save/Discard recorded Recordings --------------------------------------------------------------------------------
    def edit_recordings(self, frame_save, record_window, time_entry_label):
        """
        This function creates a Save and Discard button and makes start/stop-Button unclickable until one Option is chosen

        Parameters
        ----------
        frame_save:         frame where alle Information_labels are placed
        record_window:      recording_gui-Object
        time_entry_label:   time_entry_label:   time_entry_label which will be constanly changed

        Returns
        -------

        """
        # Reverse recording_bool at the end
        global recording_bool
        recording_bool = False

        # Pause circleprogressbar animation
        self.progressbar.toggle_pause()

        if recording_dict:
            # Create Buttons (save/discard) on recording_gui
            save_Button = tk.Button(master=frame_save, text="Save", state=tk.NORMAL, bg=Color_bg["start_button_on"],
                                    fg=Color_fg["start_button_on"],
                                    command=lambda: self.create_file_of_recordings(frame_save, record_window,
                                                                                   time_entry_label))
            discard_Button = tk.Button(master=frame_save, text="Discard", state=tk.NORMAL,
                                       bg=Color_bg["stop_button_on"], fg=Color_fg["stop_button_on"],
                                       command=lambda: self.delete_recordings(frame_save, record_window))
            save_Button.grid(column=0, row=1, sticky="nsew", pady=7, padx=15)
            discard_Button.grid(column=1, row=1, sticky="nsew", pady=7, padx=15)

            # Change State of start/stop-Button until save/discard has been clicked
            self.start_stop_button.config(state=tk.DISABLED, bg=Color_bg["start_button_off"],
                                          fg=Color_fg["start_button_off"])

        else:
            print("Error on saving recordings, recording_dict is empty !")
            self.delete_recordings(frame_save, record_window)

    def create_file_of_recordings(self, frame, record_window, time_entry_label):
        """
        Creates a Filename of saved recordings and formats it

        Parameters
        ----------
        frame:         frame where alle Information_labels are placed
        record_window:      recording_gui-Object
        time_entry_label:   time_entry_label:   time_entry_label which will be constanly changed

        Returns
        -------

        """

        path_to_save = "Error"
        for device in device_dict.keys():
            if RECORDING_MODE == "tof":
                # Create Filename
                filename = self.set_filename(".json", device)
                # Create Filepath
                path_to_save = os.path.join(self.path, filename)
                ut.create_Data_file(recording_dict[device], path_to_save)
            elif RECORDING_MODE == "kws":
                # Create Filename
                filename = self.set_filename(".wav", device)
                # Create Filepath
                path_to_save = os.path.join(self.path, filename)
                waveFile = wave.open(path_to_save, 'wb')
                waveFile.setnchannels(CHANNELS)
                waveFile.setsampwidth(self.audio.get_sample_size(FORMAT))
                waveFile.setframerate(RATE)
                waveFile.writeframes(b''.join(recording_dict[device]["audio"]))
                print("RECORDING WAV: ", recording_dict[device]["audio"])
                waveFile.close()
                ut.create_Data_file(recording_dict[device]["audio"], path_to_save)
            elif RECORDING_MODE == "mva":
                # Create Filename
                filename = self.set_filename(".json", device)
                # Create Filepath
                path_to_save = os.path.join(self.path, filename)
                print(recording_dict[device])
                ut.create_Data_file(recording_dict[device], path_to_save)

        # Reset -------------------------------------------------------------------------------------------------------
        self.start_stop_button.config(state=tk.NORMAL)
        self.delete_Content_of_Frame(frame)
        self.reset_recordings(record_window)
        # scrolled_text has to be state=normal to be edited/deleted
        for device in device_dict.keys():
            device_dict[device]["scrolled_text"].configure(state='normal')
            device_dict[device]["scrolled_text"].insert(tk.END, path_to_save)
            device_dict[device]["scrolled_text"].configure(state='disabled')
        # Reset recording_dict
        recording_dict.clear()

    def delete_recordings(self, frame, record_window):
        """
        On Button click on Discard

        Parameters
        ----------
        frame:              frame where alle Information_labels are placed
        record_window:      recording_gui-Object

        Returns
        -------

        """
        # Reset
        self.start_stop_button.config(state=tk.NORMAL)
        print("Reset CONTENT of Frame")
        self.delete_Content_of_Frame(frame)
        print("Reset RECORDINGS")
        self.reset_recordings(record_window)

    # --

    def reset_recordings(self, record_window):
        """
        This function resets everything, so a new recording can start clean from scratch

        Parameters
        ----------
        record_window: Recording_gui Object

        Returns
        -------

        """

        # CHECK if devices still are connected
        if len(recording_dict.keys()) == len(connected_devices):

            # Reset time_passed
            self.time_passed = datetime.timedelta(seconds=0)
            self.time_label_text.set("Recording time: 0.000 of ")
            self.show_time_text.set("0.000")
            # Reset start_stop_button to "Start"
            self.start_stop_button.config(text="Start", bg=Color_bg["start_button_on"], fg=Color_fg["start_button_on"])
            # Clear scrolledtext
            for device in device_dict.keys():
                # scrolled_text has to be state=normal to be edited/deleted
                device_dict[device]["scrolled_text"].configure(state='normal')
                device_dict[device]["scrolled_text"].delete("1.0", tk.END)
                device_dict[device]["scrolled_text"].configure(state='disabled')

            # Reset Progressbar canvas
            """
            self.canvas.delete("all")
            del self.progressbar
            self.progressbar = CircularProgressbar(self.canvas, 0, 0, 200, 200, 20)
            self.progressbar.start(float(time_entry_label.get()),
                                   float(self.rhythm_entry.get()))  # Has to be an Integer
            # After Starting Progressbar instantly pause it, becuase only the start_recording function should start it
            self.progressbar.toggle_pause()
            """
            self.progressbar.reset_cur_extent()

            # Reset Stop_recording
            global stop_recording
            stop_recording = False
            # Reverse recording_bool at the end
            global recording_bool
            recording_bool = False

        else:
            messagebox.showerror("Device unplugged", "Devices got un/plugged during recording \n"
                                                     "Recording_window will be closed after saving/discarding the recorded Data until now!")

            self.on_closing_gui_during_recording(False, record_window, self.recording_thread_list)

    # Further Functions -----------------------------------------------------------------------------------------------

    def set_filename(self, format, device):
        """
        Creates an unique Filename with the correct format given as an Argument

        Parameters
        ----------
        format:     Format of the ending of this filename
        device:     Device of Recording

        Returns
        -------
        filename:   Final Filename

        """
        filename = None
        if str(self.filename_idtype_options.get()) == "date":
            timestr = time.strftime("%Y%m%d-%H%M%S")
            filename = device + "_" + str(self.filename_entry.get()) + "_" + timestr + format

        elif str(self.filename_idtype_options.get()) == "numbers":
            # Search for amount of files with this name in Folder and create this name with amount
            log_list = os.listdir(path)
            # filename = log_list[0], so the first loop of while is True
            if log_list:
                filename = log_list[0]
                index = 0
                while filename in log_list:
                    print("Here: ", filename)
                    print("Here2: ", filename in log_list)
                    filename = device + "_" + str(self.filename_entry.get()) + "_" + str(index) + format
                    index += 1
                    print("Here3: ", filename)
            else:
                filename = device + "_" + str(self.filename_entry.get()) + "_" + "0" + format
        return filename

    def delete_Content_of_Frame(self, frame):
        """
        Deletes every Content of a Frame

        Parameters
        ----------
        frame:      Frame-object

        Returns
        -------

        """
        for widget in frame.winfo_children():
            widget.destroy()


# GUI-update-functions (Threads) ======================================================================================
def update_main_GUI(**kwargs):
    """
    Updates connected_device_list and all plugged devices

    This function is constantly called by one thread, which works in the background until its stopped
    Parameters
    ----------
    kwargs:     list of Key:Value - Arguments

    Returns
    -------

    """

    # If any other tab is open, make this GUI DISABLED ----------------------------------------------------------------
    gui = None
    if "gui" in kwargs.keys():
        gui = kwargs["gui"]

    # Check if root-gui has toplevel children
    has_toplevel_bool = False
    for child in gui.children.keys():
        if "!toplevel" in str(child):
            has_toplevel_bool = True
            break
    # If root-gui has toplevel-children, "close" (invisible) root-gui
    if has_toplevel_bool and gui.state() != "withdrawn":
        gui.state("withdrawn")
    # "open" root-gui
    elif not has_toplevel_bool and gui.state() != "normal":
        gui.state("normal")

    # Only update if no recording is made in the background (at the same time)
    if not recording_bool:
        # Update all plugged Devices (serials) ------------------------------------------------------------------------
        get_all_devices()

        if "serial_label" in kwargs.keys():
            # Update all connected devices
            for con_dev in connected_devices:
                # if connected_Serials are no longer plugged in,
                # delete it out of connected_devices
                if con_dev not in allDevices.keys():
                    connected_devices.remove(con_dev)
                    if con_dev in btnDevices.keys():
                        btnDevices[con_dev]["Connected"] = False

            # Update serial_Label on GUI
            label = kwargs["serial_label"]
            if connected_devices:
                label.config(fg="green", text='Connected serials: ' + ','.join(connected_devices))

            else:
                label.config(fg="red", text="No Devices are connected")

        # If at least one Device ist connected ------------------------------------------------------------------------
        if "open_Button" in kwargs.keys():
            open_Button = kwargs["open_Button"]

            # Fun mode with Button --------------------------------------------
            if fun_mode:
                random_value_x = random.randint(0, gui.winfo_width())
                random_value_y = random.randint(0, 100)

                r = lambda: random.randint(0, 255)
                random_hex = '#%02X%02X%02X' % (r(), r(), r())

                open_Button.config(bg=random_hex)
                open_Button.place(x=random_value_x, y=random_value_y)
            # -------------------------------------------------------------------

            if connected_devices:
                open_Button.config(state=tk.NORMAL, bg=Color_bg["open_button_on"], fg=Color_fg["open_button_on"])
            else:
                open_Button.config(state=tk.DISABLED, bg=Color_bg["open_button_off"], fg=Color_fg["open_button_off"])

    if "interval" in kwargs:
        interval = int(kwargs["interval"])

        time.sleep(interval)


def update_serial_GUI(**kwargs):
    """
    updates the serial list.

    this function is looped in a background Thread
    Parameters
    ----------
    kwargs:     list of Key:Value - Arguments

    Returns
    -------

    """

    # Set Gui
    gui = None
    if "gui" in kwargs:
        gui = kwargs["gui"]
    # Update Label
    if "label" in kwargs.keys():
        label = kwargs["label"]
        label.config(text='List of all serials: ' + ','.join(allDevices.keys()))

    # Create/Update Buttons to connect serials
    def set_connection(serv_dev):

        btnDevices[serv_dev]["Connected"] = not btnDevices[serv_dev]["Connected"]
        # Change Color of Button (True=Green, False=Red)
        if btnDevices[serv_dev]["Connected"]:
            btnDevices[serv_dev]["Object"].config(bg=Color_bg["start_button_on"], fg=Color_fg["start_button_on"])
            # Add
            connected_devices.append(serv_dev)
        else:
            btnDevices[serv_dev]["Object"].config(bg=Color_bg["stop_button_on"], fg=Color_fg["stop_button_on"])
            connected_devices.remove(serv_dev)

    # Delete Buttons of unplugged Devices and add Buttons to recently plugged Devices
    try:

        deletebtn = list()  # list of all button which should be deleted after the loop
        for btn in btnDevices.keys():
            # if a plugged Device exist to the matching Button
            if btn in allDevices.keys():
                # if Button not exist on GUI, create Button
                if not btnDevices[btn]["Exist"]:
                    # If Device is connected green, if not red
                    btnDevices[btn]["Object"].pack_forget()
                    if btnDevices[btn]["Connected"]:
                        btnDevices[btn]["Object"] = tk.Button(gui, text=btn, bg=Color_bg["green"],
                                                              command=lambda s=btn: set_connection(s))
                        createToolTip(btnDevices[btn]["Object"], text="Click on this Button to\n"
                                                                      "Connect/Unconnect")
                    else:
                        btnDevices[btn]["Object"] = tk.Button(gui, text=btn, bg=Color_bg["red"],
                                                              command=lambda s=btn: set_connection(s))
                        createToolTip(btnDevices[btn]["Object"], text="Click on this Button to\n"
                                                                      "Connect/Unconnect")

                    btnDevices[btn]["Object"].pack()
                    # Set Exist to True, after button was created on GUI
                    btnDevices[btn]["Exist"] = True

            # Delete Button of unexisting/unplugged device
            else:
                deletebtn.append(btn)

        # Delete Button of unexisting/unplugged device
        for del_btn in deletebtn:
            btnDevices[del_btn]["Object"].pack_forget()
            btnDevices.pop(del_btn)
            if del_btn in connected_devices:
                connected_devices.remove(del_btn)

        # Add Buttons
        for ser_dev in allDevices.keys():
            if ser_dev not in btnDevices.keys():
                # create Default btn_dict
                btnObj = dict()
                btnObj["Object"] = None  # Object Value
                btnObj["Connected"] = False  # isConnected boolean
                btnObj["Exist"] = True  # exist on GUI boolean

                # Add Button to button_dicitionary and create this button on GUI
                btnDevices[ser_dev] = btnObj
                btnDevices[ser_dev]["Object"] = tk.Button(gui, text=ser_dev, bg="red",
                                                          command=lambda s=ser_dev: set_connection(s))
                createToolTip(btnDevices[ser_dev]["Object"], text="Click on this Button to\n"
                                                                  "Connect/Unconnect")
                btnDevices[ser_dev]["Object"].pack()

    except:
        messagebox.showerror("Device Error", "Device got unplugged during Iteration \n"
                                             "program is still running")

    # Wait if interval is set
    if "interval" in kwargs.keys():
        interval = int(kwargs["interval"])
        time.sleep(interval)


def createToolTip(widget, text):
    """
    Creates a Tooltip when hovering over an widget (object)

    Parameters
    ----------
    widget:     Object which triggers the tooltip on hovering it
    text:       Text which will be shown after hovering over the widget

    Returns
    -------

    """
    toolTip = ToolTip(widget)

    def enter(event):
        toolTip.showtip(text)

    def leave(event):
        toolTip.hidetip()

    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)


def get_all_devices():
    """
    updates all plugged devices

    Returns
    -------
    bool True = device_list changed (unplugging/plugging-devices), False = Nothing changed
    """

    # Check all devices
    ports = serial.tools.list_ports.comports()

    # Update allDevices only if not recording
    if not recording_bool:
        # Print Information
        print("Amount of plugged in devices: ", len(ports),
              " | currently in all_Devices: ", allDevices.keys(),
              " | currently connected_Devices: ", connected_devices,
              " BAUDRATE: ", BAUDRATE)

        if len(ports) != len(allDevices.keys()):

            allDevices.clear()
            for port, desc, hwid in sorted(ports):
                try:
                    ser = serial.Serial(
                        port=port,
                        baudrate=BAUDRATE,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        bytesize=serial.EIGHTBITS,
                        timeout=0)
                    allDevices[port] = ser
                except:
                    print("Error, cant open serial. Wait few seconds to recover")
                    time.sleep(1)

            return False
        else:
            return True
    else:
        if len(ports) != len(allDevices.keys()):
            return True


def check_If_Number(value):
    """
    Checks if value is a number and not 0

    Parameters
    ----------
    value:      Value to check

    Returns
    -------
    boolean:    True/False
    """
    try:
        float(value)
        if float(value) != 0:
            return True
        else:
            return False
    except:
        return False


# Visualization Classes ===============================================================================================
class ToolTip(object):
    """
    Tooltip class, creates a Tooltip on hovering over an Object

    """

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() + 27
        self.tipwindow = tw = tk.Toplevel(self.widget)
        font_tip = tkFont.Font(family="Lucida Grande", size=10)

        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))

        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                         bg=Color_bg["tooltip"], fg=Color_fg["tooltip"], relief=tk.SOLID, borderwidth=2,
                         font=font_tip)
        label.pack(ipadx=5, ipady=5)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()


class ImpulseClass(object):
    """
    Class which creates an animated Impulse-Circle with canvas
    """

    def __init__(self, canvas, x0, y0, x1, y1, width):

        self.canvas = canvas
        self.x0, self.y0, self.x1, self.y1 = x0 + width, y0 + width, x1 - width, y1 - width
        self.width = width

        self.impulse_time = 40
        self.interval = 100

        self.impulse_id = self.canvas.create_oval(self.x0, self.y0, self.x1, self.y1)
        self.angel_degree = 0
        self.impulse_strength = 30  # Strength how much it will decrease/increase
        # draw static bar outline
        """
        w2 = width / 2
        self.oval_id1 = self.canvas.create_oval(self.x0-w2, self.y0-w2,
                                                self.x1+w2, self.y1+w2)
        self.oval_id2 = self.canvas.create_oval(self.x0+w2, self.y0+w2,
                                                self.x1-w2, self.y1-w2)
                                                """
        self.running = False

    def start(self, impulse_time, interval=30):
        self.interval = interval  # Milliseconds
        self.extent = 0

        self.impulse_inc = 180 / self.interval  # 90 Degree cosinus = 0 beacuse from size big to small (1 to 0)
        self.impulse_time = int((impulse_time * 1000) / self.interval)  # Seconds to Milliseconds devided by interval

        self.angel_degree = 0  # This is the current angel, Its used for resizing the Impulsecircle

        self.canvas.after(0, self.step_impulse, self.impulse_inc, time.time())

    def step_impulse(self, increment, time_lastrun):
        # Impulse position_values
        x0_impulse = (self.x0 + 1.5 * self.impulse_strength) - (abs(math.cos(np.radians(
            self.angel_degree))) * self.impulse_strength / 2)  # x0+1 so we start at min_size and make it bigger until x0. - abs(..) because x0 should move in negative direction
        y0_impulse = (self.y0 + 1.5 * self.impulse_strength) - (
                abs(math.cos(np.radians(self.angel_degree))) * self.impulse_strength / 2)
        x1_impulse = (self.x1 - 1.5 * self.impulse_strength) + (
                abs(math.cos(np.radians(self.angel_degree))) * self.impulse_strength / 2)
        y1_impulse = (self.y1 - 1.5 * self.impulse_strength) + (
                abs(math.cos(np.radians(self.angel_degree))) * self.impulse_strength / 2)
        color = "red"
        width = self.width
        if abs(math.cos(np.radians(self.angel_degree))) > 0.9:
            color = "green"
            width = width + 5
        else:
            color = "red"
            width = self.width

        self.canvas.coords(self.impulse_id, x0_impulse, y0_impulse, x1_impulse, y1_impulse)
        self.canvas.itemconfig(self.impulse_id, width=width, outline=color)

        self.angel_degree = self.angel_degree + increment  # Increase Angel with impulse_increment

        time_thisrun = time.time()
        time_dif = time_lastrun - time_thisrun

        # Add the diffrence of the run before and timevalue to timevalue
        # Example (timevalue = 0.09, time_test = 0.093 -> dif = -0.03 --> 0.09 + -0.003 => 0.087)
        new_time_value = int(self.impulse_time + (self.impulse_time + (time_dif * 1000)))

        self.canvas.after(new_time_value, self.step_impulse, increment, time_thisrun)

    def set_impulse_time(self, value):

        self.impulse_time = int((value * 1000) / self.interval)
        print(value, " = ", self.impulse_time)


class CircleProgressbar(object):
    """
    A Class which creates an animation of the progress of the currently running Recording
    """

    def __init__(self, canvas, x0, y0, x1, y1, width=2, start_ang=0, full_extent=360):
        self.cur_extent = 0.0
        self.custom_font = tkFont.Font(family="Helvetica", size=12, weight='bold')
        self.canvas = canvas
        self.x0, self.y0, self.x1, self.y1 = x0 + width, y0 + width, x1 - width, y1 - width
        self.tx, self.ty = (x1 - x0) / 2, (y1 - y0) / 2
        self.width = width
        self.start_ang, self.full_extent = start_ang, full_extent

        self.timevalue = 0
        self.interval = 100
        # draw static bar outline
        """
        w2 = width / 2
        self.oval_id1 = self.canvas.create_oval(self.x0-w2, self.y0-w2,
                                                self.x1+w2, self.y1+w2)
        self.oval_id2 = self.canvas.create_oval(self.x0+w2, self.y0+w2,
                                                self.x1-w2, self.y1-w2)
                                                """
        self.running = False

    def start(self, timevalue, interval=100):
        self.interval = interval  # Milliseconds
        self.timevalue = int((timevalue * 1000) / self.interval)  # Seconds to Milliseconds devided by interval
        self.increment = self.full_extent / self.interval
        self.extent = 0

        self.arc_id = self.canvas.create_arc(self.x0, self.y0, self.x1, self.y1,
                                             start=self.start_ang, extent=self.extent,
                                             width=self.width, style='arc')

        percent = '0%'
        self.label_id = self.canvas.create_text(self.tx, self.ty, text=percent,
                                                font=self.custom_font)
        self.running = True

        self.canvas.after(0, self.step_circle, self.increment, time.time())

    def step_circle(self, delta, time_lastrun):
        """Increment extent and update arc and label displaying how much completed."""

        if self.running:
            self.extent = (self.extent + delta)  # %360
            self.cur_extent = (self.extent + delta)  # % 360
            if self.cur_extent < 360:
                self.canvas.itemconfigure(self.arc_id, extent=self.cur_extent)
                percent = '{:.0f}%'.format(round(float(self.cur_extent) / self.full_extent * 100))
                self.canvas.itemconfigure(self.label_id, text=percent)
            elif self.cur_extent > 360 and self.cur_extent < 362:
                self.canvas.itemconfigure(self.arc_id, extent=359)
                percent = '{:.0f}%'.format(round(float(self.cur_extent) / self.full_extent * 100))
                self.canvas.itemconfigure(self.label_id, text=percent)

        # print("Time: ", time.time() - time_lastrun)
        time_thisrun = time.time()
        # Add the diffrence of the run before and timevalue to timevalue
        # Example (timevalue = 0.09, time_test = 0.093 -> dif = -0.03 --> 0.09 + -0.003 => 0.087)
        new_time_value = self.timevalue + (self.timevalue - (time.time() - time_lastrun) * 1000)
        self.after_id_circle = self.canvas.after(int(new_time_value), self.step_circle, delta, time_thisrun)

    def toggle_pause(self):
        self.running = not self.running

    def reset_cur_extent(self):
        self.cur_extent = 0.0
        self.extent = 0
        self.canvas.delete(self.arc_id)
        self.canvas.delete(self.label_id)
        self.arc_id = self.canvas.create_arc(self.x0, self.y0, self.x1, self.y1,
                                             start=self.start_ang, extent=self.extent,
                                             width=self.width, style='arc')
        percent = '0%'
        self.label_id = self.canvas.create_text(self.tx, self.ty, text=percent,
                                                font=self.custom_font)

    def set_time(self, value):
        self.timevalue = int((value * 1000) / self.interval)  # Seconds to Milliseconds devided by interval


# a subclass of Canvas for dealing with resizing of windows
class ResizingCanvas(tk.Canvas):
    """
    On resizing the canvas, all object should also resize with it
    """

    def __init__(self, parent, **kwargs):

        tk.Canvas.__init__(self, parent, **kwargs)
        self.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        width = self.winfo_width()
        height = self.winfo_height()
        x0, y0, x1, y1 = self.coords('all')
        xratio = float(width) / x1
        yratio = float(height) / y1

        if xratio < yratio:
            self.scale_objects(xratio)
        else:
            self.scale_objects(yratio)

    def scale_objects(self, scale):
        self.scale('all', 0, 0, scale, scale)


# Threads =============================================================================================================
class RecordThread(object):
    """
    This Record-class (Used for Threads) records one device for a specific time and saves it in a global Variable
    """

    def __init__(self, device, devicename, interval):
        super().__init__()
        self.device = device  # Stream (KWS) or serial (tof)
        self.interval = interval
        self.devicename = devicename

        self.line = ''
        self.logfile = dict()
        self.running = True

        self.timeindex = 0  # To count time

        self.initialize_variable()

        self.thread = threading.Thread(target=self.run, args=())
        self.thread.daemon = True
        self.thread.start()

    def run(self):
        # reset serial_buffer
        if RECORDING_MODE != "kws":
            self.device.reset_input_buffer()
        self.timeindex = 0
        while self.running:
            if RECORDING_MODE == "tof":
                self.record_serials_tof()
            elif RECORDING_MODE == "kws":
                self.record_serials_kws()
            elif RECORDING_MODE == "mva":
                self.record_serials_mva()

    def initialize_variable(self):
        if RECORDING_MODE == "tof":
            pass
        elif RECORDING_MODE == "kws":
            pass
        elif RECORDING_MODE == "mva":
            self.complete_dict = dict()
            self.data_dict = dict()
            self.axe_list = ["x", "y", "z"]
            self.count = 0

    def join_thread(self):
        self.thread.join()

    def is_alive(self):
        return self.thread.is_alive()

    def stop_thread(self):
        recording_dict[self.devicename] = self.logfile
        print("HIER", self.logfile)
        if RECORDING_MODE == "kws":
            self.device.stop_stream()

        self.running = False

    def add_to_queue(self, record):
        # logger.log(logging.INFO, record)
        device_dict[self.devicename]["log_queue"].put(record)

    # Filter Functions ----------------------------------------
    # TODO: all function here should be placed in ther record_functions not outside of it
    def add_MVA_logfile(self, final_resul):
        try:
            # Now use the second part of split_list ("/r/n") and check if its a complete line (3 cuts)

            if len(final_resul) == 3:
                result_float = list(map(float, final_resul))
                final_resul = [round(i * 0.244, 3) for i in result_float]

                timestamp = round(self.timeindex * (1 / SAMPLERATE), 3)

                self.logfile[timestamp] = final_resul
                self.add_to_queue(
                    "[{timestamp}] {result}".format(timestamp=str(timestamp), result=str(final_resul)))
                self.timeindex += 1
                """
                if timestamp not in self.logfile:
                    self.logfile[timestamp] = []
                self.logfile[timestamp].append(final_result)
                self.add_to_queue("[{timestamp}] {result}".format(timestamp=str(timestamp), result=str(final_result)))
                self.timeindex += 1
                """
        except:
            pass

    def add_MVA_logfile_DV(self, result):
        try:

            self.logfile[self.timeindex] = result

            self.add_to_queue(
                "[{timestamp}] {result}".format(timestamp=str(self.timeindex), result=str(result)))
            self.timeindex += 1
        except:
            pass

    # Recording Functions -------------------------------------
    def record_serials_mva(self):
        """

        :param task: string: unique taskname
        :param user: string: name of user doing the tasks
        :return:
        """

        # try to read. if not possible, stop recording
        lineIn = None
        try:
            lineIn = self.device.readline()
        except:
            print("Cant read Serial: ", self.device, " ... Stop Recording")
            self.add_to_queue("Cant read Serial: {} ... Stop Recording".format(self.device))
            global stop_recording
            stop_recording = True
            # sleep 1 second so we can give the looping function some more time
            time.sleep(self.interval)

        def check_MVA_has_n(final_result_split):
            # Check if \n is included if so get everything only after that
            # Error Correction: If "\n" is in line, only split data afterwards
            if "\n" in final_result_split:
                final_result_index = final_result_split.index("\n")
                final_result_cut = final_result_split[final_result_index + 2:]
                final_result = final_result_cut.split(",")
            else:
                final_result = final_result_split.split(",")

            # print(repr("{} Test {}".format(self.line, final_result)))
            # print(len(final_result))
            return final_result

        try:
            if lineIn != b'':
                # If line is not complete
                if not lineIn.endswith(b'\r\n'):
                    # self.add_to_queue(lineIn)
                    self.line += lineIn.decode('utf-8')
                else:
                    self.line += lineIn.decode('utf-8')
                    # if "START\r\n" is not in self.line
                    if "\r\n" in self.line and "START" not in self.line:
                        # final_result = self.line.replace('\r\n', '').split(', ')
                        # If parts of 2 lines were send as one line, split them
                        final_result_split_list = self.line.split('\r\n')
                        final_result_split_part1 = final_result_split_list[0]
                        final_result = check_MVA_has_n(final_result_split_part1)
                        self.add_MVA_logfile(final_result)

                        final_result_split_part2 = final_result_split_list[1]
                        final_result = check_MVA_has_n(final_result_split_part2)
                        self.add_MVA_logfile(final_result)

                    self.line = ''
        except:
            print("[Record Error] Couldnt readline: ", lineIn)

    def record_serials_mva_double(self):
        """

        :param task: string: unique taskname
        :param user: string: name of user doing the tasks
        :return:
        """
        line = self.device.readline()
        if line != b'':

            # Check if line is 27 bytes long
            print(len(line))
            if len(line) == 27:

                # Get all Sensor-data (x,y,z for each sensor) and decode it
                data_sensor = line[5:17]
                list_data_sensor = list()
                for l in range(0, len(data_sensor), 2):
                    list_data_sensor.append(data_sensor[l] + data_sensor[l + 1] * 256)

                axe_dict = dict()
                for value in range(0, len(list_data_sensor)):

                    axe_dict[self.axe_list[value % len(self.axe_list)]] = list_data_sensor[value % len(self.axe_list)]
                    if len(axe_dict.keys()) == len(self.axe_list):
                        sensor_name = "{}{}".format("sensor", int(value / len(self.axe_list)))
                        copy_dict = copy.deepcopy(axe_dict)
                        self.complete_dict[sensor_name] = copy_dict
                        axe_dict.clear()

                # Get Motorrunning-status (0=False or 1=True)
                motor_value_list = [line[18], line[19]]
                for motor_value in range(0, len(motor_value_list)):
                    motor_name = "{}{}".format("motor", motor_value)
                    self.complete_dict[motor_name] = motor_value_list[motor_value]

                # Get Current-data
                data_current = line[17:21]
                list_data_current = list()
                for c in range(0, len(data_current), 2):
                    list_data_current.append(data_sensor[c] + data_sensor[c + 1] * 256)

                for current_value in range(0, len(list_data_current)):
                    current_name = "{}{}".format("current", current_value)
                    self.complete_dict[current_name] = list_data_current[current_value]

                """
                # Get Counter-value
                # counter_value = line[-4] + line[-3] * 256
                # counter_value = self.count
                #self.complete_dict["counter"] = counter_value


                # Save Data
                self.data_dict["Counter"] = counter_value
                temp_dict = copy.deepcopy(self.data_dict)
                self.complete_dict[self.count] = temp_dict

                print(line)
                print("Motor_value: {}{}, Counter: {}".format(motor_value[0], motor_value[1], counter_value))
                self.data_dict.clear()

                self.count += 1
                self.add_MVA_logfile(self.complete_dict)
                """

                print(line)
                print("Motor_value: {}{}, Counter: {}".format(motor_value_list[0], motor_value_list[1], self.timeindex))

                self.add_MVA_logfile(self.complete_dict)

        # ut.create_Data_file_and_path(cself.omplete_dict, r"C:\Users\Praktikant Software\Desktop\Create Data\test.json")

    def record_serials_tof(self):
        """


        :param task: string: unique taskname
        :param user: string: name of user doing the tasks
        :return:
        """
        # try to read. if not possible, stop recording
        try:

            lineIn = self.device.readline()
            self.add_to_queue(lineIn)

            if lineIn != b'':
                if not lineIn.endswith(b'\n'):
                    # self.add_to_queue(lineIn)
                    self.line += lineIn.decode('utf-8')
                else:
                    self.line += lineIn.decode('utf-8')
                    if "\n" in self.line:
                        splits = self.line.replace('\n', '').split(', ')
                        # print(splits)
                        if len(splits) == 4:
                            if splits[0] not in self.logfile:
                                self.logfile[splits[0]] = []
                            self.logfile[splits[0]].append(
                                splits[1:4])
                    self.line = ''
        except:
            print("Cant read Serial: ", self.device, " ... Stop Recording")
            global stop_recording
            stop_recording = True
            # sleep 1 second so we can give the looping function some more time
            time.sleep(self.interval)

    def record_serials_kws(self):

        data = self.device.read(CHUNK)
        if "audio" not in self.logfile:
            self.logfile["audio"] = []
        self.logfile["audio"].append(data)
        self.add_to_queue(data)

    # ---------------------------------------------------------


class updateThread:
    """
    This Class is creating a thread which constantly calls a specific function given as an Argument
    """

    def __init__(self, function, **kwargs):
        super().__init__()
        self.kwargs = kwargs
        self.function = function
        self.running = True

        p = threading.Thread(target=self.run, args=())
        p.daemon = True
        p.start()

    def run(self):
        while self.running:
            self.function(**self.kwargs)

    def stop_thread(self):
        self.running = False


# -------------------------------


class MDLabel(tk.Frame):

    def __init__(self, parent=None, **options):
        tk.Frame.__init__(self, parent, bg=options["sc"])  # sc = shadow color
        self.label = tk.Label(self, text=options["text"], padx=15, pady=10)
        self.label.pack(expand=1, fill="both", padx=(0, options["si"]), pady=(0, options["si"]))  # shadow intensity


class recording_multi:

    def __init__(self):
        self.gui = tk.Tk()

        # Recording
        # self.recording_thread_list = list()
        self.recording_process_list = list()
        self.time_label_text = tk.StringVar()
        self.time_label_text.set("")
        self.time_passed = 0.0
        self.start_stop_button = tk.Button
        self.running = False
        self.time_entry_label = None
        self.recording_window = None

        # Logging
        # self.device_dict = dict()

        # Entry
        self.duration_time_options = None
        self.duration_entry = None
        self.filename_idtype_options = None
        self.filename_entry = None

        self.main_GUI()

    # Start function --------------------------------------------------------------------------------------------------
    def main_GUI(self):
        # Init GUI #
        self.gui.title("Recording GUI")
        ws = self.gui.winfo_screenwidth()  # width of the screen
        hs = self.gui.winfo_screenheight()  # height of the screen
        w = 500  # width for the Tk root
        h = 500  # height for the Tk root
        x = int((ws / 2) - (w / 2))
        y = int((hs / 2) - (h / 2))
        self.gui.geometry("{}x{}+{}+{}".format(w, h, x, y))
        exitButton = tk.Button(self.gui, width=10, text="Exit", command=self.gui.destroy)

        # Create Frames -----------------------------------------------------------------------------------------------
        frame_serialize = tk.Frame(master=self.gui, bg='#FFCFC9')
        frame_serialize.pack(side="top")

        frame_duration = tk.Frame(master=self.gui, bg='#FFCFC9')
        frame_duration.pack(side="top")

        frame_filename = tk.Frame(master=self.gui, bg='#FFCFC9')
        frame_filename.pack(side="top")

        frame_start = tk.Frame(master=self.gui, bg='#FFCFC9')
        frame_start.pack(side="top")

        # Start Button ------------------------------------------------------------------------------------------------

        start_Button = tk.Button(master=frame_start, text="Start", state=tk.DISABLED,
                                 command=lambda: self.recording_GUI())

        # Serialize --------------------------------------------------------------------------------------------------

        # serial Connection List
        serialConnectionButton = tk.Button(master=frame_serialize, text="Serial Connection Setup",
                                           command=lambda: self.serial_GUI())
        # Connected serials Label_list
        connected_serial_label = tk.Label(master=frame_serialize, fg="red",
                                          text='Connected serials: ' + ','.join(connected_devices))

        # Duration Label ----------------------------------------------------------------------------------------------

        duration_label_before = tk.Label(master=frame_duration, text="Duration")
        duration_label_after = tk.Label(master=frame_duration, text="in")
        self.duration_entry = tk.Entry(master=frame_duration)

        duration_time_list = ["seconds", "minutes"]  # List of all Options
        self.duration_time_options = tk.StringVar(master=frame_duration)  # SringVar
        self.duration_time_options.set(duration_time_list[0])  # Default
        duration_dropdown = tk.OptionMenu(frame_duration, self.duration_time_options,
                                          *duration_time_list)  # DropMenu Object

        # Filename label ----------------------------------------------------------------------------------------------

        filename_label = tk.Label(master=frame_filename, text="Filename")
        self.filename_entry = tk.Entry(master=frame_filename)

        filename_idtype_list = ["date", "numbers"]  # List of all Options
        self.filename_idtype_options = tk.StringVar(master=frame_filename)  # SringVar
        self.filename_idtype_options.set(filename_idtype_list[0])  # Default
        filename_idtype_dropdown = tk.OptionMenu(frame_filename, self.filename_idtype_options,
                                                 *filename_idtype_list)  # DropMenu Object

        # Place Labels ------------------------------------------------------------------------------------------------

        # Place labels in Frame
        # Start Button
        start_Button.pack()
        # serialize
        serialConnectionButton.pack(side="left")
        connected_serial_label.pack(side="left")
        # Duration
        duration_label_before.pack(side="left")
        self.duration_entry.pack(side="left")
        duration_label_after.pack(side="left")
        duration_dropdown.pack(side="left")
        # Filename
        filename_label.pack(side="left")
        self.filename_entry.pack(side="left")
        filename_idtype_dropdown.pack(side="left")

        # Start Thread ------------------------------------------------------------------------------------------------
        tr_con = updateThread(update_main_GUI,
                              interval=interval_update_gui,
                              gui=self.gui,
                              serial_label=connected_serial_label,
                              start_Button=start_Button
                              )

        exitButton.place(relx=1.0, rely=1.0, anchor="se")
        self.gui.mainloop()

    # GUI's -----------------------------------------------------------------------------------------------------------
    def serial_GUI(self):
        """
        The GUI where devices (serials) can be connected/disconnected
        """
        serialConnectionWindow = tk.Toplevel(self.gui)
        serialConnectionWindow.title("Serial Connection")
        serialConnectionWindow.geometry("{}x{}".format(500, 250))

        serial_list_label = tk.Label(serialConnectionWindow, text='List of all serials: ' + ','.join(allDevices.keys()))
        serial_list_label.pack(side="top", padx='5', pady='10')

        tr = updateThread(update_serial_GUI,
                          interval=1,
                          gui=serialConnectionWindow,
                          label=serial_list_label
                          )
        serialConnectionWindow.wm_protocol("WM_DELETE_WINDOW",
                                           lambda: self.on_closing_serial_gui(serialConnectionWindow, tr))

    def recording_GUI(self):
        """
        GUI where recording are visualized and cen be stopped/saved
        """

        def check_If_Number(value):
            try:
                float(value)
                return True
            except:
                return False

        # Check if all entrys were made
        error_msg = None
        if self.duration_time_options.get() and self.duration_entry.get() \
                and self.filename_idtype_options.get() and self.filename_entry.get():
            if check_If_Number(self.duration_entry.get()):

                # addDisplayToLogging("COM4", 7)

                # Recordung GUI ---------------------------------------------------------------------------------------
                recordingWindow = tk.Toplevel(self.gui)
                recordingWindow.title("Recording Gui")
                recordingWindow.geometry("{}x{}".format(500, 250))

                recordingWindow.wm_protocol("WM_DELETE_WINDOW",
                                            lambda: self.on_closing_recording_gui(recordingWindow,
                                                                                  self.recording_process_list))

                # Create Frames ---------------------------------------------------------------------------------------
                frame_filename = tk.Frame(master=recordingWindow, bg='#FFCFC9')
                frame_filename.pack(side="top")

                frame_recording_time = tk.Frame(master=recordingWindow, bg='#FFCFC9')
                frame_recording_time.pack(side="top")

                frame_content = tk.Frame(master=recordingWindow, bg='#FFCFC9')
                frame_content.pack(side="top")

                # Create Device dict ----------------------------------------------------------------------------------
                # log_queue, queue_handler, logger, scrolled_text
                for con_dev in connected_devices:
                    device_dict[con_dev] = dict()

                    # Create log_queue and add to dict
                    log_queue = Queue
                    device_dict[con_dev]["log_queue"] = log_queue

                    # create scrolled_text and add to dict
                    def create_scrolled_text():
                        scrolled_text = ScrolledText(frame_content, state='disabled', height=20)
                        scrolled_text.configure(font='TkFixedFont')
                        scrolled_text.tag_config('INFO', foreground='black')
                        scrolled_text.tag_config('DEBUG', foreground='gray')
                        scrolled_text.tag_config('WARNING', foreground='orange')
                        scrolled_text.tag_config('ERROR', foreground='red')
                        scrolled_text.tag_config('CRITICAL', foreground='red', underline=1)
                        scrolled_text.pack(side="top")
                        return scrolled_text

                    device_dict[con_dev]["scrolled_text"] = create_scrolled_text()

                # Filename label --------------------------------------------------------------------------------------

                filename_label = tk.Label(master=frame_filename, fg="blue",
                                          text=self.filename_entry.get())  # TODO: change to filename+filetyp (date)

                # Recording_time label --------------------------------------------------------------------------------

                self.time_label_text.set('Recording time: 0.0' + " of ")
                time_entry_label = tk.Entry(master=frame_recording_time, width=10)
                time_entry_label.insert(0, str(self.duration_entry.get()))
                recording_label = tk.Label(master=frame_recording_time, fg="blue", textvariable=self.time_label_text)

                # Create filename and max_time(with correct time_type) ------------------------------------------------

                filename = self.filename_entry.get() + self.filename_idtype_options.get()
                max_time = float(self.duration_entry.get())  # + self.duration_time_options.get()

                # Function that calls a thread which constantly updates the time --------------------------------------

                self.start_stop_button = tk.Button(master=frame_recording_time, text="Start", state=tk.NORMAL,
                                                   command=lambda: self.start_recording())

                # Set/pack Labels on Gui ------------------------------------------------------------------------------

                filename_label.pack(side="top")
                recording_label.pack(side="left")
                time_entry_label.pack(side="left")
                # self.scrolled_text.pack(side="top")
                self.start_stop_button.pack(side="left")


            else:
                error_msg = "Duration entry is not a int/float"
        else:
            error_msg = "Not all entrys were filled"

        if error_msg:
            error_recording_gui = tk.Toplevel(self.gui)
            error_recording_gui.title("Error Messages")
            error_recording_gui.geometry("{}x{}".format(250, 150))
            error_label = tk.Label(master=error_recording_gui, fg="red", text=error_msg)
            error_label.pack()

    # GUI-Functions ---------------------------------------------------------------------------------------------------
    def on_closing_serial_gui(self, gui_to_close, thread):
        """
        Closing tab and thread, also changes the existance of all buttons to False
        """
        # Close Tab
        gui_to_close.destroy()
        # Stop thread
        if thread:
            thread.stop_thread()
        # Set button of serial_devices on not Exist  (False)
        for btn in btnDevices:
            btnDevices[btn]["Exist"] = False

    def on_closing_recording_gui(self, gui_to_close, thread_list):
        """
        Closing tab and thread, also changes the existance of all buttons to False
        """
        # Close Tab
        gui_to_close.destroy()
        # Stop thread
        for thread in thread_list:
            thread.terminate()
        # Set button of serial_devices on not Exist  (False)
        for btn in btnDevices:
            btnDevices[btn]["Exist"] = False

        # Reset time_passed
        self.time_passed = 0

        # Reset Stop_recording
        global stop_recording
        stop_recording = False
        # Reverse recording_bool at the end
        global recording_bool
        recording_bool = False

    def delete_Content_of_Frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    # Recording functions ---------------------------------------------------------------------------------------------
    def start_recording(self):
        # Reverse recording_bool
        global recording_bool
        recording_bool = not recording_bool

        if recording_bool:  # after reverse, if True start recording, otherwise stop recording
            # Change label of Start_stop_button to "Stop"
            self.start_stop_button.config(text="Stop")

            # Start Process for every connected device
            self.recording_process_list = [mp.Process(target=self.record_serials, args=(connected_devices[x])) for x in
                                           range(len(connected_devices))]
            for p in self.recording_process_list:
                p.start()

            # Add Process for label_update
            print("size of thread_list: ", len(self.recording_process_list))
            label_process = mp.Process(target=self.update_label, args=(), daemon=True)
            self.recording_process_list.append(label_process)
            label_process.start()

            print("threads created!")



        # if start/stop-Button got clicked again, end all Threads and save logs
        else:
            global stop_recording
            stop_recording = True

    def display(self, record, device):
        # msg = self.queue_handler.format(record)
        msg = "[{}] {}".format(device, record)

        device_dict[device]["scrolled_text"].configure(state='normal')
        device_dict[device]["scrolled_text"].insert(tk.END, msg + '\n')
        device_dict[device]["scrolled_text"].configure(state='disabled')
        device_dict[device]["scrolled_text"].yview(tk.END)

        """
        self.scrolled_text.configure(state='normal')
        self.scrolled_text.insert(tk.END, msg + '\n', record.levelname)
        self.scrolled_text.configure(state='disabled')
        # Autoscroll to the bottom
        self.scrolled_text.yview(tk.END)
        """

    def update_label(self):
        start_time = time.time()
        max_time = self.time_entry_label.get()

        # During recordings, the time_entry is disabled
        self.time_entry_label.config(state=tk.DISABLED)

        # As long as time_passed is below max_time AND stop_recording is FALSE
        while self.time_passed <= float(max_time) and not stop_recording:
            # Check for device changes
            didnt_change_bool = get_all_devices()

            # If devices didnt change during recording
            if not didnt_change_bool:
                # Change Label ----------------------------------------------------------------
                self.time_label_text.set('Recording time: ' + str(self.time_passed) + " of ")
                # Change Logtext --------------------------------------------------------------
                # Check if a new Log is in queue to display
                for device in device_dict.keys():
                    try:
                        # record = self.log_queue.get(block=False)
                        record = device_dict[device]["log_queue"].get(block=False)


                    except Queue.empty():
                        pass
                    else:
                        if record:
                            self.display(record, device)

                global interval_recording
                if interval_recording:
                    time.sleep(interval_recording)

                # Update time_passed
                self.time_passed = time.time() - start_time

            # If device changed during recording
            else:
                print("size of device_list changed during recording")
                break
        self.time_entry_label.config(state=tk.NORMAL)
        self.delete_processes()
        # process all recordings
        self.edit_recordings(self.recording_window)

    def record_serials(self, devicename):
        """


        :param task: string: unique taskname
        :param user: string: name of user doing the tasks
        :return:
        """

        line = ''
        logfile = dict()
        self.running = True

        def add_to_queue(record):
            # logger.log(logging.INFO, record)
            device_dict[devicename]["log_queue"].put(record)

        while self.running:
            # Check if device still plugged in
            device = None
            for device_serial in allDevices.keys():
                if str(device_serial) == str(devicename):
                    device = device_serial

            if device:
                # try to read. if not possible, stop recording
                try:

                    lineIn = device.readline()
                    if lineIn != b'':
                        if not lineIn.endswith(b'\n'):
                            add_to_queue(lineIn)
                            line += lineIn.decode('utf-8')
                        else:
                            line += lineIn.decode('utf-8')
                            if "\n" in line:
                                splits = line.replace('\n', '').split(', ')
                                # print(splits)
                                if len(splits) == 4:
                                    if splits[0] not in logfile:
                                        logfile[splits[0]] = []
                                    logfile[splits[0]].append(
                                        splits[1:4])
                            line = ''
                except:
                    print("Cant read Serial: ", devicename, " ... Stop Recording")
                    global stop_recording
                    stop_recording = True
                    # sleep 1 second so we can give the looping function some more time
                    time.sleep(1)
            else:
                print("Device got unplugged during recording serial: ", devicename)
                break
        recording_dict[devicename] = logfile

    def delete_processes(self, *args):
        self.running = False
        # If also other Processes should be terminated
        if args:
            for process in args:
                process.terminate()

    # Save/Discard recorded Recordings --------------------------------------------------------------------------------
    def edit_recordings(self, recording_window):
        # Create Save and Discard button and make start/stop-Button unclickable until one Option is chosen
        frame_save = tk.Frame(master=recording_window, bg='#FFCFC9')
        frame_save.pack(side="top")

        if recording_dict:
            # Create Buttons (save/discard) on recording_gui
            save_Button = tk.Button(master=frame_save, text="Save", state=tk.NORMAL,
                                    command=lambda: self.create_file_of_recordings(frame_save))
            discard_Button = tk.Button(master=frame_save, text="Discard", state=tk.NORMAL,
                                       command=lambda: self.delete_recordings(frame_save))
            save_Button.pack(side="top")
            discard_Button.pack(side="top")
            # Change State of start/stop-Button until save/discard has been clicked
            self.start_stop_button.config(state=tk.DISABLED)

        else:
            print("Error on saving recordings, recording_dict is empty !")
            self.delete_recordings(frame_save)

    def create_file_of_recordings(self, frame):
        path_to_save = os.path.join("")
        ut.create_Data_file(recording_dict, path_to_save)
        # Reset
        self.start_stop_button.config(state=tk.NORMAL)
        self.delete_Content_of_Frame(frame)
        self.reset_recordings()

    def delete_recordings(self, frame):
        # Reset
        self.start_stop_button.config(state=tk.NORMAL)
        print("Reset CONTENT of Frame")
        self.delete_Content_of_Frame(frame)
        print("Reset RECORDINGS")
        self.reset_recordings()

    def reset_recordings(self):
        # Reset recording_dict
        if __name__ == '__main__':   recording_dict.clear()
        # Reset time_passed
        self.time_passed = 0
        self.time_label_text.set('Recording time: ' + str(self.time_passed) + " of ")
        # Reset start_stop_button to "Start"
        self.start_stop_button.config(text="Start")
        # Clear scrolledtext
        for device in device_dict.keys():
            device_dict[device]["scrolled_text"].delete("1.0", "end")
        # delete recording_window
        self.recording_window = None
        self.time_entry_label = None

        # Reset Stop_recording
        global stop_recording
        stop_recording = False
        # Reverse recording_bool at the end
        global recording_bool
        recording_bool = False


# --------------------------------

if __name__ == "__main__":
    # path = os.path.join(ROOT_DIR, "ToF", "logs")
    ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "logs"))
    path = os.path.join(ROOT_DIR)
    print(path)
    recording(path)

