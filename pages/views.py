from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import render
from .forms import ConsultaForm
from .models import Lottery
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required


# Create your views here.

#Modificar en prod
url_server = "http://localhost:8000"

@login_required
def homepage_view(request, *args, **kwargs):
    if request.user.is_authenticated:
        print("Logged in")
    else:
        print("Not logged in")
    #Making up the view
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    delta = end_date - start_date
    date_list = [start_date + timedelta(days=d) for d in range((delta).days + 1)] 
    data = []
    numbers = {}
    #For instance, it is important to store the amount of times that a number is in the 1st position
    numbers_head = {}
    for d in date_list:
        #Check in the database if we already have the data
        try:
            obj = Lottery.objects.get(date=str(d)[0:10])
            data.append(obj)
            i=0
            for n in obj.numbers_afternoon:
                numbers[int(n)] = numbers.get(int(n), 0) + 1
                if(i==0):
                    numbers_head[int(n)] = numbers_head.get(int(n), 0) + 1
                i=i+1
            i=0
            for n in obj.numbers_night:
                if(i==0):
                    numbers_head[int(n)] = numbers_head.get(int(n), 0) + 1
                numbers[int(n)] = numbers.get(int(n), 0) + 1
                i = i+1
        except Lottery.DoesNotExist:
           #If we don't have the tdata, get the data from the website
            if(Lottery.getDataAndSaveLottery(str(d)[8:10], str(d)[5:7], str(d)[0:4])):
                lottery = Lottery.objects.get(date=str(d)[0:10])
                data.append(lottery)
                i=0
                for n in lottery.numbers_afternoon:
                    numbers[int(n)] = numbers.get(int(n), 0) + 1
                    if(i==0):
                        numbers_head[int(n)] = numbers_head.get(int(n), 0) + 1
                    i = i+1
                i=0
                for n in lottery.numbers_night:
                    numbers[int(n)] = numbers.get(int(n), 0) + 1
                    if(i==0):
                        numbers_head[int(n)] = numbers_head.get(int(n), 0) + 1
                    i = i+1
            else:
                print("Error al recuperar los datos")
    ndates = []
    myData = None
    if (data != None):
        for i in range(1, len(data)):
            ndates.append(i)
        myData = zip(data, ndates)
    numbers = sorted(numbers.items(), key=lambda x:x[1], reverse=True) 
    #numbers_head = sorted(numbers_head.items(), key=lambda x:x[1], reverse=True) 
    numbers = dict(numbers)
    numbers_head = dict(numbers_head)
    
                
    context = {
        "url_server": url_server,
        "active": "home",
        "data": myData,
        "numbers": numbers,
        "numbers_head": numbers_head,
    }
#    return HttpResponse("<h1>Hello World</h1>")
    return render(request, "index.html", context)


@login_required
def notifications_view(request, *args, **kwargs):
    context = {
        "url_server": url_server,
        "active": "notifications",
    }
    return render(request,"notificaciones.html", context)


@login_required
def analysis_view(request, *args, **kwargs):
    form = ConsultaForm(request.POST or None)
    #As we modified the form and the format of the date is not the same as the one in the database, we need to skip chequing date validation
    print (form.data)
    #Let's extract the dates range and and check if we already have the data in the database
    #define an array of 1000 integers using list comprehension
    numbers = {}
    data = None
    typeFilter = None
    top = None
    if (form.data.get('dates') != None):
        typeFilter = form.data.get('typeFilter')
        top = form.data.get('numberFilter')
        print("Tipo de filtro: " + typeFilter + " Numeros a mostrar: " + top)
        data = []
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
                data.append(obj)
                for n in obj.numbers_afternoon:
                    numbers[int(n)] = numbers.get(int(n), 0) + 1
                for n in obj.numbers_night:
                    numbers[int(n)] = numbers.get(int(n), 0) + 1
            except Lottery.DoesNotExist:
                print("No tenemos los datos de la fecha: " + str(d))
                print("Haciendo scrapping y recuperando data...")
                if(Lottery.getDataAndSaveLottery(str(d)[8:10], str(d)[5:7], str(d)[0:4])):
                    print("Datos recuperados y guardados en la base de datos")
                    lottery = Lottery.objects.get(date=str(d)[0:10])
                    data.append(lottery)
                    for n in lottery.numbers_afternoon:
                        numbers[int(n)] = numbers.get(int(n), 0) + 1
                    for n in lottery.numbers_night:
                        numbers[int(n)] = numbers.get(int(n), 0) + 1
                else:
                    print("Error al recuperar los datos")
                
        #deltadates = end_date - start_date
        #print(deltadates)
    form = ConsultaForm()
    ndates = []
    myData = None
    if (data != None):
        for i in range(1, len(data)):
            ndates.append(i)
        myData = zip(data, ndates)
    if(typeFilter != None):
        if (typeFilter == '1'):
            print("Ordenando los números de mayor a menor")
            numbers = sorted(numbers.items(), key=lambda x:x[1], reverse=True) 
            numbers = dict(numbers)
        elif (typeFilter == '2'):
            print("Ordenando los números de menor a mayor")
            numbers = sorted(numbers.items(), key=lambda x:x[1]) 
            numbers = dict(numbers)
    if (top != None):
        try:
            new_dict = {}
            # Iterate over the dictionary and add the elements to the new dictionary
            for i, (key, value) in enumerate(numbers.items()):
                new_dict[key] = value
                if i+1 == int(top):
                    break
            numbers = new_dict
        except:
            print("No se esta filtrando por cantiad de numeros")
    print(numbers)
    context = {
        "form": form,
        "url_server": url_server,
        "active": "analysis",
        "data": myData,
        "numbers": numbers,
        

    }
    return render(request,"nuevo.html", context)

#Function that receives a dictionary and an integer and returns a dictionary with the first x elements of the dictionary
    def first_x_elements(dictionary, x):
        # Create an empty dictionary to store the elements
        new_dict = {}
        # Iterate over the dictionary and add the elements to the new dictionary
        for i, (key, value) in enumerate(dictionary.items()):
            new_dict[key] = value
            if i+1 == x:
                break
        # Return the new dictionary
        return new_dict


