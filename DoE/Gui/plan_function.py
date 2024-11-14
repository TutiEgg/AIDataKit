from datetime import datetime
from typing import Dict, Any, Union

import pandas as pd


from PySide6.QtWidgets import QFileDialog, QWidget
from PySide6 import QtCore

from main import MainWindow
from ..objects import *
from ..strategies import *
from main import *
from IO.read_create_files import *
from functools import partial
from definitions import *

from main import HEADER_LABELS
from math import isnan


# TODO: CHANGE THIS SO ITS INHERIT FROM MAINWINDOW
class Plan_function:
    def __init__(self, ui, errorUi, dialogUi, plan, attr_list):
        self.ui = ui
        self.errorUi = errorUi
        self.dialogUi = dialogUi
        self.table_plan = self.ui.tableWidget_plan_show
        self.plan = plan
        self.attr_list = attr_list
        self.check_list = []

        self.buttonImport = self.ui.button_plan_import
        self.buttonExport = self.ui.button_plan_export

        # CHANGE PLAN_TABLE-HEADER HERE
        self.header_labels = HEADER_LABELS  # TODO: This list should be global
        self.experiments_dict = {}

        self.initialize_gui_elements()

    def initialize_gui_elements(self):
        self.table_plan.setSortingEnabled(False)


        self.table_plan.setRowCount(len(self.plan.plan))
        self.table_plan.resizeColumnsToContents()
        self.table_plan.resizeRowsToContents()

        # INITIALIZE DOUBLE_CLICK ON CELL/HEADER EVENT
        self.table_plan.cellDoubleClicked.connect(self.cell_was_doubleclicked)
        self.table_plan.horizontalHeader().sectionDoubleClicked.connect(self.horizontal_header_was_doubleclicked)

        # INITIALIZE BUTTONS
        self.ui.button_plan_export.clicked.connect(lambda: self.save_plan())  # ONLY EXPORT
        # Enable button
        self.ui.button_plan_export.setEnabled(True)

    # TODO: lambda-function as parameter. Edit/upgrade this
    def lambda_function(self, name, message, btn1_name, btn1_func, btn2_name, btn2_func):
        self.dialogUi.dialogConstrict(name, message, btn1_name, btn1_func, btn2_name, btn2_func, "images/close.png")
        self.dialogUi.exec_()

    def test(self, msg):
        print("Msg: ", msg)

    def delete_plan(self):
        if bool(self.experiments_dict):
            for exp in self.experiments_dict:
                self.experiments_dict[exp]["btn"].deleteLater()
                self.experiments_dict[exp][self.header_labels[1]].deleteLater()
                self.experiments_dict[exp][self.header_labels[0]].deleteLater()
        else:
            print("NO")

    def show_plan(self, exp_dict=None):
        """

        Parameters
        ----------
        exp_dict:    If given, prioritize data inside of exp_dict over the automatic generation (filename, dates ...)

        Returns
        -------

        """

        experiments_dict = {}



        # ONE LOOP equals 1 ROW IN TABLE
        print(self.plan.plan)

        for exp_index in range(0, len(self.plan.plan)):

            header_list = self.header_labels.copy()
            # GET EXPERIMENT OBJECT
            exp_obj = self.plan.plan[exp_index]
            # EXPERIMENT NAME
            exp_name = exp_obj.name

            # SETTINGS_DICT ###########################################################################################
            # HERE YOU CAN SET THE CONTENT/TOOLTIP/EDITABLE OF EACH COLUMN (HEADER)
            # length of settings_dict.keys() should be the same as self.header_label


            setting_dict = {
                header_list[0]: {
                    "content_txt": exp_name,
                    "tooltip": str(exp_obj.attribute_dict),
                    "edit": False
                },
                header_list[1]: {
                    "content_txt": ("{}".format(exp_dict[exp_name][header_list[1]]) if exp_dict else ""),
                    "tooltip": "DOUBLE CLICK to change Date",
                    "edit": True
                },
                header_list[2]: {
                    "content_txt": ("{}".format(exp_dict[exp_name][header_list[2]]) if exp_dict else ""),
                    "tooltip": "DOUBLE CLICK to change Date",
                    "edit": True
                },
                header_list[3]: {
                    "content_txt": ("{}".format(exp_dict[exp_name][header_list[3]]) if exp_dict else ""),  # TODO: Should be generated on else
                    "tooltip": "DOUBLE CLICK to change Filename",
                    "edit": True
                },
                header_list[4]: {
                    "content_txt": ("{}".format(exp_dict[exp_name][header_list[4]]) if exp_dict else "{}".format(exp_obj.runtime_cost)),  # TODO: Should be saved as an int_object
                    "tooltip": "DOUBLE CLICK to change Filename",
                    "edit": True
                },
                #self.header_labels[5]: {
                #    "content_txt": "{}".format(self.rep),  # TODO: Should be saved as an int_object
                #    "tooltip": "EXISTING REPITION of this Experiment",
                #    "edit": False
                #},

            }

            # ADD ATTRIBUTES TO header_list AND Settings_dict #########################################################
            # --- ADD ATTRIBUTES TO header_list ---
            index_attr = 3  # THIS IS THE INDEX WHERE THE ATTRIBUTES SHOULD BE PLACED (FOR ORDER) INSIDE OF header_labels
            for i in range(len(self.attr_list)):
                header_list.insert(i + index_attr, self.attr_list[i].name)
            # --- ADD ATTRIBUTES TO settings_dict ---

            for attr in exp_obj.attribute_dict:
                temp_dict = {}
                temp_dict["content_txt"] = exp_obj.attribute_dict[attr]
                temp_dict["tooltip"] = "YOU CANT EDIT THIS, ONLY IN THE EXCEL"
                temp_dict["edit"] = False
                setting_dict[attr] = temp_dict

            ##############################################################################################

            # initialize plan_table #TODO: ONLY HAS TO BE INITIALIZED ONCE
            self.table_plan.setColumnCount(len(header_list))
            self.table_plan.setHorizontalHeaderLabels(header_list)

            print(header_list)
            print(exp_index)
            print(setting_dict.keys())

            # Loop through every header and add content to it
            for counter in range(0, len(header_list)):
                header = header_list[counter]
                print(header)
                # CHECK IF NAN IN DICT

                item = QTableWidgetItem("{}".format(setting_dict[header]["content_txt"]))
                item.setToolTip("" + setting_dict[header]["tooltip"])

                if not setting_dict[header]["edit"]:
                    item.setFlags(QtCore.Qt.ItemIsEnabled) # Set Item uneditable
                self.table_plan.setItem(exp_index, counter, item)


        self.table_plan.setSortingEnabled(True)

    def save_plan(self):
        col_count = self.table_plan.columnCount()
        header_list = []
        for i in range(0, col_count):
            header_list.append(self.table_plan.horizontalHeaderItem(i).text())

        data_matrix = []  # Rows and cols,  cell-content

        for row in range(0, self.table_plan.rowCount()):
            row_list = []
            for col in range(0, col_count):
                item = self.table_plan.item(row, col)
                item_text = item.text()
                row_list.append(item_text)
            data_matrix.append(row_list)

        df = pd.DataFrame(data_matrix, columns=header_list)
        filename = QtWidgets.QFileDialog.getSaveFileName(QFileDialog(),
                                                              "Selected Plan",
                                                              os.path.join(ROOT_DIR, "DoE", "Plan"))[0]
        if filename:
            if not filename.endswith(".xlsx"):
                filename += ".xlsx"
            df.to_excel(filename, index=False, sheet_name="Plan")

        print("Dataframe", df)

        # create_CSV_file(header_list=, )

    def cell_was_doubleclicked(self, row, column):
        print("Row %d and Column %d was clicked" % (row, column))
        print(self.header_labels[column])
        if self.header_labels[column] == "Executed_date":
            item = self.table_plan.item(row, column)
            print(item.text())
            print(item)
            if item.text() == "":
                today = datetime.now()
                self.table_plan.setItem(row,column, QTableWidgetItem(""+ today.strftime("%d_%m_%Y_%H:%M:%S")))

    def horizontal_header_was_doubleclicked(self, index):
        # TODO: MAybe add customized sorting later (for date)
        # Add here Customized Sorting
        print(self.table_plan.horizontalHeader().sortIndicatorOrder())
        #if self.table_plan.horizontalHeader().sortIndicatorOrder() == QtCore.Qt.SortOrder.DescendingOrder:
        #    self.table_plan.sortItems(index, QtCore.Qt.AscendingOrder)
        #else:
        #    self.table_plan.sortItems(index, QtCore.Qt.DescendingOrder)

