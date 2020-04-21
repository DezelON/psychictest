import json, asyncio, random

from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt

from psychictest import config, api

def index(request):

    request.session.clear()

    data = {
        "continue": request.session.get("psy_data") is not None
    }
    
    return render(request, "index.html", data)

@csrf_exempt
def game(request):

    psy_data = request.session.get("psy_data")
    num_data = request.session.get("num_data")

    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode) if body_unicode != "" else {} #Очередной костыль
        if body.get('num') is not None:
            num = body.get('num')
            for psy in psy_data:
                if int(psy['history'][-1]) == int(num):
                    psy['credibility']+=1
                    psy['status'] = 'win'
                else:
                    psy['credibility']-=1
                    psy['status'] = 'loss'
            request.session["psy_data"] = psy_data
            request.session["num_data"].append(num)
            return HttpResponse(json.dumps(psy_data))
        else:
            if request.session.get("psy_start") is None:
                for psy in psy_data:
                    psy['status'] = 'wait'
                    psy["answer_time"] = random.randint(1, config.max_time_psy_wait) # маленькое читерство, по визуализации "реальных" экстрасенсов
                request.session["psy_start"] = api.get_now_time()
                return HttpResponse(json.dumps({"action": "start"}))
            else:
                difference = api.get_now_time() - int(request.session["psy_start"])
                end = True
                for psy in psy_data: 
                    if psy["answer_time"] != 0 :
                        if difference > psy["answer_time"]:
                            psy["history"].append(random.randint(10, 99))
                            psy["answer_time"] = 0
                        end = False
                if end:
                    request.session["psy_start"] = None
                    return HttpResponse(json.dumps({"action": "end"}))
                else:
                    request.session["psy_data"] = psy_data
                    return HttpResponse(json.dumps(psy_data))
    elif request.method == "GET":
        if psy_data is None:
            psy_data = []
            num_data = []
            psy_count = random.randint(2, 6)
            for p in range(psy_count):
                psy_data.append({
                    'status': 'wait',
                    "credibility": 50,
                    "history": [],
                    "answer_time": 0
                })
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

        data = {
            "psy_data": psy_data,
            "num_data": num_data
        }

        return render(request, "game.html", data)