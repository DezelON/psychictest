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
    num_data = request.session.get("num_data", [])

    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode) if body_unicode != "" else {} #Очередной костыль
        if body.get('num') is not None:
            num = body.get('num')
            request.session["psy_data"] = api.scoring(num, psy_data)
            request.session["num_data"].append(num)
            return HttpResponse(json.dumps(psy_data))
        else:
            if request.session.get("psy_start") is None:
                psy_data = api.init_answer_time(psy_data)
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
        answer = api.get_method(request, psy_data, num_data)
        return render(answer['request'], "game.html", answer['data'])