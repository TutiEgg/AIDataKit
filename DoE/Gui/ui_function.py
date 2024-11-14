

from main import *   # IMPORTING THE MAIN.PY FILE
import stylesheet as sty
#from about import *

GLOBAL_STATE = 0  # NECESSERY FOR CHECKING WEATHER THE WINDWO IS FULL SCREEN OR NOT
GLOBAL_TITLE_BAR = True  # NECESSERY FOR CHECKING WEATHER THE WINDWO IS FULL SCREEN OR NOT
init = False  # NECRESSERY FOR INITITTION OF THE WINDOW.


# tab_Buttons = ['bn_home', 'bn_bug', 'bn_android', 'bn_cloud'] #BUTTONS IN MAIN TAB
# android_buttons = ['bn_android_contact', 'bn_android_game', 'bn_android_clean', 'bn_android_world'] #BUTTONS IN ANDROID STACKPAGE

# THIS CLASS HOUSES ALL FUNCTION NECESSERY FOR THE PROGRAMME TO RUN.
class UIFunction(MainWindow):

    # ----> INITIAL FUNCTION TO LOAD THE FRONT STACK WIDGET AND TAB BUTTON I.E. HOME PAGE
    # INITIALISING THE WELCOME PAGE TO: HOME PAGE IN THE STACKEDWIDGET, SETTING THE BOTTOM LABEL AS THE PAGE NAME, SETTING THE BUTTON STYLE.
    def initStackTab(self):
        global init
        if not init:
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_settings)
            self.ui.lab_tab.setText("Settings")
            self.ui.frame_settings.setStyleSheet(u"background:{};".format(sty.MAIN_DARK))
            init = True

    ################################################################################################

    # ------> SETING THE APPLICATION NAME , WHERE LABEL NAMED: lab_appname()
    def labelTitle(self, appName):
        self.ui.lab_appname.setText(appName)

    ################################################################################################

    # ----> MAXIMISE/RESTORE FUNCTION
    # THIS FUNCTION MAXIMISES OUR MAINWINDOW WHEN THE MAXIMISE BUTTON IS PRESSED OR IF DOUBLE MOUSE LEFT PRESS IS DOEN OVER THE TOPFRMAE.
    # THIS MAKE THE APPLICATION TO OCCUPY THE WHOLE MONITOR.
    def maximize_restore(self):
        global GLOBAL_STATE
        status = GLOBAL_STATE
        if status == 0:
            self.showMaximized()
            GLOBAL_STATE = 1
            self.ui.bn_max.setToolTip("Restore")
            self.ui.bn_max.setIcon(QtGui.QIcon("images/restore.png"))  # CHANGE THE MAXIMISE ICON TO RESTOR ICON
            self.ui.frame_drag.hide()  # HIDE DRAG AS NOT NECESSERY
        else:
            GLOBAL_STATE = 0
            self.showNormal()
            self.resize(self.width() + 1, self.height() + 1)
            self.ui.bn_max.setToolTip("Maximize")
            self.ui.bn_max.setIcon(QtGui.QIcon("images/maximize.png"))  # CHANGE BACK TO MAXIMISE ICON
            self.ui.frame_drag.show()

    ################################################################################################

    # ----> RETURN STATUS MAX OR RESTROE
    # NECESSERY OFR THE MAXIMISE FUNCTION TRO WORK.
    def returStatus(self):
        return GLOBAL_STATE

    def setStatus(status):
        global GLOBAL_STATE
        GLOBAL_STATE = status

    # ------> TOODLE MENU FUNCTION
    # THIS FUNCTION TOODLES THE MENU BAR TO DOUBLE THE LENGTH OPENING A NEW ARE OF ABOUT TAB IN FRONT.
    # ASLO IT SETS THE ABOUT>SETTINGS AS THE FIRST PAGE.
    # IF THE PAGE IS IN THE ABOUT PAGE THEN PRESSING AGAIN WILL RESULT IN UNDOING THE PROCESS AND COMMING BACK TO THE
    # HOME PAGE.
    def toodleMenu(self, maxWidth, clicked):

        # ------> THIS LINE CLEARS THE BG OF PREVIOUS TABS : I.E. MAKING THEN NORMAL COLOR THAN LIGHTER COLOR.
        for each in self.ui.frame_bottom_west.findChildren(QFrame):
            each.setStyleSheet(u"background:{};".format(sty.NAVI))

        if clicked:
            currentWidth = self.ui.frame_bottom_west.width()  # Reads the current width of the frame
            minWidth = 80  # MINIMUN WITDTH OF THE BOTTOM_WEST FRAME
            if currentWidth == 80:
                extend = maxWidth
                # ----> MAKE THE STACKED WIDGET PAGE TO ABOUT HOME PAGE
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_about_settings)
                self.ui.lab_tab.setText("About > Settings")
                self.ui.frame_settings.setStyleSheet(
                    u"background:{};".format(sty.MAIN_DARK))

            else:
                extend = minWidth
                # -----> REVERT THE ABOUT HOME PAGE TO NORMAL HOME PAGE
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_settings)
                self.ui.lab_tab.setText("Settings")
                self.ui.frame_settings.setStyleSheet(u"background:{};".format(sty.MAIN_DARK))
            # THIS ANIMATION IS RESPONSIBLE FOR THE TOODLE TO MOVE IN A SOME FIXED STATE.
            self.animation = QPropertyAnimation(self.ui.frame_bottom_west, b"minimumWidth")
            self.animation.setDuration(300)
            self.animation.setStartValue(minWidth)
            self.animation.setEndValue(extend)
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation.start()

    ################################################################################################

    # -----> DEFAULT ACTION FUNCTION
    def constantFunction(self):
        # -----> DOUBLE CLICK RESULT IN MAXIMISE OF WINDOW
        def maxDoubleClick(stateMouse):
            if stateMouse.type() == QtCore.QEvent.MouseButtonDblClick:
                QtCore.QTimer.singleShot(250, lambda: UIFunction.maximize_restore(self))

        # ----> REMOVE NORMAL TITLE BAR
        if True:
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
            self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            self.ui.frame_appname.mouseDoubleClickEvent = maxDoubleClick
        else:
            self.ui.frame_close.hide()
            self.ui.frame_max.hide()
            self.ui.frame_min.hide()
            self.ui.frame_drag.hide()

        # -----> RESIZE USING DRAG
        # self.sizegrip = QSizeGrip(self.ui.frame_drag)
        # self.sizegrip.setStyleSheet("width: 20px; height: 20px; margin 0px; padding: 0px;")

        # SINCE THERE IS NO WINDOWS TOPBAR, THE CLOSE MIN, MAX BUTTON ARE ABSENT AND SO THERE IS A NEED FOR THE ALTERNATIVE BUTTONS IN OUR
        # DIALOG BOX, WHICH IS CARRIED OUT BY THE BELOW CODE
        # -----> MINIMIZE BUTTON FUNCTION
        self.ui.bn_min.clicked.connect(lambda: self.showMinimized())

        # -----> MAXIMIZE/RESTORE BUTTON FUNCTION
        self.ui.bn_max.clicked.connect(lambda: UIFunction.maximize_restore(self))

        # -----> CLOSE APPLICATION FUNCTION BUTTON
        self.ui.bn_close.clicked.connect(lambda: self.close())

    ################################################################################################################

    # ----> BUTTON IN TAB PRESSED EXECUTES THE CORRESPONDING PAGE IN STACKEDWIDGET PAGES
    def buttonPressed(self, buttonName):

        index = self.ui.stackedWidget.currentIndex()

        # ------> THIS LINE CLEARS THE BG OF PREVIOUS TABS
        for each in self.ui.frame_bottom_west.findChildren(QFrame):
            each.setStyleSheet(u"background:{};".format(sty.NAVI))

        if buttonName == 'bn_settings':
            if self.ui.frame_bottom_west.width() == 80 and index != 0:
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_settings)
                self.ui.lab_tab.setText("Settings")
                self.ui.frame_settings.setStyleSheet(u"background:{};".format(sty.MAIN_DARK))

            elif self.ui.frame_bottom_west.width() == 160 and index != 1:  # ABOUT PAGE STACKED WIDGET
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_about_settings)
                self.ui.lab_tab.setText("Home > Settings")
                self.ui.frame_settings.setStyleSheet(u"background:{};".format(sty.MAIN_DARK))

        elif buttonName == 'bn_plan':
            if self.ui.frame_bottom_west.width() == 80 and index != 5:
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_plan)
                self.ui.lab_tab.setText("Plan")
                self.ui.frame_plan.setStyleSheet(u"background:{};".format(sty.MAIN_DARK))

            elif self.ui.frame_bottom_west.width() == 160 and index != 4:  # ABOUT PAGE STACKED WIDGET
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_about_plan)
                self.ui.lab_tab.setText("Home > Plan")
                self.ui.frame_plan.setStyleSheet(u"background:{};".format(sty.MAIN_DARK))

        elif buttonName == 'bn_recordings':
            if self.ui.frame_bottom_west.width() == 80 and index != 7:
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_recordings)
                self.ui.lab_tab.setText("Recordings")
                self.ui.frame_recordings.setStyleSheet(u"background:{};".format(sty.MAIN_DARK))

            elif self.ui.frame_bottom_west.width() == 160 and index != 3:  # ABOUT PAGE STACKED WIDGET
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_about_recordings)
                self.ui.lab_tab.setText("Home > Recordings")
                self.ui.frame_recordings.setStyleSheet(u"background:{};".format(sty.MAIN_DARK))

        # ADD ANOTHER ELIF STATEMENT HERE FOR EXECTUITING A NEW MENU BUTTON STACK PAGE.

    ########################################################################################################################

    # ----> STACKWIDGET EACH PAGE FUNCTION PAGE FUNCTIONS
    # CODE TO PERFOMR THE TASK IN THE STACKED WIDGET PAGE
    # WHAT EVER WIDGET IS IN THE STACKED PAGES ITS ACTION IS EVALUATED HERE AND THEN THE REST FUNCTION IS PASSED.
    def stackPage(self):

        ######### PAGE_SETTINGS ############# BELOW DISPLAYS THE FUNCTION OF WIDGET, LABEL, PROGRESS BAR, E.T.C IN STACKEDWIDGET
        self.ui.lab_settings_hed.setText("Settings")
        self.ui.lab_settings_strat_hed.setText("Strategie")
        self.ui.lab_recording_main.setText("Recordings")


        ##########PAGE: ABOUT SETTINGS #############
        self.ui.text_about_settings.setText("This is the page where each attribute is listed in a table."
                                            "\nThe table consists of 3 columns: The first column is for the designation, "
                                            "\nThe second column is for the ID's of the respective designations. "
                                            "\nFor example, the IDs 'h04, h03,h01, u02' belong to the designation 'MotorID'. "
                                            "\nIf several IDs are used, they should be specified in a list notation. ('h01,h02,h03,...'). "
                                            "\nThe third column describes the time costs required for a recording."
                                            "\nIt is also possible to save attributes that have already been added to the table in a file or to load them again."
                                            "\nThe runs that can be specified are the same for all attributes.")
    ################################################################################################################################



    ################################################################################################################################



################################################################################################################################################