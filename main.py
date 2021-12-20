from datetime import datetime as dt
from requests import get as r_get


weather_json = r_get(
    "https://api.openweathermap.org/data/2.5/onecall", 
    {
        "lat" : "60.99",
        "lon" : "30.9",
        "exclude" : "current,minutely,hourly,alerts",
        "appid" : "c07d90f95de0fa31f69f050b18f0261f",
        "units" : "metric",
        "lang" : "ru"
    }
).json()["daily"]

wd_arr = []


class weather_date:
    def __init__(self, date : dt, sunrise : dt, sunset : dt, temp_night : float, feels_night : float):
        self.date = date.date()
        self.daylight_hours = sunset - sunrise
        self.temp_diff = abs(feels_night - temp_night)
    

    def __lt__(self, other):
        return (self.temp_diff < other.temp_diff)


    def __gt__(self, other):
        return (self.daylight_hours > other.daylight_hours)

    
for json_wd in weather_json:
    wd_arr.append(weather_date(
        date = dt.fromtimestamp(json_wd["dt"]),
        sunrise = dt.fromtimestamp(json_wd["sunrise"]),
        sunset = dt.fromtimestamp(json_wd["sunset"]),
        temp_night = json_wd["temp"]["night"],
        feels_night = json_wd["feels_like"]["night"]
        ))


if __name__ == "__main__":
    wd1 = min(wd_arr)
    wd2 = max(wd_arr[:5])
    print(f"1. Day with minimal diffirence in 'feels like' and 'in fact' temperature:  {wd1.date} ({wd1.temp_diff})")
    print(f"2. Day with maximal daylight hours for the nearest five days:  {wd2.date} ({wd2.daylight_hours})")