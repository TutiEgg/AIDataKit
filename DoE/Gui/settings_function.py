import re

from main import MainWindow
from ..objects import *
from ..strategies import *
from plan_function import *
from main import *
from definitions import *
import stylesheet as sty




class Settings_function():

    # TODO: CHANGE THIS SO ITS INHERIT FROM MAINWINDOW
    def __init__(self, ui, errorUi, dialogUi):
        self.ui = ui
        self.errorUi = errorUi
        self.dialogUi = dialogUi




    def initialize_gui_elements(self):
        # TODO: THIS FUNCTION SHOULD INITIALIZE ALL CHOOSEABLE OPTIONS (COMBO_BOX-ELEMENTS)
        self.all_strats_list = ["full_factor"]  # TODO: CHANGES THIS VALUE AUTOMATICALLY
        self.ui.comboBox_strat.clear()
        self.ui.comboBox_strat.addItems(self.all_strats_list)



        # TODO: TRY TO CHANGE. EVERY UI-VALUE SHOULD BE REFERED TO ANOTHER VARIABLE,  SO ON CHANGE OF UI-VARIABLE-NAMES U ONLY HAVE TO CHANGE THIS VARIABLE

        self.input_parameter_list = []
        self.input_table = self.ui.tableWidget_settings_paramter
        self.input_parameter_1 = self.ui.input_settings_text_1
        self.input_parameter_2 = self.ui.input_settings_text_2
        self.input_parameter_3 = self.ui.input_settings_text_3
        self.button_del_row = self.ui.button_settings_del_row
        self.input_del_row = self.ui.settings_del_row

        # CREATE VARIABLRS
        self.init_input_table()
        # DONT CREATE ELEMENTS ON THE GUI, ITS WAY EASIER TO ADD ELEMENTS HERE (CODE)

    def buttonPressed(self, buttonName):

        if buttonName == 'bn_settings_save':
            # Check how many Row exist in input_table
            rowCount = self.input_table.rowCount()
            if rowCount > 0:
                table_list = [] # 2 Dim List which will be saved in a file
                for row in range(0, rowCount):
                    designation = self.input_table.item(row, 0).text()
                    id = self.input_table.item(row, 1).text()
                    cost = self.input_table.item(row, 2).text()
                    table_list.append([designation, id, cost])
                file_tuple = QtWidgets.QFileDialog.getSaveFileName(QFileDialog(),
                                                              "Selected Plan",
                                                              os.path.join(ROOT_DIR, "DoE", "Strategies"))
                print(file_tuple[0])
                if file_tuple[0]:
                    file_name = file_tuple[0]+".json"
                    print(file_name)
                    with open(file_name, 'w') as f:
                        json.dump(table_list, f)

        elif buttonName == 'bn_settings_load':
            file_name = QtWidgets.QFileDialog.getOpenFileName(QFileDialog(),
                                                              "Selected Plan",
                                                              os.path.join(ROOT_DIR, "DoE", "Strategies"))[0]
            if file_name:
                with open(file_name, 'r') as file:
                    table_list = ujson.load(file)

                # Delete current Table
                self.input_table.setRowCount(0)
                # Fill Table with new Data of selected file
                for row in table_list:
                    self.add_parameter_to_table(row[0], row[1], row[2])

        elif buttonName == 'bn_settings_start':
            # GET INPUT VALUES FROM GUI
            repetition_value = self.ui.spinBox_rep.value()
            strategie_input = self.ui.comboBox_strat.currentText()

            # TODO: MAYBE PASS FUNCTION AS PARAMETERS INSTEAD OF IF/ELSE
            if strategie_input == "full_factor":
                # CHECK IF INPUT_VALUES ARE CORRECT

                if self.check_input_parameters_full_fact():

                    attr_list = self.create_attr_list()

                    plan = full_fact(attr_list, repetition_value)

                    plan_obj = Plan_function(self.ui, self.errorUi, self.dialogUi, plan, attr_list)
                    plan_obj.show_plan()

                    # Set UI transformation. As if it was clicked manually
                    # ------> this line clears the bg of all tabs
                    for each in self.ui.frame_bottom_west.findChildren(QFrame):
                        each.setStyleSheet(u"background:{};".format(sty.NAVI))

                    self.ui.stackedWidget.setCurrentWidget(self.ui.page_plan)
                    self.ui.lab_tab.setText("Plan")
                    self.ui.frame_plan.setStyleSheet(u"background:{};".format(sty.MAIN_DARK))
                else:
                    # TODO: USE errorexec
                    self.errorUi.errorConstrict("Incorrect Input given", "images/close.png", "Retry")
                    self.errorUi.exec_()

        elif buttonName == 'bn_settings_add_parameter':
            self.add_parameter_to_table(self.input_parameter_1.text(), self.input_parameter_2.text(), self.input_parameter_3.text())
        elif buttonName == "bn_settings_del_row":
            self.delete_parameter_of_table(self.input_del_row.value()-1)

    def delete_parameter_of_table(self, input):
        self.input_table.removeRow(input)

    def init_input_table(self):
        sb_col_value = 3
        sb_row_value = 0
        self.input_table.setColumnCount(sb_col_value)
        self.input_table.setRowCount(sb_row_value)

        for col in range(0, sb_col_value):
            for row in range(0, sb_row_value):
                newItem = QTableWidgetItem("")

                self.input_table.setItem(row, col, newItem)

    def add_parameter_to_table(self, input_parameter_1, input_parameter_2, input_parameter_3):
        # Add new empty Row to table
        rowPosition = self.input_table.rowCount()
        self.input_table.insertRow(rowPosition)
        # Add text to new row
        self.input_table.setItem(rowPosition,0, QTableWidgetItem("" + input_parameter_1))
        self.input_table.setItem(rowPosition, 1, QTableWidgetItem("" + input_parameter_2))
        self.input_table.setItem(rowPosition, 2, QTableWidgetItem("" + input_parameter_3))
    def change_input_table(self):
        sb_col_value = self.ui.settings_set_columns.value()
        sb_row_value = self.ui.settings_set_rows.value()
        if self.input_table.columnCount() > sb_col_value:
            for s in range(0, self.input_table.columnCount()-sb_col_value):
                self.input_table.removeColumn(self.input_table.columnCount()-1)
        elif self.input_table.columnCount() < sb_col_value:
            for s in range(0, sb_col_value-self.input_table.columnCount()):
                colPosition = self.input_table.columnCount()
                self.input_table.insertColumn(colPosition)

        if self.input_table.rowCount() > sb_row_value:
            for s in range(0, self.input_table.rowCount()-sb_row_value):
                self.input_table.removeRow(self.input_table.rowCount()-1)
        elif self.input_table.rowCount() < sb_row_value:
            for s in range(0, sb_row_value-self.input_table.rowCount()):
                rowPosition = self.input_table.rowCount()
                self.input_table.insertRow(rowPosition)

    def create_attr_list(self):
        # CREATES A LIST OF ATTRIBUTES IN GENERAL

        attribute_list = []
        for row_index in range(0, self.input_table.rowCount()):
            if self.input_table.item(row_index, 0) is not None:
                name = self.input_table.item(row_index, 0).text()
                attr_list = self.input_table.item(row_index, 1).text()
                attr_list = attr_list.strip('][').split(',')
                cost = self.input_table.item(row_index, 2).text()
                attribute_list.append(Attribute(name, attr_list, cost))

        return attribute_list

    def create_attr_list_general(self):
        # CREATES A LIST OF ATTRIBUTES IN GENERAL

        attribute_list = []
        for row_index in range(0, self.input_table.rowCount()):
            obj_attribute_list = []
            for col_index in range(0, self.input_table.columnCount()):
                obj_attribute_list.append(self.input_table.item(row_index, col_index).text())

            attribute_list.append(Attribute(*obj_attribute_list))
        return attribute_list



    def check_input_parameters_full_fact(self):
        input_table_col_amount = self.input_table.columnCount()
        if input_table_col_amount == 3:
            return True
        else:
            return False
