
TEXT_COLOR_LIGHT = "#FFFFFF"
TEXT_COLOR_DARK = "#000000"
NAVI = "#122B36"
MAIN_DARK = "#598392"
MAIN_LIGHT = "#AEC3B0"
INPUT = "#EFF6E0"

NAVI_BUTTONS = u"QPushButton {\n"
"	border: none;\n"
"	background-color: {};\n".format(NAVI)
"}\n"
"QPushButton:hover {\n"
"	background-color: {};\n".format(MAIN_LIGHT)
"}\n"
"QPushButton:pressed {\n"
"	background-color: {};\n".format(NAVI)
"}"