# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_main.ui'
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
        MainWindow.resize(1123, 839)
        MainWindow.setMinimumSize(QSize(800, 550))
        MainWindow.setLayoutDirection(Qt.LeftToRight)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"background:rgb(91,90,90);")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_top = QFrame(self.centralwidget)
        self.frame_top.setObjectName(u"frame_top")
        self.frame_top.setMaximumSize(QSize(16777215, 55))
        self.frame_top.setFrameShape(QFrame.NoFrame)
        self.frame_top.setFrameShadow(QFrame.Plain)
        self.horizontalLayout = QHBoxLayout(self.frame_top)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_toodle = QFrame(self.frame_top)
        self.frame_toodle.setObjectName(u"frame_toodle")
        self.frame_toodle.setMinimumSize(QSize(80, 55))
        self.frame_toodle.setMaximumSize(QSize(80, 55))
        self.frame_toodle.setStyleSheet(u"background:rgb(0,143,150);")
        self.frame_toodle.setFrameShape(QFrame.NoFrame)
        self.frame_toodle.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_toodle)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.toodle = QPushButton(self.frame_toodle)
        self.toodle.setObjectName(u"toodle")
        self.toodle.setMinimumSize(QSize(80, 55))
        self.toodle.setMaximumSize(QSize(80, 55))
        self.toodle.setStyleSheet(u"QPushButton {\n"
"	border: none;\n"
"	background-color: rgba(0,0,0,0);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(0,178,178);\n"
"}\n"
"QPushButton:pressed {\n"
"	background-color: rgba(0,0,0,0);\n"
"}")
        icon = QIcon()
        icon.addFile(u"", QSize(), QIcon.Normal, QIcon.Off)
        self.toodle.setIcon(icon)
        self.toodle.setIconSize(QSize(60, 40))
        self.toodle.setFlat(True)

        self.horizontalLayout_3.addWidget(self.toodle)


        self.horizontalLayout.addWidget(self.frame_toodle)

        self.frame_top_east = QFrame(self.frame_top)
        self.frame_top_east.setObjectName(u"frame_top_east")
        self.frame_top_east.setMaximumSize(QSize(16777215, 55))
        self.frame_top_east.setStyleSheet(u"background:rgb(51,51,51);")
        self.frame_top_east.setFrameShape(QFrame.NoFrame)
        self.frame_top_east.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_top_east)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.frame_appname = QFrame(self.frame_top_east)
        self.frame_appname.setObjectName(u"frame_appname")
        self.frame_appname.setFrameShape(QFrame.NoFrame)
        self.frame_appname.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_10 = QHBoxLayout(self.frame_appname)
        self.horizontalLayout_10.setSpacing(7)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.lab_appname = QLabel(self.frame_appname)
        self.lab_appname.setObjectName(u"lab_appname")
        font = QFont()
        font.setFamily(u"Segoe UI Light")
        font.setPointSize(24)
        self.lab_appname.setFont(font)
        self.lab_appname.setStyleSheet(u"color:rgb(255,255,255);")

        self.horizontalLayout_10.addWidget(self.lab_appname)


        self.horizontalLayout_4.addWidget(self.frame_appname)

        self.frame_user = QFrame(self.frame_top_east)
        self.frame_user.setObjectName(u"frame_user")
        self.frame_user.setFrameShape(QFrame.NoFrame)
        self.frame_user.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_9 = QHBoxLayout(self.frame_user)
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.lab_user = QLabel(self.frame_user)
        self.lab_user.setObjectName(u"lab_user")
        self.lab_user.setFont(font)
        self.lab_user.setStyleSheet(u"color:rgb(255,255,255);")
        self.lab_user.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_9.addWidget(self.lab_user)


        self.horizontalLayout_4.addWidget(self.frame_user)

        self.frame_person = QFrame(self.frame_top_east)
        self.frame_person.setObjectName(u"frame_person")
        self.frame_person.setMinimumSize(QSize(55, 55))
        self.frame_person.setMaximumSize(QSize(55, 55))
        self.frame_person.setFrameShape(QFrame.NoFrame)
        self.frame_person.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_8 = QHBoxLayout(self.frame_person)
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.lab_person = QLabel(self.frame_person)
        self.lab_person.setObjectName(u"lab_person")
        self.lab_person.setMaximumSize(QSize(55, 55))
        self.lab_person.setPixmap(QPixmap(u""))
        self.lab_person.setScaledContents(False)
        self.lab_person.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_8.addWidget(self.lab_person)


        self.horizontalLayout_4.addWidget(self.frame_person)

        self.frame_min = QFrame(self.frame_top_east)
        self.frame_min.setObjectName(u"frame_min")
        self.frame_min.setMinimumSize(QSize(55, 55))
        self.frame_min.setMaximumSize(QSize(55, 55))
        self.frame_min.setFrameShape(QFrame.NoFrame)
        self.frame_min.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_7 = QHBoxLayout(self.frame_min)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.bn_min = QPushButton(self.frame_min)
        self.bn_min.setObjectName(u"bn_min")
        self.bn_min.setMaximumSize(QSize(55, 55))
        self.bn_min.setStyleSheet(u"QPushButton {\n"
"	border: none;\n"
"	background-color: rgba(0,0,0,0);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(0,143,150);\n"
"}\n"
"QPushButton:pressed {\n"
"	background-color: rgba(0,0,0,0);\n"
"}")
        icon1 = QIcon()
        icon1.addFile(u"images/minimize.png", QSize(), QIcon.Normal, QIcon.Off)
        self.bn_min.setIcon(icon1)
        self.bn_min.setIconSize(QSize(22, 22))
        self.bn_min.setFlat(True)

        self.horizontalLayout_7.addWidget(self.bn_min)


        self.horizontalLayout_4.addWidget(self.frame_min)

        self.frame_max = QFrame(self.frame_top_east)
        self.frame_max.setObjectName(u"frame_max")
        self.frame_max.setMinimumSize(QSize(55, 55))
        self.frame_max.setMaximumSize(QSize(55, 55))
        self.frame_max.setFrameShape(QFrame.NoFrame)
        self.frame_max.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_6 = QHBoxLayout(self.frame_max)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.bn_max = QPushButton(self.frame_max)
        self.bn_max.setObjectName(u"bn_max")
        self.bn_max.setMaximumSize(QSize(55, 55))
        self.bn_max.setStyleSheet(u"QPushButton {\n"
"	border: none;\n"
"	background-color: rgba(0,0,0,0);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(0,143,150);\n"
"}\n"
"QPushButton:pressed {\n"
"	background-color: rgba(0,0,0,0);\n"
"}")
        icon2 = QIcon()
        icon2.addFile(u"images/maximize.png", QSize(), QIcon.Normal, QIcon.Off)
        self.bn_max.setIcon(icon2)
        self.bn_max.setIconSize(QSize(22, 22))
        self.bn_max.setFlat(True)

        self.horizontalLayout_6.addWidget(self.bn_max)


        self.horizontalLayout_4.addWidget(self.frame_max)

        self.frame_close = QFrame(self.frame_top_east)
        self.frame_close.setObjectName(u"frame_close")
        self.frame_close.setMinimumSize(QSize(55, 55))
        self.frame_close.setMaximumSize(QSize(55, 55))
        self.frame_close.setFrameShape(QFrame.NoFrame)
        self.frame_close.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_close)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.bn_close = QPushButton(self.frame_close)
        self.bn_close.setObjectName(u"bn_close")
        self.bn_close.setMaximumSize(QSize(55, 55))
        self.bn_close.setStyleSheet(u"QPushButton {\n"
"	border: none;\n"
"	background-color: rgba(0,0,0,0);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(0,143,150);\n"
"}\n"
"QPushButton:pressed {\n"
"	background-color: rgba(0,0,0,0);\n"
"}")
        icon3 = QIcon()
        icon3.addFile(u"images/close.png", QSize(), QIcon.Normal, QIcon.Off)
        self.bn_close.setIcon(icon3)
        self.bn_close.setIconSize(QSize(22, 22))
        self.bn_close.setFlat(True)

        self.horizontalLayout_5.addWidget(self.bn_close)


        self.horizontalLayout_4.addWidget(self.frame_close)


        self.horizontalLayout.addWidget(self.frame_top_east)


        self.verticalLayout.addWidget(self.frame_top)

        self.frame_bottom = QFrame(self.centralwidget)
        self.frame_bottom.setObjectName(u"frame_bottom")
        self.frame_bottom.setFrameShape(QFrame.NoFrame)
        self.frame_bottom.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_bottom)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame_bottom_west = QFrame(self.frame_bottom)
        self.frame_bottom_west.setObjectName(u"frame_bottom_west")
        self.frame_bottom_west.setMinimumSize(QSize(80, 0))
        self.frame_bottom_west.setMaximumSize(QSize(80, 16777215))
        self.frame_bottom_west.setStyleSheet(u"background:rgb(51,51,51);")
        self.frame_bottom_west.setFrameShape(QFrame.NoFrame)
        self.frame_bottom_west.setFrameShadow(QFrame.Plain)
        self.verticalLayout_3 = QVBoxLayout(self.frame_bottom_west)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.frame_settings = QFrame(self.frame_bottom_west)
        self.frame_settings.setObjectName(u"frame_settings")
        self.frame_settings.setMinimumSize(QSize(80, 55))
        self.frame_settings.setMaximumSize(QSize(160, 55))
        self.frame_settings.setFrameShape(QFrame.NoFrame)
        self.frame_settings.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_15 = QHBoxLayout(self.frame_settings)
        self.horizontalLayout_15.setSpacing(0)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.bn_settings = QPushButton(self.frame_settings)
        self.bn_settings.setObjectName(u"bn_settings")
        self.bn_settings.setMinimumSize(QSize(80, 55))
        self.bn_settings.setMaximumSize(QSize(160, 55))
        self.bn_settings.setStyleSheet(u"QPushButton {\n"
"	border: none;\n"
"	background-color: rgba(0,0,0,0);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(91,90,90);\n"
"}\n"
"QPushButton:pressed {\n"
"	background-color: rgba(0,0,0,0);\n"
"}")
        icon4 = QIcon()
        icon4.addFile(u"images/settings.png", QSize(), QIcon.Normal, QIcon.Off)
        self.bn_settings.setIcon(icon4)
        self.bn_settings.setIconSize(QSize(22, 22))
        self.bn_settings.setFlat(True)

        self.horizontalLayout_15.addWidget(self.bn_settings)


        self.verticalLayout_3.addWidget(self.frame_settings)

        self.frame_plan = QFrame(self.frame_bottom_west)
        self.frame_plan.setObjectName(u"frame_plan")
        self.frame_plan.setMinimumSize(QSize(80, 55))
        self.frame_plan.setMaximumSize(QSize(160, 55))
        self.frame_plan.setFrameShape(QFrame.NoFrame)
        self.frame_plan.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_16 = QHBoxLayout(self.frame_plan)
        self.horizontalLayout_16.setSpacing(0)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.bn_plan = QPushButton(self.frame_plan)
        self.bn_plan.setObjectName(u"bn_plan")
        self.bn_plan.setMinimumSize(QSize(80, 55))
        self.bn_plan.setMaximumSize(QSize(160, 55))
        self.bn_plan.setStyleSheet(u"QPushButton {\n"
"	border: none;\n"
"	background-color: rgba(0,0,0,0);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(91,90,90);\n"
"}\n"
"QPushButton:pressed {\n"
"	background-color: rgba(0,0,0,0);\n"
"}")
        icon5 = QIcon()
        icon5.addFile(u"images/plan.png", QSize(), QIcon.Normal, QIcon.Off)
        self.bn_plan.setIcon(icon5)
        self.bn_plan.setIconSize(QSize(22, 22))
        self.bn_plan.setFlat(True)

        self.horizontalLayout_16.addWidget(self.bn_plan)


        self.verticalLayout_3.addWidget(self.frame_plan)

        self.frame_recordings = QFrame(self.frame_bottom_west)
        self.frame_recordings.setObjectName(u"frame_recordings")
        self.frame_recordings.setMinimumSize(QSize(80, 55))
        self.frame_recordings.setMaximumSize(QSize(160, 55))
        self.frame_recordings.setFrameShape(QFrame.NoFrame)
        self.frame_recordings.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_17 = QHBoxLayout(self.frame_recordings)
        self.horizontalLayout_17.setSpacing(0)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.horizontalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.bn_recordings = QPushButton(self.frame_recordings)
        self.bn_recordings.setObjectName(u"bn_recordings")
        self.bn_recordings.setMinimumSize(QSize(80, 55))
        self.bn_recordings.setMaximumSize(QSize(160, 55))
        self.bn_recordings.setStyleSheet(u"QPushButton {\n"
"	border: none;\n"
"	background-color: rgba(0,0,0,0);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(91,90,90);\n"
"}\n"
"QPushButton:pressed {\n"
"	background-color: rgba(0,0,0,0);\n"
"}")
        icon6 = QIcon()
        icon6.addFile(u"images/Recording.png", QSize(), QIcon.Normal, QIcon.Off)
        self.bn_recordings.setIcon(icon6)
        self.bn_recordings.setIconSize(QSize(22, 12))
        self.bn_recordings.setFlat(True)

        self.horizontalLayout_17.addWidget(self.bn_recordings)


        self.verticalLayout_3.addWidget(self.frame_recordings)

        self.frame_spacer = QFrame(self.frame_bottom_west)
        self.frame_spacer.setObjectName(u"frame_spacer")
        self.frame_spacer.setFrameShape(QFrame.NoFrame)
        self.frame_spacer.setFrameShadow(QFrame.Plain)
        self.verticalLayout_4 = QVBoxLayout(self.frame_spacer)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_3.addWidget(self.frame_spacer)


        self.horizontalLayout_2.addWidget(self.frame_bottom_west)

        self.frame_bottom_east = QFrame(self.frame_bottom)
        self.frame_bottom_east.setObjectName(u"frame_bottom_east")
        self.frame_bottom_east.setFrameShape(QFrame.NoFrame)
        self.frame_bottom_east.setFrameShadow(QFrame.Plain)
        self.verticalLayout_2 = QVBoxLayout(self.frame_bottom_east)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(self.frame_bottom_east)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_14 = QHBoxLayout(self.frame)
        self.horizontalLayout_14.setSpacing(0)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.stackedWidget = QStackedWidget(self.frame)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setMinimumSize(QSize(0, 55))
        self.stackedWidget.setStyleSheet(u"")
        self.page_settings = QWidget()
        self.page_settings.setObjectName(u"page_settings")
        self.page_settings.setStyleSheet(u"background:rgb(91,90,90);")
        self.horizontalLayout_19 = QHBoxLayout(self.page_settings)
        self.horizontalLayout_19.setSpacing(0)
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.horizontalLayout_19.setContentsMargins(0, 5, 0, 5)
        self.frame_settings_main = QFrame(self.page_settings)
        self.frame_settings_main.setObjectName(u"frame_settings_main")
        self.frame_settings_main.setFrameShape(QFrame.NoFrame)
        self.frame_settings_main.setFrameShadow(QFrame.Plain)
        self.verticalLayout_5 = QVBoxLayout(self.frame_settings_main)
        self.verticalLayout_5.setSpacing(5)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(5, 5, 5, 5)
        self.lab_settings_hed = QLabel(self.frame_settings_main)
        self.lab_settings_hed.setObjectName(u"lab_settings_hed")
        self.lab_settings_hed.setMinimumSize(QSize(0, 55))
        self.lab_settings_hed.setMaximumSize(QSize(16777215, 55))
        font1 = QFont()
        font1.setFamily(u"Segoe UI Semilight")
        font1.setPointSize(24)
        self.lab_settings_hed.setFont(font1)
        self.lab_settings_hed.setLayoutDirection(Qt.LeftToRight)
        self.lab_settings_hed.setAutoFillBackground(False)
        self.lab_settings_hed.setStyleSheet(u"QLabel {\n"
"	color:rgb(255,255,255);\n"
"}")
        self.lab_settings_hed.setTextFormat(Qt.RichText)
        self.lab_settings_hed.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_5.addWidget(self.lab_settings_hed)

        self.comboBox_settings = QComboBox(self.frame_settings_main)
        self.comboBox_settings.addItem("")
        self.comboBox_settings.addItem("")
        self.comboBox_settings.setObjectName(u"comboBox_settings")

        self.verticalLayout_5.addWidget(self.comboBox_settings)

        self.frame_settings_parameter = QFrame(self.frame_settings_main)
        self.frame_settings_parameter.setObjectName(u"frame_settings_parameter")
        self.frame_settings_parameter.setFrameShape(QFrame.StyledPanel)
        self.frame_settings_parameter.setFrameShadow(QFrame.Raised)
        self.horizontalLayoutWidget = QWidget(self.frame_settings_parameter)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(430, 10, 371, 411))
        self.frame_settings_show_parameter = QHBoxLayout(self.horizontalLayoutWidget)
        self.frame_settings_show_parameter.setObjectName(u"frame_settings_show_parameter")
        self.frame_settings_show_parameter.setContentsMargins(0, 0, 0, 0)
        self.tableWidget_settings_paramter = QTableWidget(self.horizontalLayoutWidget)
        self.tableWidget_settings_paramter.setObjectName(u"tableWidget_settings_paramter")

        self.frame_settings_show_parameter.addWidget(self.tableWidget_settings_paramter)

        self.horizontalLayoutWidget_2 = QWidget(self.frame_settings_parameter)
        self.horizontalLayoutWidget_2.setObjectName(u"horizontalLayoutWidget_2")
        self.horizontalLayoutWidget_2.setGeometry(QRect(30, 420, 201, 51))
        self.frame_settings_rep = QHBoxLayout(self.horizontalLayoutWidget_2)
        self.frame_settings_rep.setObjectName(u"frame_settings_rep")
        self.frame_settings_rep.setContentsMargins(0, 0, 0, 0)
        self.label_rep = QLabel(self.horizontalLayoutWidget_2)
        self.label_rep.setObjectName(u"label_rep")
        font2 = QFont()
        font2.setPointSize(20)
        self.label_rep.setFont(font2)
        self.label_rep.setAlignment(Qt.AlignCenter)

        self.frame_settings_rep.addWidget(self.label_rep)

        self.spinBox_rep = QSpinBox(self.horizontalLayoutWidget_2)
        self.spinBox_rep.setObjectName(u"spinBox_rep")
        self.spinBox_rep.setMinimum(1)

        self.frame_settings_rep.addWidget(self.spinBox_rep)

        self.horizontalLayoutWidget_3 = QWidget(self.frame_settings_parameter)
        self.horizontalLayoutWidget_3.setObjectName(u"horizontalLayoutWidget_3")
        self.horizontalLayoutWidget_3.setGeometry(QRect(430, 430, 371, 41))
        self.frame_settings_buttons = QHBoxLayout(self.horizontalLayoutWidget_3)
        self.frame_settings_buttons.setObjectName(u"frame_settings_buttons")
        self.frame_settings_buttons.setContentsMargins(0, 0, 0, 0)
        self.button_settings_load = QPushButton(self.horizontalLayoutWidget_3)
        self.button_settings_load.setObjectName(u"button_settings_load")
        self.button_settings_load.setFont(font2)

        self.frame_settings_buttons.addWidget(self.button_settings_load)

        self.button_settings_save = QPushButton(self.horizontalLayoutWidget_3)
        self.button_settings_save.setObjectName(u"button_settings_save")
        self.button_settings_save.setFont(font2)
        self.button_settings_save.setMouseTracking(True)

        self.frame_settings_buttons.addWidget(self.button_settings_save)

        self.frame_settings_input_parameter_2 = QFrame(self.frame_settings_parameter)
        self.frame_settings_input_parameter_2.setObjectName(u"frame_settings_input_parameter_2")
        self.frame_settings_input_parameter_2.setGeometry(QRect(20, 10, 391, 391))
        self.frame_settings_input_parameter_2.setStyleSheet(u"#frame_settings_input_parameter_2 {border-radius: 4px; border: 4px solid #666464; padding: 10;}")
        self.frame_settings_input_parameter = QVBoxLayout(self.frame_settings_input_parameter_2)
        self.frame_settings_input_parameter.setObjectName(u"frame_settings_input_parameter")
        self.formLayout_settings = QFormLayout()
        self.formLayout_settings.setObjectName(u"formLayout_settings")
        self.label_settings_1 = QLabel(self.frame_settings_input_parameter_2)
        self.label_settings_1.setObjectName(u"label_settings_1")
        self.label_settings_1.setFont(font2)

        self.formLayout_settings.setWidget(1, QFormLayout.LabelRole, self.label_settings_1)

        self.input_settings_text_1 = QLineEdit(self.frame_settings_input_parameter_2)
        self.input_settings_text_1.setObjectName(u"input_settings_text_1")
        font3 = QFont()
        font3.setPointSize(12)
        self.input_settings_text_1.setFont(font3)

        self.formLayout_settings.setWidget(1, QFormLayout.FieldRole, self.input_settings_text_1)

        self.label_settings_2 = QLabel(self.frame_settings_input_parameter_2)
        self.label_settings_2.setObjectName(u"label_settings_2")
        self.label_settings_2.setFont(font2)

        self.formLayout_settings.setWidget(2, QFormLayout.LabelRole, self.label_settings_2)

        self.input_settings_text_2 = QLineEdit(self.frame_settings_input_parameter_2)
        self.input_settings_text_2.setObjectName(u"input_settings_text_2")
        self.input_settings_text_2.setFont(font3)

        self.formLayout_settings.setWidget(2, QFormLayout.FieldRole, self.input_settings_text_2)

        self.label_settings_3 = QLabel(self.frame_settings_input_parameter_2)
        self.label_settings_3.setObjectName(u"label_settings_3")
        self.label_settings_3.setFont(font2)

        self.formLayout_settings.setWidget(3, QFormLayout.LabelRole, self.label_settings_3)

        self.input_settings_text_3 = QLineEdit(self.frame_settings_input_parameter_2)
        self.input_settings_text_3.setObjectName(u"input_settings_text_3")
        self.input_settings_text_3.setFont(font3)

        self.formLayout_settings.setWidget(3, QFormLayout.FieldRole, self.input_settings_text_3)


        self.frame_settings_input_parameter.addLayout(self.formLayout_settings)

        self.button_settings_add_parameter = QPushButton(self.frame_settings_input_parameter_2)
        self.button_settings_add_parameter.setObjectName(u"button_settings_add_parameter")
        self.button_settings_add_parameter.setFont(font2)
        self.button_settings_add_parameter.setAutoFillBackground(False)

        self.frame_settings_input_parameter.addWidget(self.button_settings_add_parameter)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.frame_settings_input_parameter.addItem(self.horizontalSpacer)

        self.gridLayout_row = QGridLayout()
        self.gridLayout_row.setObjectName(u"gridLayout_row")
        self.gridLayout_row.setSizeConstraint(QLayout.SetNoConstraint)
        self.label_row = QLabel(self.frame_settings_input_parameter_2)
        self.label_row.setObjectName(u"label_row")
        self.label_row.setFont(font2)
        self.label_row.setAlignment(Qt.AlignCenter)

        self.gridLayout_row.addWidget(self.label_row, 0, 0, 1, 1)

        self.settings_del_row = QSpinBox(self.frame_settings_input_parameter_2)
        self.settings_del_row.setObjectName(u"settings_del_row")
        self.settings_del_row.setFont(font2)
        self.settings_del_row.setMinimum(1)
        self.settings_del_row.setMaximum(10)

        self.gridLayout_row.addWidget(self.settings_del_row, 0, 1, 1, 1)

        self.button_settings_del_row = QPushButton(self.frame_settings_input_parameter_2)
        self.button_settings_del_row.setObjectName(u"button_settings_del_row")
        self.button_settings_del_row.setFont(font2)

        self.gridLayout_row.addWidget(self.button_settings_del_row, 0, 2, 1, 2)


        self.frame_settings_input_parameter.addLayout(self.gridLayout_row)

        self.button_settings_start = QPushButton(self.frame_settings_parameter)
        self.button_settings_start.setObjectName(u"button_settings_start")
        self.button_settings_start.setGeometry(QRect(270, 420, 101, 51))
        self.button_settings_start.setFont(font2)

        self.verticalLayout_5.addWidget(self.frame_settings_parameter)


        self.horizontalLayout_19.addWidget(self.frame_settings_main)

        self.vert_divide = QFrame(self.page_settings)
        self.vert_divide.setObjectName(u"vert_divide")
        self.vert_divide.setFrameShape(QFrame.VLine)
        self.vert_divide.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_19.addWidget(self.vert_divide)

        self.frame_settings_strat = QFrame(self.page_settings)
        self.frame_settings_strat.setObjectName(u"frame_settings_strat")
        self.frame_settings_strat.setMinimumSize(QSize(220, 0))
        self.frame_settings_strat.setMaximumSize(QSize(220, 16777215))
        self.frame_settings_strat.setFrameShape(QFrame.NoFrame)
        self.frame_settings_strat.setFrameShadow(QFrame.Plain)
        self.verticalLayout_6 = QVBoxLayout(self.frame_settings_strat)
        self.verticalLayout_6.setSpacing(5)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(5, 5, 5, 5)
        self.lab_settings_strat_hed = QLabel(self.frame_settings_strat)
        self.lab_settings_strat_hed.setObjectName(u"lab_settings_strat_hed")
        self.lab_settings_strat_hed.setMinimumSize(QSize(0, 55))
        self.lab_settings_strat_hed.setMaximumSize(QSize(16777215, 55))
        self.lab_settings_strat_hed.setFont(font1)
        self.lab_settings_strat_hed.setStyleSheet(u"QLabel {\n"
"	color:rgb(255,255,255);\n"
"}")
        self.lab_settings_strat_hed.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_6.addWidget(self.lab_settings_strat_hed)

        self.comboBox_strat = QComboBox(self.frame_settings_strat)
        self.comboBox_strat.setObjectName(u"comboBox_strat")

        self.verticalLayout_6.addWidget(self.comboBox_strat)

        self.lab_settings_strat_disc = QLabel(self.frame_settings_strat)
        self.lab_settings_strat_disc.setObjectName(u"lab_settings_strat_disc")
        self.lab_settings_strat_disc.setEnabled(True)
        font4 = QFont()
        font4.setFamily(u"Segoe UI")
        font4.setPointSize(10)
        self.lab_settings_strat_disc.setFont(font4)
        self.lab_settings_strat_disc.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.verticalLayout_6.addWidget(self.lab_settings_strat_disc)


        self.horizontalLayout_19.addWidget(self.frame_settings_strat)

        self.stackedWidget.addWidget(self.page_settings)
        self.page_about_settings = QWidget()
        self.page_about_settings.setObjectName(u"page_about_settings")
        self.page_about_settings.setStyleSheet(u"background:rgb(91,90,90);")
        self.gridLayout_3 = QGridLayout(self.page_about_settings)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.lab_about_settings = QLabel(self.page_about_settings)
        self.lab_about_settings.setObjectName(u"lab_about_settings")
        self.lab_about_settings.setMinimumSize(QSize(0, 55))
        self.lab_about_settings.setMaximumSize(QSize(16777215, 55))
        font5 = QFont()
        font5.setFamily(u"Segoe UI")
        font5.setPointSize(24)
        self.lab_about_settings.setFont(font5)
        self.lab_about_settings.setStyleSheet(u"color:rgb(255,255,255);")

        self.gridLayout_3.addWidget(self.lab_about_settings, 0, 0, 1, 1)

        self.frame_about_settings = QFrame(self.page_about_settings)
        self.frame_about_settings.setObjectName(u"frame_about_settings")
        self.frame_about_settings.setFrameShape(QFrame.StyledPanel)
        self.frame_about_settings.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_28 = QHBoxLayout(self.frame_about_settings)
        self.horizontalLayout_28.setSpacing(0)
        self.horizontalLayout_28.setObjectName(u"horizontalLayout_28")
        self.horizontalLayout_28.setContentsMargins(5, 5, 0, 5)
        self.text_about_settings = QTextEdit(self.frame_about_settings)
        self.text_about_settings.setObjectName(u"text_about_settings")
        self.text_about_settings.setEnabled(True)
        self.text_about_settings.setFont(font4)
        self.text_about_settings.setStyleSheet(u"color:rgb(255,255,255);")
        self.text_about_settings.setFrameShape(QFrame.NoFrame)
        self.text_about_settings.setFrameShadow(QFrame.Plain)
        self.text_about_settings.setReadOnly(True)
        self.text_about_settings.setTextInteractionFlags(Qt.TextBrowserInteraction)

        self.horizontalLayout_28.addWidget(self.text_about_settings)

        self.vsb_about_settings = QScrollBar(self.frame_about_settings)
        self.vsb_about_settings.setObjectName(u"vsb_about_settings")
        self.vsb_about_settings.setStyleSheet(u"QScrollBar:vertical {\n"
"	background:rgb(51,51,51);\n"
"    width:20px;\n"
"    margin: 0px 0px 0px 0px;\n"
"}\n"
"QScrollBar::handle:vertical {\n"
"    background:rgb(0,143,170);\n"
"}\n"
"QScrollBar::add-page:vertical {\n"
" 	background:rgb(51,51,51);\n"
"}\n"
"QScrollBar::sub-page:vertical {\n"
" 	background:rgb(51,51,51);\n"
"}")
        self.vsb_about_settings.setOrientation(Qt.Vertical)

        self.horizontalLayout_28.addWidget(self.vsb_about_settings)


        self.gridLayout_3.addWidget(self.frame_about_settings, 1, 0, 1, 1)

        self.stackedWidget.addWidget(self.page_about_settings)
        self.page_about_recordings = QWidget()
        self.page_about_recordings.setObjectName(u"page_about_recordings")
        self.page_about_recordings.setStyleSheet(u"background:rgb(91,90,90);")
        self.horizontalLayout_29 = QHBoxLayout(self.page_about_recordings)
        self.horizontalLayout_29.setObjectName(u"horizontalLayout_29")
        self.stackedWidget.addWidget(self.page_about_recordings)
        self.page_about_empty_for_future_tabs = QWidget()
        self.page_about_empty_for_future_tabs.setObjectName(u"page_about_empty_for_future_tabs")
        self.page_about_empty_for_future_tabs.setStyleSheet(u"background:rgb(91,90,90);")
        self.stackedWidget.addWidget(self.page_about_empty_for_future_tabs)
        self.page_plan = QWidget()
        self.page_plan.setObjectName(u"page_plan")
        self.page_plan.setStyleSheet(u"background:rgb(91,90,90);")
        self.gridLayout = QGridLayout(self.page_plan)
        self.gridLayout.setObjectName(u"gridLayout")
        self.top_frame_plan = QHBoxLayout()
        self.top_frame_plan.setObjectName(u"top_frame_plan")
        self.top_frame_plan.setContentsMargins(-1, 10, -1, 10)
        self.lab_plan = QLabel(self.page_plan)
        self.lab_plan.setObjectName(u"lab_plan")
        font6 = QFont()
        font6.setPointSize(40)
        self.lab_plan.setFont(font6)

        self.top_frame_plan.addWidget(self.lab_plan)

        self.lab_plan_input_infos = QLabel(self.page_plan)
        self.lab_plan_input_infos.setObjectName(u"lab_plan_input_infos")
        self.lab_plan_input_infos.setFont(font2)

        self.top_frame_plan.addWidget(self.lab_plan_input_infos)


        self.gridLayout.addLayout(self.top_frame_plan, 2, 0, 1, 1)

        self.tableWidget_plan_show = QTableWidget(self.page_plan)
        self.tableWidget_plan_show.setObjectName(u"tableWidget_plan_show")
        self.tableWidget_plan_show.setFont(font2)

        self.gridLayout.addWidget(self.tableWidget_plan_show, 3, 0, 1, 1)

        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.button_plan_import = QPushButton(self.page_plan)
        self.button_plan_import.setObjectName(u"button_plan_import")
        self.button_plan_import.setFont(font2)

        self.horizontalLayout_18.addWidget(self.button_plan_import)

        self.button_plan_export = QPushButton(self.page_plan)
        self.button_plan_export.setObjectName(u"button_plan_export")
        self.button_plan_export.setFont(font2)

        self.horizontalLayout_18.addWidget(self.button_plan_export)


        self.gridLayout.addLayout(self.horizontalLayout_18, 5, 0, 1, 1)

        self.stackedWidget.addWidget(self.page_plan)
        self.page_about_plan = QWidget()
        self.page_about_plan.setObjectName(u"page_about_plan")
        self.page_about_plan.setStyleSheet(u"background:rgb(91,90,90);")
        self.gridLayout_4 = QGridLayout(self.page_about_plan)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(5, 5, 5, 5)
        self.lab_plan_2 = QLabel(self.page_about_plan)
        self.lab_plan_2.setObjectName(u"lab_plan_2")
        self.lab_plan_2.setMinimumSize(QSize(0, 55))
        self.lab_plan_2.setMaximumSize(QSize(16777215, 55))
        self.lab_plan_2.setFont(font1)
        self.lab_plan_2.setStyleSheet(u"color:rgb(255,255,255);")

        self.gridLayout_4.addWidget(self.lab_plan_2, 0, 0, 1, 1)

        self.textEdit_plan = QTextEdit(self.page_about_plan)
        self.textEdit_plan.setObjectName(u"textEdit_plan")

        self.gridLayout_4.addWidget(self.textEdit_plan, 1, 0, 1, 1)

        self.verticalScrollBar = QScrollBar(self.page_about_plan)
        self.verticalScrollBar.setObjectName(u"verticalScrollBar")
        self.verticalScrollBar.setOrientation(Qt.Vertical)

        self.gridLayout_4.addWidget(self.verticalScrollBar, 1, 1, 1, 1)

        self.stackedWidget.addWidget(self.page_about_plan)
        self.page_recordings = QWidget()
        self.page_recordings.setObjectName(u"page_recordings")
        self.page_recordings.setStyleSheet(u"background:rgb(91,90,90);")
        self.verticalLayout_8 = QVBoxLayout(self.page_recordings)
        self.verticalLayout_8.setSpacing(5)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(5, 5, 5, 5)
        self.lab_recording_main = QLabel(self.page_recordings)
        self.lab_recording_main.setObjectName(u"lab_recording_main")
        self.lab_recording_main.setMinimumSize(QSize(0, 55))
        self.lab_recording_main.setMaximumSize(QSize(16777215, 55))
        self.lab_recording_main.setFont(font5)
        self.lab_recording_main.setStyleSheet(u"QLabel {\n"
"	color:rgb(255,255,255);\n"
"}")

        self.verticalLayout_8.addWidget(self.lab_recording_main)

        self.frame_2 = QFrame(self.page_recordings)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setEnabled(True)
        self.frame_2.setMinimumSize(QSize(0, 235))
        self.frame_2.setMaximumSize(QSize(16777215, 235))
        font7 = QFont()
        font7.setFamily(u"Segoe UI")
        font7.setPointSize(12)
        self.frame_2.setFont(font7)
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setHorizontalSpacing(5)
        self.gridLayout_2.setVerticalSpacing(0)
        self.gridLayout_2.setContentsMargins(5, 5, 5, 5)
        self.label_2 = QLabel(self.frame_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(100, 0))
        font8 = QFont()
        font8.setFamily(u"Segoe UI")
        font8.setPointSize(14)
        self.label_2.setFont(font8)
        self.label_2.setStyleSheet(u"color:rgb(255,255,255);")

        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)

        self.label_3 = QLabel(self.frame_2)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(100, 0))
        self.label_3.setFont(font8)
        self.label_3.setStyleSheet(u"color:rgb(255,255,255);")

        self.gridLayout_2.addWidget(self.label_3, 1, 0, 1, 1)

        self.label_4 = QLabel(self.frame_2)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(100, 0))
        self.label_4.setFont(font8)
        self.label_4.setStyleSheet(u"color:rgb(255,255,255);")

        self.gridLayout_2.addWidget(self.label_4, 2, 0, 1, 1)

        self.line_label4 = QLineEdit(self.frame_2)
        self.line_label4.setObjectName(u"line_label4")
        self.line_label4.setMinimumSize(QSize(400, 25))
        self.line_label4.setMaximumSize(QSize(500, 25))
        self.line_label4.setFont(font7)
        self.line_label4.setStyleSheet(u"QLineEdit {\n"
"	color:rgb(255,255,255);\n"
"	border:2px solid rgb(51,51,51);\n"
"	border-radius:4px;\n"
"	background:rgb(51,51,51);\n"
"}\n"
"\n"
"QLineEdit:disabled {\n"
"	color:rgb(255,255,255);\n"
"	border:2px solid rgb(112,112,112);\n"
"	border-radius:4px;\n"
"	background:rgb(112,112,112);\n"
"}")

        self.gridLayout_2.addWidget(self.line_label4, 2, 1, 1, 3)

        self.line_label2 = QLineEdit(self.frame_2)
        self.line_label2.setObjectName(u"line_label2")
        self.line_label2.setEnabled(True)
        self.line_label2.setMinimumSize(QSize(400, 25))
        self.line_label2.setMaximumSize(QSize(500, 25))
        self.line_label2.setFont(font7)
        self.line_label2.setStyleSheet(u"QLineEdit {\n"
"	color:rgb(255,255,255);\n"
"	border:2px solid rgb(51,51,51);\n"
"	border-radius:4px;\n"
"	background:rgb(51,51,51);\n"
"}\n"
"\n"
"QLineEdit:disabled {\n"
"	color:rgb(255,255,255);\n"
"	border:2px solid rgb(112,112,112);\n"
"	border-radius:4px;\n"
"	background:rgb(112,112,112);\n"
"}")

        self.gridLayout_2.addWidget(self.line_label2, 0, 1, 1, 3)

        self.line_label3 = QLineEdit(self.frame_2)
        self.line_label3.setObjectName(u"line_label3")
        self.line_label3.setMinimumSize(QSize(400, 25))
        self.line_label3.setMaximumSize(QSize(500, 25))
        self.line_label3.setFont(font7)
        self.line_label3.setStyleSheet(u"QLineEdit {\n"
"	color:rgb(255,255,255);\n"
"	border:2px solid rgb(51,51,51);\n"
"	border-radius:4px;\n"
"	background:rgb(51,51,51);\n"
"}\n"
"\n"
"QLineEdit:disabled {\n"
"	color:rgb(255,255,255);\n"
"	border:2px solid rgb(112,112,112);\n"
"	border-radius:4px;\n"
"	background:rgb(112,112,112);\n"
"}")

        self.gridLayout_2.addWidget(self.line_label3, 1, 1, 1, 3)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_2, 1, 4, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_3, 3, 0, 1, 2)

        self.bn_recording_start = QPushButton(self.frame_2)
        self.bn_recording_start.setObjectName(u"bn_recording_start")
        self.bn_recording_start.setEnabled(True)
        self.bn_recording_start.setMinimumSize(QSize(69, 25))
        self.bn_recording_start.setMaximumSize(QSize(69, 25))
        self.bn_recording_start.setFont(font7)
        self.bn_recording_start.setStyleSheet(u"QPushButton {\n"
"	border: 2px solid rgb(51,51,51);\n"
"	border-radius: 5px;\n"
"	color:rgb(255,255,255);\n"
"	background-color: rgb(51,51,51);\n"
"}\n"
"QPushButton:hover {\n"
"	border: 2px solid rgb(0,143,150);\n"
"	background-color: rgb(0,143,150);\n"
"}\n"
"QPushButton:pressed {\n"
"	border: 2px solid rgb(0,143,150);\n"
"	background-color: rgb(51,51,51);\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(112,112,112);\n"
"	background-color: rgb(112,112,112);\n"
"}")

        self.gridLayout_2.addWidget(self.bn_recording_start, 3, 2, 1, 1)

        self.bn_recording_connect = QPushButton(self.frame_2)
        self.bn_recording_connect.setObjectName(u"bn_recording_connect")
        self.bn_recording_connect.setMinimumSize(QSize(69, 25))
        self.bn_recording_connect.setMaximumSize(QSize(69, 25))
        self.bn_recording_connect.setFont(font7)
        self.bn_recording_connect.setStyleSheet(u"QPushButton {\n"
"	border: 2px solid rgb(51,51,51);\n"
"	border-radius: 5px;\n"
"	color:rgb(255,255,255);\n"
"	background-color: rgb(51,51,51);\n"
"}\n"
"QPushButton:hover {\n"
"	border: 2px solid rgb(0,143,150);\n"
"	background-color: rgb(0,143,150);\n"
"}\n"
"QPushButton:pressed {\n"
"	border: 2px solid rgb(0,143,150);\n"
"	background-color: rgb(51,51,51);\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(112,112,112);\n"
"	background-color: rgb(112,112,112);\n"
"}")

        self.gridLayout_2.addWidget(self.bn_recording_connect, 3, 3, 1, 1)


        self.verticalLayout_8.addWidget(self.frame_2)

        self.verticalSpacer_2 = QSpacerItem(20, 162, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_8.addItem(self.verticalSpacer_2)

        self.stackedWidget.addWidget(self.page_recordings)
        self.page_empty_for_future_tabs = QWidget()
        self.page_empty_for_future_tabs.setObjectName(u"page_empty_for_future_tabs")
        self.page_empty_for_future_tabs.setStyleSheet(u"background:rgb(91,90,90);")
        self.verticalLayout_9 = QVBoxLayout(self.page_empty_for_future_tabs)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.stackedWidget.addWidget(self.page_empty_for_future_tabs)

        self.horizontalLayout_14.addWidget(self.stackedWidget)


        self.verticalLayout_2.addWidget(self.frame)

        self.frame_low = QFrame(self.frame_bottom_east)
        self.frame_low.setObjectName(u"frame_low")
        self.frame_low.setMinimumSize(QSize(0, 20))
        self.frame_low.setMaximumSize(QSize(16777215, 20))
        self.frame_low.setStyleSheet(u"")
        self.frame_low.setFrameShape(QFrame.NoFrame)
        self.frame_low.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_11 = QHBoxLayout(self.frame_low)
        self.horizontalLayout_11.setSpacing(0)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.frame_tab = QFrame(self.frame_low)
        self.frame_tab.setObjectName(u"frame_tab")
        font9 = QFont()
        font9.setFamily(u"Segoe UI")
        self.frame_tab.setFont(font9)
        self.frame_tab.setStyleSheet(u"background:rgb(51,51,51);")
        self.frame_tab.setFrameShape(QFrame.NoFrame)
        self.frame_tab.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_12 = QHBoxLayout(self.frame_tab)
        self.horizontalLayout_12.setSpacing(0)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.lab_tab = QLabel(self.frame_tab)
        self.lab_tab.setObjectName(u"lab_tab")
        font10 = QFont()
        font10.setFamily(u"Segoe UI Light")
        font10.setPointSize(10)
        self.lab_tab.setFont(font10)
        self.lab_tab.setStyleSheet(u"color:rgb(255,255,255);")

        self.horizontalLayout_12.addWidget(self.lab_tab)


        self.horizontalLayout_11.addWidget(self.frame_tab)

        self.frame_drag = QFrame(self.frame_low)
        self.frame_drag.setObjectName(u"frame_drag")
        self.frame_drag.setMinimumSize(QSize(20, 20))
        self.frame_drag.setMaximumSize(QSize(20, 20))
        self.frame_drag.setStyleSheet(u"background:rgb(51,51,51);")
        self.frame_drag.setFrameShape(QFrame.NoFrame)
        self.frame_drag.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_13 = QHBoxLayout(self.frame_drag)
        self.horizontalLayout_13.setSpacing(0)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(0, 0, 0, 0)

        self.horizontalLayout_11.addWidget(self.frame_drag)


        self.verticalLayout_2.addWidget(self.frame_low)


        self.horizontalLayout_2.addWidget(self.frame_bottom_east)


        self.verticalLayout.addWidget(self.frame_bottom)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.toodle.setText("")
        self.lab_appname.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><br/></p></body></html>", None))
        self.lab_user.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" color:#ffffff;\">Admin</span></p></body></html>", None))
        self.lab_person.setText("")
#if QT_CONFIG(tooltip)
        self.bn_min.setToolTip(QCoreApplication.translate("MainWindow", u"Minimize", None))
#endif // QT_CONFIG(tooltip)
        self.bn_min.setText("")
#if QT_CONFIG(tooltip)
        self.bn_max.setToolTip(QCoreApplication.translate("MainWindow", u"Maximize", None))
#endif // QT_CONFIG(tooltip)
        self.bn_max.setText("")
#if QT_CONFIG(tooltip)
        self.bn_close.setToolTip(QCoreApplication.translate("MainWindow", u"Close", None))
#endif // QT_CONFIG(tooltip)
        self.bn_close.setText("")
#if QT_CONFIG(tooltip)
        self.bn_settings.setToolTip(QCoreApplication.translate("MainWindow", u"Home", None))
#endif // QT_CONFIG(tooltip)
        self.bn_settings.setText("")
#if QT_CONFIG(tooltip)
        self.bn_plan.setToolTip(QCoreApplication.translate("MainWindow", u"Bug", None))
#endif // QT_CONFIG(tooltip)
        self.bn_plan.setText("")
#if QT_CONFIG(tooltip)
        self.bn_recordings.setToolTip(QCoreApplication.translate("MainWindow", u"Cloud", None))
#endif // QT_CONFIG(tooltip)
        self.bn_recordings.setText("")
        self.lab_settings_hed.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" color:#ffffff;\">Profile</span></p></body></html>", None))
        self.comboBox_settings.setItemText(0, QCoreApplication.translate("MainWindow", u"Settings_1", None))
        self.comboBox_settings.setItemText(1, QCoreApplication.translate("MainWindow", u"Settings_2", None))

        self.label_rep.setText(QCoreApplication.translate("MainWindow", u"Repitions", None))
        self.button_settings_load.setText(QCoreApplication.translate("MainWindow", u"Load", None))
        self.button_settings_save.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.label_settings_1.setText(QCoreApplication.translate("MainWindow", u"Parameter", None))
#if QT_CONFIG(tooltip)
        self.input_settings_text_1.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.label_settings_2.setText(QCoreApplication.translate("MainWindow", u"ID's", None))
        self.label_settings_3.setText(QCoreApplication.translate("MainWindow", u"Costs", None))
        self.button_settings_add_parameter.setText(QCoreApplication.translate("MainWindow", u"Add Parameter", None))
        self.label_row.setText(QCoreApplication.translate("MainWindow", u"Row", None))
        self.button_settings_del_row.setText(QCoreApplication.translate("MainWindow", u"Delete Row", None))
        self.button_settings_start.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.lab_settings_strat_hed.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" color:#ffffff;\">Stat </span></p></body></html>", None))
        self.lab_settings_strat_disc.setText(QCoreApplication.translate("MainWindow", u"Choose a Strategie", None))
        self.lab_about_settings.setText(QCoreApplication.translate("MainWindow", u"About: Settings (Docu)", None))
        self.lab_plan.setText(QCoreApplication.translate("MainWindow", u"   Plan", None))
        self.lab_plan_input_infos.setText(QCoreApplication.translate("MainWindow", u"All Infos of given Inputs", None))
        self.button_plan_import.setText(QCoreApplication.translate("MainWindow", u"Import Plan", None))
        self.button_plan_export.setText(QCoreApplication.translate("MainWindow", u"Export Plan", None))
        self.lab_plan_2.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" color:#ffffff;\">About Plan (docu)</span></p></body></html>", None))
        self.lab_recording_main.setText(QCoreApplication.translate("MainWindow", u"Recordings", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"DeviceID", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Recording_length", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Description", None))
        self.bn_recording_start.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
        self.bn_recording_connect.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
        self.lab_tab.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><br/></p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.frame_drag.setToolTip(QCoreApplication.translate("MainWindow", u"Drag", None))
#endif // QT_CONFIG(tooltip)
    # retranslateUi

