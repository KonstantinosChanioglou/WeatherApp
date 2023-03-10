import requests
import json
from geopy.geocoders import Nominatim
import datetime
from datetime import datetime, timedelta

API = ""

class Weather:
    
    beggin = 0;
    
    def __init__(self, location) -> None: #type-check the method and raise an error
        
        self.location = location

        try:
            self.lat, self.lon = self.getLocationInfo(location)
        except AttributeError:
            print("Custom Error: Invalid City")
            self.lat, self.lon = self.lat, self.lon
        except:
            print("Unkown Error has occured")

        self.currentWeatherData = {}
        self.forecastWeatherData = {}
        self.callApiCurrent()
        self.callApiForcast()
        

    def callApiCurrent(self):
        print("Api calling self lat:"+ str(self.lat)+" self long:"+ str(self.lon))
        url = "https://api.openweathermap.org/data/2.5/weather?lat=%s&lon=%s&appid=%s&units=metric" % (self.lat, self.lon, API) # Construct the URL with the parameters
        response = requests.get(url) #Calls API and get the response
        self.currentWeatherData = json.loads(response.text) #Convers json object into a dictionary with kyes and values

    def callApiForcast(self):
        url = "https://api.openweathermap.org/data/2.5/forecast?lat=%s&lon=%s&appid=%s&units=metric" % (self.lat, self.lon, API) # Construct the URL with the parameters
        response = requests.get(url) #Calls API and get the response
        self.forecastWeatherData = json.loads(response.text) #Convers json object into a dictionary with kyes and values


    #---- Curent Weather
    def getCountry(self):
        return "("+self.currentWeatherData['sys']['country']+")"
    
    def getLocation(self):
        return self.location
    
    def getCurrentPhoto(self):
        return self.currentWeatherData['weather'][0]['icon']
    
    def getCurrentDateTime(self):
        now = datetime.utcnow()
        now = now + timedelta(seconds=self.currentWeatherData['timezone'])
        return now.strftime("%Y-%m-%d %H:%M:%S")
    
    def getCurrentCondition(self):
        return self.currentWeatherData['weather'][0]['description']
    
    def getCurrentTemp(self):
       return self.currentWeatherData['main']['temp']
    
    def getCurrentFeelsLike(self):
        return self.currentWeatherData['main']['feels_like']
    
    def getCurrentHumidity(self):
       return self.currentWeatherData['main']['humidity']
    
    def getCurrentWind(self):
       return self.currentWeatherData['wind']['speed']


    #---- Forecat Weather
    def getForecastPhoto(self,step):
        return self.forecastWeatherData['list'][step]['weather'][0]['icon']
    
    def getForecastDateTime(self,step):
        dt = datetime.strptime(self.forecastWeatherData['list'][step]['dt_txt'], '%Y-%m-%d %H:%M:%S')
        dt = dt + timedelta(seconds=self.forecastWeatherData['city']['timezone'])
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    def getForecastCondition(self,step):
        return self.forecastWeatherData['list'][step]['weather'][0]['description']
    
    def getForecastTemp(self,step):
       return self.forecastWeatherData['list'][step]['main']['temp']
    
    def getForecastFeelsLike(self,step):
        return self.forecastWeatherData['list'][step]['main']['feels_like']
    
    def getForecastHumidity(self,step):
       return self.forecastWeatherData['list'][step]['main']['humidity']
    
    def getForecastWind(self,step):
       return self.forecastWeatherData['list'][step]['wind']['speed']

    def getLocationInfo(self, location):
        # Initialize Nominatim API
        geolocator = Nominatim(user_agent="WeatheApp")
        location = geolocator.geocode(location)
        return location.latitude, location.longitude
        
