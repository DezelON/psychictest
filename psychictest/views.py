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

    if request.method == "POST":
        if request.session.get("psy_start") is None:
            for psy in psy_data:
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
                return HttpResponse(json.dumps({"action": "end"}))
            else:
                request.session["psy_data"] = psy_data
                return HttpResponse(json.dumps(psy_data))
    elif request.method == "GET":
        if psy_data is None:
            psy_data = []
            psy_count = random.randint(2, 6)
            for p in range(psy_count):
                psy_data.append({
                    "credibility": 50,
                    "history": [],
                    "answer_time": 0
                })
            request.session["psy_data"] = psy_data

        data = {
            "psy_data": psy_data
        }

        return render(request, "game.html", data)