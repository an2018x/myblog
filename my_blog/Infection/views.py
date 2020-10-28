from django.shortcuts import render, redirect
from django.http import HttpResponse
from .infectionModel import Infection
import os

# Create your views here.

def processInfect(request):
    if request.method == 'POST':
        myModel = Infection()
        myFile = request.FILES.get('data',None)
        sources = request.POST.get('source',None)
        if not sources:
            pass
        else:
            sources=sources.split(',')
            alphaVal = request.POST.get('alpha', None)
            betaVal = request.POST.get('beta', None)
            myModel.setData(sources,alphaVal,betaVal)

        if not myFile:
            return HttpResponse("no files for upload!")
        destination = open(os.path.join('./',myFile.name),"wb+")
        for chunk in myFile.chunks():
            destination.write(chunk)
        destination.close()
        list = 'No'

        myModel.readfile(myFile.name)
        myModel.calNum()
        myModel.getAns()
        myModel.ans.sort()
        #print(model.ans)
        myModel.toChart()
        return render(request, 'graph_with_edge_options.html')
    elif request.method == 'GET':
        return render(request, 'infection/process.html')