# -*- coding: utf-8 -*-
import threading

import kivy
import requests
import time
from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.uix.floatlayout import FloatLayout
from requests import ConnectionError

Config.set('graphics', 'width', '809')
Config.set('graphics', 'height', '500')
kivy.require("1.10.0")


class Screen(FloatLayout):
    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)
        self.weather = Weather()

    def set_items(self):
        try:
            json_data = self.weather.request(t='weather')
            print json_data['cod']
            if int(json_data['cod']) != 200:
                self.popup_loading.title = 'Nie znaleziono miasta!'
                self.pb.value = 100
            else:
                print str(json_data['cod'])
                self.label_temp.text = str(int(json_data['main']['temp'])) + '°C'
                self.label_city.text = json_data['name']
                self.label_description.text = json_data['weather'][0]['description']
                self.label_pressure.text = str(json_data['main']['pressure']) + ' hPa'
                self.label_humidity.text = str(json_data['main']['humidity']) + '%'
                self.label_wind.text = str(json_data['wind']['speed']) + ' m/s'
                self.image_icon.source = 'http://openweathermap.org/img/w/' + json_data['weather'][0]['icon'] + '.png'


                timestruct = time.gmtime(json_data['dt'])
                print str(timestruct[0]) + '-' + str(timestruct[1]) + '-' + str(timestruct[2]) + ', ' + str(
                    timestruct[3]) + ':' + str(timestruct[4]) + ':' + str(timestruct[5])

        except ConnectionError:
            self.popup_loading.title = 'Problem z połączeniem!'
            self.pb.value = 100

        # FORECAST
        try:
            json_data = self.weather.request(t='forecast')
            self.forecast_label_1.text = json_data['list'][0]['dt_txt']
            self.forecast_icon_1.source = 'http://openweathermap.org/img/w/' + json_data['list'][0]['weather'][0]['icon'] + '.png'
            self.temp_forecast_label_1.text = str(int(json_data['list'][0]['main']['temp'])) + '°C'

            self.forecast_label_2.text = json_data['list'][1]['dt_txt']
            self.forecast_icon_2.source = 'http://openweathermap.org/img/w/' + json_data['list'][1]['weather'][0]['icon'] + '.png'
            self.temp_forecast_label_2.text = str(int(json_data['list'][1]['main']['temp'])) + '°C'

            self.forecast_label_3.text = json_data['list'][2]['dt_txt']
            self.forecast_icon_3.source = 'http://openweathermap.org/img/w/' + json_data['list'][2]['weather'][0]['icon'] + '.png'
            self.temp_forecast_label_3.text = str(int(json_data['list'][2]['main']['temp'])) + '°C'

            self.forecast_label_4.text = json_data['list'][3]['dt_txt']
            self.forecast_icon_4.source = 'http://openweathermap.org/img/w/' + json_data['list'][3]['weather'][0]['icon'] + '.png'
            self.temp_forecast_label_4.text = str(int(json_data['list'][3]['main']['temp'])) + '°C'

            self.forecast_label_5.text = json_data['list'][4]['dt_txt']
            self.forecast_icon_5.source = 'http://openweathermap.org/img/w/' + json_data['list'][4]['weather'][0]['icon'] + '.png'
            self.temp_forecast_label_5.text = str(int(json_data['list'][4]['main']['temp'])) + '°C'

            self.popup_loading.dismiss()
        except ConnectionError:
            self.popup_loading.title = 'Problem z połączeniem!'
            self.pb.value = 100

    def open_thread(self):
        thread = MyThread(self)
        thread.start()

    def next(self, dt):
        if self.pb.value >= 100:
            return False
        self.pb.value += 1

    def popen(self):
        self.popup_loading.title = 'Ładowanie..'
        self.pb.value = 0
        Clock.schedule_interval(self.next, 1 / 15)


class MyThread(threading.Thread):
    def __init__(self, screen):
        threading.Thread.__init__(self)
        self.screen = screen

    def run(self):
        self.screen.set_items()


class WeatherApp(App):
    def build(self):
        return Screen()


class Weather:
    def __init__(self):
        #self.type = 'weather'  # forecast - 5 dni prognoza
        self.city = 'None'
        self.units = 'metric'  # imperial - F
        self.lang = 'pl'
        self.api_key = '87a6b4d611741ef019ccde6d19820f67'

        self.json_data = {}
        self.forecast_data = {}

    def request(self, t):
        return requests.get('http://api.openweathermap.org/data/2.5/' + t + '?q=' + self.city
                         + '&units=' + self.units
                         + '&lang=' + self.lang
                         + '&APIKEY=' + self.api_key).json()


if __name__ == '__main__':
    WeatherApp().run()
