import datetime
import json
import requests


def time_converter(time):
    converted_time = datetime.datetime.fromtimestamp(
        int(time)
    ).strftime('%I:%M %p')
    return converted_time


def url_builder(city_id):
    user_api = 'd0b4680c681d693fab7ff26422b32040'  # Obtain yours form: http://openweathermap.org/
    unit = 'metric'  # For Fahrenheit use imperial, for Celsius use metric, and the default is Kelvin.
    api = 'http://api.openweathermap.org/data/2.5/weather?q='     # Search for your city ID here: http://bulk.openweathermap.org/sample/city.list.json.gz

    full_api_url = api + str(city_id) + '&mode=json&units=' + unit + '&APPID=' + user_api
    return full_api_url


def data_fetch(full_api_url):
    url = requests.get(full_api_url)
    output = url.text
    raw_api_dict = json.loads(output)
    return raw_api_dict


def data_organizer(raw_api_dict):
    data = dict(
        city=raw_api_dict.get('name'),
        country=raw_api_dict.get('sys').get('country'),
        temp=raw_api_dict.get('main').get('temp'),
        sky=raw_api_dict['weather'][0]['main'],
        wind=raw_api_dict.get('wind').get('speed'),
    )
    return data


def data_format(data):
    t_symbol = 'C'
    v_symbol = 'm/s'
    result = 'Current weather in: {}, {}:\n'.format(data['city'], data['country'])+\
            'Temperature is {}{}, {}, '.format(data['temp'], t_symbol, data['sky'])+\
            'Wind Speed is {}{}'.format(data['wind'], v_symbol)
    return result

def owm_get_weather(city):
    try:
        return data_format(data_organizer(data_fetch(url_builder(city))))
    except:
        return "Sorry, can't fetch weater in {}.".format(city)

if __name__ == "__main__":
    print owm_get_weather("moscow")