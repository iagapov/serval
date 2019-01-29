from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from django.template import loader
from django.utils import timezone
import numpy as np
import pymongo
from datetime import datetime

def index(request):
    return HttpResponse("Polls index")

from .models import Question

import numpy as np

class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y


def plots(request):
    #return HttpResponse("Plots")


    template = loader.get_template('polls/plots.html')
    try:
        question = Question.objects.create(question_text="how so?", pub_date = timezone.now() )
    except Question.DoesNotExist:
        raise Http404("Question does not exist")

    context = {'question': question, 'data': [Point(0,1), Point(1,2), Point(2,4), Point(3,8), Point(3,8), Point(3,8), Point(3,8) ] }
    #context = {
    #    'latest_question_list': latest_question_list,
    #}
    return HttpResponse(template.render(context, request))

def detail(request, question_id):
    time_series = np.linspace(0,10,20)
    time_series = time_series**2
    labels = np.linspace(0,10, 20)
    response =  JsonResponse({"x":time_series.tolist(), "labels":labels.tolist()})
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
    return response

def results(request, question_id):
    client = pymongo.MongoClient("mongodb://serval.desy.de/accc_db") # defaults to port 27017
    db = client.acc_db
    record = db.posts.find_one({'tags':'petra'})
    tst = [datetime.utcfromtimestamp(t[1]) for t in record['data'][:]]
    val = [t[0] for t in record['data'][:]]
    response =  JsonResponse({"x":val, "labels":tst})
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
    return response

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
