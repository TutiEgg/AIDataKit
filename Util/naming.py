""" here can be different functions defined for naming of files and folders"""

from datetime import datetime


def create_name_with_date_and_time():
    """
     creates name out of dateand time
    Returns
    -------
    name : str (yyyy_mm_dd_xxh_xxm_xx_s
    """
    date = datetime.today().strftime('%Y_%m_%d')
    now = datetime.now()
    current_time = now.strftime("%Hh_%Mm_%Ss")
    name = date + '_'+ current_time
    return name