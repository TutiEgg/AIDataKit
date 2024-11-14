# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1047, 709)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(10)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setSpacing(10)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(10, 10, 10, 10)
        self.comboBox_serialport = QComboBox(self.centralwidget)
        self.comboBox_serialport.setObjectName(u"comboBox_serialport")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_serialport.sizePolicy().hasHeightForWidth())
        self.comboBox_serialport.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(20)
        self.comboBox_serialport.setFont(font)

        self.gridLayout.addWidget(self.comboBox_serialport, 1, 1, 1, 1)

        self.text_usecase = QPlainTextEdit(self.centralwidget)
        self.text_usecase.setObjectName(u"text_usecase")
        sizePolicy1 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.text_usecase.sizePolicy().hasHeightForWidth())
        self.text_usecase.setSizePolicy(sizePolicy1)
        self.text_usecase.setFont(font)

        self.gridLayout.addWidget(self.text_usecase, 2, 1, 1, 1)

        self.text_output = QLabel(self.centralwidget)
        self.text_output.setObjectName(u"text_output")
        font1 = QFont()
        font1.setPointSize(30)
        self.text_output.setFont(font1)
        self.text_output.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.text_output, 3, 0, 1, 1)

        self.label_readerscript = QLabel(self.centralwidget)
        self.label_readerscript.setObjectName(u"label_readerscript")
        self.label_readerscript.setFont(font1)
        self.label_readerscript.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_readerscript, 0, 0, 1, 1)

        self.label_usecase = QLabel(self.centralwidget)
        self.label_usecase.setObjectName(u"label_usecase")
        self.label_usecase.setFont(font1)
        self.label_usecase.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_usecase, 2, 0, 1, 1)

        self.label_serialport = QLabel(self.centralwidget)
        self.label_serialport.setObjectName(u"label_serialport")
        self.label_serialport.setFont(font1)
        self.label_serialport.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_serialport, 1, 0, 1, 1)

        self.comboBox_input_readerscript = QComboBox(self.centralwidget)
        self.comboBox_input_readerscript.setObjectName(u"comboBox_input_readerscript")
        sizePolicy.setHeightForWidth(self.comboBox_input_readerscript.sizePolicy().hasHeightForWidth())
        self.comboBox_input_readerscript.setSizePolicy(sizePolicy)
        self.comboBox_input_readerscript.setFont(font)

        self.gridLayout.addWidget(self.comboBox_input_readerscript, 0, 1, 1, 1)

        self.spinBox_output = QSpinBox(self.centralwidget)
        self.spinBox_output.setObjectName(u"spinBox_output")
        sizePolicy.setHeightForWidth(self.spinBox_output.sizePolicy().hasHeightForWidth())
        self.spinBox_output.setSizePolicy(sizePolicy)
        self.spinBox_output.setFont(font)

        self.gridLayout.addWidget(self.spinBox_output, 3, 1, 1, 1)

        self.gridLayout.setRowStretch(0, 10)
        self.gridLayout.setRowStretch(1, 10)
        self.gridLayout.setRowStretch(2, 10)
        self.gridLayout.setRowStretch(3, 5)
        self.gridLayout.setColumnStretch(0, 10)
        self.gridLayout.setColumnStretch(1, 20)

        self.verticalLayout_2.addLayout(self.gridLayout)


        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.tableWidget = QTableWidget(self.centralwidget)
        self.tableWidget.setObjectName(u"tableWidget")

        self.verticalLayout.addWidget(self.tableWidget)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.btn_load = QPushButton(self.widget)
        self.btn_load.setObjectName(u"btn_load")
        self.btn_load.setFont(font)

        self.gridLayout_3.addWidget(self.btn_load, 1, 0, 1, 1)

        self.btn_save = QPushButton(self.widget)
        self.btn_save.setObjectName(u"btn_save")
        self.btn_save.setFont(font)

        self.gridLayout_3.addWidget(self.btn_save, 2, 0, 1, 1)


        self.horizontalLayout.addLayout(self.gridLayout_3)

        self.btn_start = QPushButton(self.widget)
        self.btn_start.setObjectName(u"btn_start")
        font2 = QFont()
        font2.setPointSize(50)
        self.btn_start.setFont(font2)

        self.horizontalLayout.addWidget(self.btn_start)


        self.horizontalLayout_2.addWidget(self.widget)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.verticalLayout.setStretch(0, 15)
        self.verticalLayout.setStretch(1, 17)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.text_output.setText(QCoreApplication.translate("MainWindow", u"Number Output:", None))
        self.label_readerscript.setText(QCoreApplication.translate("MainWindow", u"Readerscript:", None))
        self.label_usecase.setText(QCoreApplication.translate("MainWindow", u"Usecase:", None))
        self.label_serialport.setText(QCoreApplication.translate("MainWindow", u"Serial Port:", None))
        self.btn_load.setText(QCoreApplication.translate("MainWindow", u"Load Settings", None))
        self.btn_save.setText(QCoreApplication.translate("MainWindow", u"Save Settings", None))
        self.btn_start.setText(QCoreApplication.translate("MainWindow", u"Start", None))
    # retranslateUi

