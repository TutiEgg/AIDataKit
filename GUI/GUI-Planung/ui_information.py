# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'information.ui'
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
        MainWindow.resize(913, 937)
        sizePolicy = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setSizeConstraint(QLayout.SetMinAndMaxSize)
        self.widget_information = QWidget(self.centralwidget)
        self.widget_information.setObjectName(u"widget_information")
        self.verticalLayout = QVBoxLayout(self.widget_information)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_information = QLabel(self.widget_information)
        self.label_information.setObjectName(u"label_information")
        font = QFont()
        font.setPointSize(40)
        self.label_information.setFont(font)
        self.label_information.setLayoutDirection(Qt.LeftToRight)
        self.label_information.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_information)

        self.textbrowser_information = QTextBrowser(self.widget_information)
        self.textbrowser_information.setObjectName(u"textbrowser_information")
        font1 = QFont()
        font1.setPointSize(12)
        self.textbrowser_information.setFont(font1)

        self.verticalLayout.addWidget(self.textbrowser_information)


        self.verticalLayout_2.addWidget(self.widget_information)

        self.widget_historie = QWidget(self.centralwidget)
        self.widget_historie.setObjectName(u"widget_historie")
        self.verticalLayout_3 = QVBoxLayout(self.widget_historie)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_historie = QLabel(self.widget_historie)
        self.label_historie.setObjectName(u"label_historie")
        self.label_historie.setFont(font)
        self.label_historie.setLayoutDirection(Qt.LeftToRight)
        self.label_historie.setAlignment(Qt.AlignCenter)

        self.verticalLayout_3.addWidget(self.label_historie)

        self.textBrowser_historie = QTextBrowser(self.widget_historie)
        self.textBrowser_historie.setObjectName(u"textBrowser_historie")
        font2 = QFont()
        font2.setPointSize(20)
        self.textBrowser_historie.setFont(font2)

        self.verticalLayout_3.addWidget(self.textBrowser_historie)


        self.verticalLayout_2.addWidget(self.widget_historie)

        self.widget_interpretation = QWidget(self.centralwidget)
        self.widget_interpretation.setObjectName(u"widget_interpretation")
        self.widget_interpretation.setMinimumSize(QSize(200, 250))
        font3 = QFont()
        font3.setPointSize(8)
        self.widget_interpretation.setFont(font3)
        self.widget_interpretation.setAutoFillBackground(False)
        self.horizontalLayout = QHBoxLayout(self.widget_interpretation)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetMinimumSize)
        self.label_interpretation = QLabel(self.widget_interpretation)
        self.label_interpretation.setObjectName(u"label_interpretation")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_interpretation.sizePolicy().hasHeightForWidth())
        self.label_interpretation.setSizePolicy(sizePolicy1)
        font4 = QFont()
        font4.setPointSize(80)
        self.label_interpretation.setFont(font4)
        self.label_interpretation.setCursor(QCursor(Qt.CrossCursor))
        self.label_interpretation.setAutoFillBackground(True)
        self.label_interpretation.setScaledContents(True)
        self.label_interpretation.setAlignment(Qt.AlignCenter)
        self.label_interpretation.setWordWrap(False)

        self.horizontalLayout.addWidget(self.label_interpretation)


        self.verticalLayout_2.addWidget(self.widget_interpretation)

        self.widget_save = QWidget(self.centralwidget)
        self.widget_save.setObjectName(u"widget_save")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_save)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.pushButton = QPushButton(self.widget_save)
        self.pushButton.setObjectName(u"pushButton")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy2)
        self.pushButton.setSizeIncrement(QSize(0, 0))
        font5 = QFont()
        font5.setPointSize(40)
        font5.setBold(False)
        font5.setItalic(False)
        font5.setUnderline(False)
        font5.setWeight(50)
        self.pushButton.setFont(font5)
        self.pushButton.setAutoFillBackground(False)
        self.pushButton.setIconSize(QSize(12, 12))
        self.pushButton.setAutoDefault(False)

        self.horizontalLayout_2.addWidget(self.pushButton)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout_2.addWidget(self.widget_save)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_information.setText(QCoreApplication.translate("MainWindow", u"Information", None))
        self.label_historie.setText(QCoreApplication.translate("MainWindow", u"Historie", None))
        self.label_interpretation.setText(QCoreApplication.translate("MainWindow", u"Interpretation", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Save Run", None))
    # retranslateUi

