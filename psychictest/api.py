import random

from time import mktime
from datetime import datetime

from psychictest import config

def get_now_time():
    return int(mktime((datetime.now()).timetuple()))

def int_to_data(intTime):
    intTime = int(str(intTime)[0:10])
    data = datetime.fromtimestamp(intTime)
    return data

def init_psy_data():
    psy_data = []
    psy_count = random.randint(2, 6)
    for p in range(psy_count):
        psy_data.append({
            'status': 'wait',
            "credibility": 50,
            "history": [],
            "answer_time": 0
        })
    return psy_data

def get_method(request, psy_data, num_data):
    if psy_data is None:
        psy_data = init_psy_data()
        request.session["psy_data"] = psy_data
        request.session["num_data"] = num_data

    if request.session.get("psy_start") is not None:
        request.session['psy_start'] = None
    
    psy_history_len = 0

    for psy in psy_data:
        psy_history_len = psy_history_len if len(psy['history']) <= psy_history_len else len(psy['history'])

    if len(num_data) != psy_history_len:
        num_data.append('#')
        request.session["num_data"] = num_data

    answer = {
        'request': request,
        'data': {
            "psy_data": psy_data,
            "num_data": num_data
        }
    }
    
    return answer

def scoring(num, psy_data):
    for psy in psy_data:
        if int(psy['history'][-1]) == int(num):
            psy['credibility']+=1
            psy['status'] = 'win'
        else:
            psy['credibility']-=1
            psy['status'] = 'loss'
    return psy_data

def init_answer_time(psy_data):
    for psy in psy_data:
        psy['status'] = 'wait'
        psy["answer_time"] = random.randint(1, config.max_time_psy_wait) # маленькое читерство, по визуализации "реальных" экстрасенсов
    return psy_data