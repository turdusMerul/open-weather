# api key from https://home.openweathermap.org/api_keys (needs registration)
# it's better to use your own key but this should still work fine
API_KEY = "c07d90f95de0fa31f69f050b18f0261f"


# importing python libs for working with datetime and HTTP requests
from datetime import datetime as dt
from requests import get as r_get


# define class weather date
class weather_date:

    # define class constructor
    def __init__(self, date : dt, sunrise : dt, sunset : dt, temp_night : float, feels_night : float):

        # set date field of class from date in datetime param
        self.date = date.date()

        # set daylight hours field of class from difference between sunrise and sunset time
        self.daylight_hours = sunset - sunrise

        # set temperature diffirence field of class from absolute difference
        # between "feels like" and "in fact" temperature at night
        self.temp_diff = abs(feels_night - temp_night)


    # attention: the following two method overrides - jugaad for a specific task 🙈
    # it can be done without it, but it will run slower this way


    # redefine methods of class objects comparing
    def __lt__(self, other):
        # when we compare two objects of class and checking if it LESS than another
        # we checking their TEMPERATURE DIFFERENCE fields
        return (self.temp_diff < other.temp_diff)


    def __gt__(self, other):
        # when we compare two objects of class and checking if it greater than another
        # we checking their DAYLIGHT HOURS fields
        return (self.daylight_hours > other.daylight_hours)


def get_weather_json(api_key : str):
    # get JSON data from openweathermap.org using API
    return(r_get(
        "https://api.openweathermap.org/data/2.5/onecall",
        {
            "lat" : "60.99",
            "lon" : "30.9",
            "exclude" : "current,minutely,hourly,alerts",
            "appid" : api_key,
            "units" : "metric",
            "lang" : "ru"
        }
    ).json()["daily"])


def wd_list_from_json(json_list):
    wd_list = []
    # for any date in JSON response create new object of weather date class and put it in list
    for wd_json in json_list:
        wd_list.append
        (
            weather_date
            (
                date = dt.fromtimestamp(wd_json["dt"]),
                sunrise = dt.fromtimestamp(wd_json["sunrise"]),
                sunset = dt.fromtimestamp(wd_json["sunset"]),
                temp_night = wd_json["temp"]["night"],
                feels_night = wd_json["feels_like"]["night"]
            )
        )
    return(wd_list)


# if main.py is main running file
if __name__ == "__main__":

    # getting JSON via API-request from openweathermap.org and using API key generated on the site 
    responsed_json = get_weather_json(API_KEY)

    # creating a list of weather date objects
    weather_dates = wd_list_from_json(responsed_json)

    # getting day with minimal difference in 'feels like' and 'in fact' temperature
    # and day with maximal daylight hours for the nearest five days
    # with using the weather date class jugaad
    wd1 = min(weather_dates)
    wd2 = max(weather_dates[:5])

    # and printing the results
    print(f"1. Day with minimal diffirence in 'feels like' and 'in fact' temperature:  {wd1.date} ({wd1.temp_diff})")
    print(f"2. Day with maximal daylight hours for the nearest five days:  {wd2.date} ({wd2.daylight_hours})")