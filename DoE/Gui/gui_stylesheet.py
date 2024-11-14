# UPDATE THIS FILE IF NEW ELEMENTS WERE ADDED TO THE UI
import stylesheet as sty

class Gui_stylesheet:

    def __init__(self, ui):
        self.ui = ui
        self.set_topbar()
        self.set_sidebar_navi()
        self.set_main_settings()
        self.set_main_plan()
        self.set_tooltips_settings()


    def set_topbar(self):
        pass
        # TOP-BACKGROUND
        #self.ui.frame_toodle.setStyleSheet()
        self.ui.frame_top_east.setStyleSheet(u"background:{};".format(sty.NAVI))
        # ELEMENTS ON TOPBAR
        #self.ui.frame_appname.setStyleSheet(u"color:rgb(255,255,255);")
        #self.ui.lab_appname
        #self.ui.frame_user
        #self.ui.lab_user

    def set_sidebar_navi(self):
        self.ui.frame_bottom_west.setStyleSheet(u"background:{};".format(sty.NAVI))
        self.ui.bn_settings.setStyleSheet(sty.NAVI_BUTTONS)
        self.ui.bn_plan.setStyleSheet(sty.NAVI_BUTTONS)
        self.ui.bn_recordings.setStyleSheet(sty.NAVI_BUTTONS)


    def set_main_settings(self):
        # SETTING BACKGROUND
        self.ui.page_settings.setStyleSheet(u"background:{};".format(sty.MAIN_DARK))
        # SETTINGS_TAB
        self.ui.comboBox_settings.setStyleSheet(u"color:{};background:{};".format(sty.TEXT_COLOR_DARK, sty.INPUT))
        self.ui.spinBox_rep.setStyleSheet(u"color:{}; background:{};".format(sty.TEXT_COLOR_DARK, sty.INPUT))
        # STRATEGIE_TAB
        self.ui.lab_settings_strat_disc.setStyleSheet(u"color:{};".format(sty.TEXT_COLOR_LIGHT))
        self.ui.lab_settings_strat_hed.setStyleSheet(u"color:{};".format(sty.TEXT_COLOR_LIGHT))
        self.ui.comboBox_strat.setStyleSheet(u"color:{};background:{};".format(sty.TEXT_COLOR_DARK, sty.INPUT))
        # BUTTONS

        #self.ui.button_settings_start.setStyleSheet(u"color:{};".format(sty.TEXT_COLOR_LIGHT))
        # PLAIN TEXT
        # self.ui.plainTextEdit.setStyleSheet(u"background:{};".format(sty.INPUT))

    def set_tooltips_settings(self):
        # Set Tooltip for Input/label_settings
        self.ui.label_settings_1.setToolTip("Set designation-name. \nEx.: 'MotorID' or 'TubeID'")
        self.ui.input_settings_text_1.setToolTip("Set designation-name. \nEx.: 'MotorID' or 'TubeID'")

        self.ui.label_settings_2.setToolTip("Set ID's (in List-notation). \nEx.: 'healthy02, used2' or 'u04,h03,h01'")
        self.ui.input_settings_text_2.setToolTip("Set ID's (in List-notation). \nEx.: 'healthy02, used2' or 'u04,h03,h01'")

        self.ui.label_settings_3.setToolTip("Set cost. \nEx.: '100 seconds' or '20 minutes'")
        self.ui.input_settings_text_3.setToolTip("Set cost. \nEx.: '100 seconds' or '20 minutes'")

        # Set Tooltip for Buttons
        self.ui.button_settings_add_parameter.setToolTip("Add parameter to Table on Click")
        self.ui.button_settings_del_row.setToolTip("Delete selected row of Table on Click")
        self.ui.button_settings_load.setToolTip("Load previously saved settings/parameter into the table")
        self.ui.button_settings_save.setToolTip("Save all settings/parameter into a File")
        self.ui.button_settings_start.setToolTip("Start creating a Plan with given Parameter on Table")

        # Set Tooltip for SpinBox
        self.ui.settings_del_row.setToolTip("Select Row (starts at 1) to delete from Table")
        self.ui.spinBox_rep.setToolTip("Select Amount of Repetitions for each Parameter")

    def set_main_plan(self):
        # SETTING BACKGROUND
        self.ui.page_plan.setStyleSheet(u"background:{};".format(sty.MAIN_DARK))
        #self.ui.textBrowser_plan.setStyleSheet(u"background:{};".format(sty.INPUT))
        self.ui.lab_plan.setStyleSheet(u"color:{};".format(sty.TEXT_COLOR_LIGHT))
        self.ui.lab_plan_input_infos.setStyleSheet(u"color:{};".format(sty.TEXT_COLOR_LIGHT))



