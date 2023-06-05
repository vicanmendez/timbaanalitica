from django.db import models
from django.urls import reverse
from datetime import date


# Create your models here.

class Lottery(models.Model):
    #moment could be 'morning', 'afternoon', 'evening'
    '''
    morning = 'mañana'
    afternoon = 'tarde'
    night = 'noche'
    MOMENTS = [
        (morning, 'mañana'),
        (afternoon, 'tarde'),
        (night, 'noche'),
    ]
    moment = models.CharField(max_length=20, choices=MOMENTS, default=morning)
    '''
    date = models.DateField(default=date.today)
    numbers_afternoon = models.JSONField(default=list)
    numbers_night = models.JSONField(default=list)
    
    def getDataAndSaveLottery(day, month, year):
        try:
            from .scrapper.scrapper import Scrapper
            myScrapper = Scrapper(day, month, year)
            my_date = date(int(year), int(month), int(day))
            numbers = myScrapper.getLottery()
            numbers_afternoon = numbers['afternoon']
            numbers_night = numbers['night']
            if (len(numbers_afternoon) > 0 or len(numbers_night) > 0):
                if(Lottery.objects.create(date=my_date, numbers_afternoon=numbers_afternoon, numbers_night=numbers_night)):
                    return True
        except: 
         return False
        return False

    
    