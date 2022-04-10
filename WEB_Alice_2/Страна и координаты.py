import requests


def get_geo_info(city_name, type_info):
    if type_info == "country":
        return get_country(city_name)
    elif type_info == "coordinates":
        return get_coordinates(city_name)
    else:
        return "invalid command"


def get_country(city_name):
    try:
        url = "https://geocode-maps.yandex.ru/1.x/"
        params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": city_name,
            "format": "json"
        }

        response = requests.get(url, params)
        json = response.json()
        return json["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"][
            "metaDataProperty"]["GeocoderMetaData"]["AddressDetails"]["Country"]["CountryName"]
    except Exception as e:
        return e


def get_coordinates(city_name):
    try:
        url = "https://geocode-maps.yandex.ru/1.x/"
        params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": city_name,
            "format": "json"
        }
        response = requests.get(url, params)
        json = response.json()
        coordinates_str = json["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]
        long, lat = map(float, coordinates_str.split())
        return long, lat
    except Exception as e:
        return e


print(get_geo_info("Лиссабон", "country"))
