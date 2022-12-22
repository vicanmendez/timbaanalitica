from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import render
from .forms import ConsultaForm
from .models import Lottery
from datetime import datetime, timedelta



# Create your views here.

#Modificar en prod
url_server = "http://localhost:8000"

def homepage_view(request, *args, **kwargs):
    context = {
        "url_server": url_server,
        "active": "home",
    }
#    return HttpResponse("<h1>Hello World</h1>")
    return render(request, "index.html", context)


def notifications_view(request, *args, **kwargs):
    context = {
        "url_server": url_server,
        "active": "notifications",
    }
    return render(request,"notificaciones.html", context)

def analysis_view(request, *args, **kwargs):
    form = ConsultaForm(request.POST or None)
    #As we modified the form and the format of the date is not the same as the one in the database, we need to skip chequing date validation
    print (form.data)
    #Let's extract the dates range and and check if we already have the data in the database
    if (form.data.get('dates') != None):
        dates = form.data.get('dates')
        #get integers from dates string and then create datetime objects
        start_date = datetime(int(dates[0:4]), int(dates[5:7]), int(dates[8:10]))
        end_date = datetime(int(dates[13:18]), int(dates[19:21]), int(dates[22:24]))
        delta = end_date - start_date
        date_list = [start_date + timedelta(days=d) for d in range((delta).days + 1)] 
        for d in date_list:
            print(str(d)[0:10])
            #Check in the database if we already have the data
            try:
                obj = Lottery.objects.get(date=str(d)[0:10])
                if(obj != None):
                    print("Numeros del dia: " + str(d) + " son: " + str(obj.numbers))
            except Lottery.DoesNotExist:
                print("No tenemos los datos de la fecha: " + str(d))
        #deltadates = end_date - start_date
        #print(deltadates)
    form = ConsultaForm()
    context = {
        "form": form,
        "url_server": url_server,
        "active": "analysis",

    }
    return render(request,"nuevo.html", context)


