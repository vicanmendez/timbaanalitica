# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 15:51:23 2022

@author: vicmn
"""

from bs4 import BeautifulSoup as bs
import requests
from datetime import datetime, timedelta


class Scrapper:
    def __init__(self, day, month, year, url):
        self.day = day
        self.month = month
        self.year = year
        self.url = url

    def __init__(self):
        self.url = "https://www.loteria.gub.uy/ver_resultados.php"
        
    def __init__(self, url):
        self.url = url
        
    def __init__(self, day, month, year):
        self.day = day
        self.month = month
        self.year = year
        self.url = "https://www.loteria.gub.uy/ver_resultados.php"
        
    def __del__(self):
        print("Destructor called, Scrapper object deleted")
        
    def setDay(self, dia):
        self.day = dia
        
    def setMonth(self, mes):
        self.month = mes
    
    def setYear(self, year):
        self.year = year
    
    def setUrl(self, url):
        self.url = url
        
    def getDay(self):
        return self.day
    
    def getMonth(self):
        return self.month
    
    def getYear(self):
        return self.year
    
    def getUrl(self):
        return self.year
    
    #Atributes: vdia, vmes, vano, vurl
    def getLottery(self):
        if(self.day != None and self.month != None and self.year != None and self.url != None):
            params = {
                "vdia": self.day,
                "vmes": self.month,
                "vano": self.year
                }
            document = requests.get(self.url, params)
            soup = bs(document.text, "html.parser")
            numbers_str = soup.findAll("div", {"class": "text_azul_3"})
            numbers = []
            afternoon = []
            night = []
            #Extract only the data contained within the tags we want
            #3 digit numbers: Quiniela, 2 digit: Tombola, 5 de Oro
            for number_str in numbers_str:
                n_raw = number_str.get_text()
                n_cleaned = n_raw.replace(" ", "")
                if len(n_cleaned) == 4:
                    print (n_cleaned)
                    numbers.append(n_cleaned)
            #Quiniela has 20 numbers, so the first 20 numbers are drawn at afternoon, the last 20 at night
            #If we retrieved only 20 numbers, it is night lottery
            if(len(numbers) == 40):
                afternoon = numbers[0:20]
                night = numbers[20:40]
            elif (len(numbers) == 20):
                night = numbers[0:20]

            '''
            Now, we noticed that the order of the lottery is not the same as exposed in HTML
            I.E: First number of the list, is the 1, second is the 11, third is 2, fourth is 12 and so on...
            So, TIDY UP
            '''
            orderer_afternoon = []
            orderer_night = []
            for i in range(0,20):
                if(i % 2 == 0):
                    if(len(afternoon) > 0 and afternoon[i] != '' and afternoon[i] != None):
                        orderer_afternoon.append(afternoon[i])
            for i in range(0,20):
                if(i % 2 != 0):
                    if(len(afternoon) > 0 and afternoon[i] != '' and afternoon[i] != None):
                        orderer_afternoon.append(afternoon[i])
            for i in range(0,20):
                if(i % 2 == 0):
                    if(len(night) > 0 and night[i] != '' and night[i] != None):
                        orderer_night.append(night[i])
            for i in range(0,20):
                if(i % 2 != 0):
                    if(len(night) > 0 and night[i] != '' and night[i] != None):
                        orderer_night.append(night[i])
        else:
            print("Error: Missing parameters, could not get lottery")
            return False   
        return {"afternoon": orderer_afternoon, "night": orderer_night}
    
    
    def getLotteriesByRange(self, start_date, end_date):
        lotteries = []
        #Get the difference between the dates
        delta = end_date - start_date
        #Create a list of dates
        date_list = [start_date + timedelta(days=d) for d in range((delta).days + 1)] 
        #Iterate over the list of dates and get the lottery for each date
        if(self.url != None):
            for d in date_list:
                print("Getting lottery for date: " + str(d))
                self.setDay(d.day)
                self.setMonth(d.month)
                self.setYear(d.year)
                lottery = self.getLottery()
                if(lottery):
                 lotteries.append(lottery)
            return lotteries
        else: 
            print("Error: Could not get lottery by range, missing url, may Lottery class is not initialized?")
            return False
    
                    



                 
