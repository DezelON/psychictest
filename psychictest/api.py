from time import mktime
from datetime import datetime

def get_now_time():
    return int(mktime((datetime.now()).timetuple()))

def int_to_data(intTime):
    intTime = int(str(intTime)[0:10])
    data = datetime.fromtimestamp(intTime)
    return data