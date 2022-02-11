from haversine import haversine
import folium
import argparse
import re
from geopy.geocoders import Nominatim


def createMap():
    map = folium.Map()
    locator = Nominatim(user_agent="bob")
    args = parser.parse_args()
    year = args.year
    x = float(args.latitude)
    y = float(args.longtitude)
    src = args.src

    infos = []

    with open(src, "r", errors='ignore') as file:
        films = list(file)
        for film in films:
            to_delete = re.findall("{.+?}", str(film))
            if to_delete:
                film = film.replace(to_delete[0], "")
            info = re.findall("\\(.+?\\)", film)
            if not info:
                continue
            if info[0][1:-1] == year:
                location = locator.geocode(film.split(year)[1].strip())
                if location:
                    dis = haversine(location[1], (x, y))
                    infos.append((dis, location[1], film.split(
                        "("+year+")")[0][:-1].strip().rstrip("\" ").lstrip("\"").strip("'")))
                    if len(infos) >= 100:
                        break
    infos.sort(key=lambda x: x[0])
    closest = folium.FeatureGroup(name="Closest filmed")
    furthest = folium.FeatureGroup(name="Furthest filmed")
    for i in range(5):
        info = infos[i]
        closest.add_child(folium.Marker(location=info[1],
                                        popup=info[2],
                                        icon=folium.Icon()))
        info = infos[-i-1]
        furthest.add_child(folium.Marker(location=info[1],
                                         popup=info[2],
                                         icon=folium.Icon()))
        
    map.add_child(closest)
    map.add_child(furthest)
    map.add_child(folium.LayerControl())
    map.save("map.html")


parser = argparse.ArgumentParser()
parser.add_argument("year")
parser.add_argument("latitude")
parser.add_argument("longtitude")
parser.add_argument("src")

createMap()
