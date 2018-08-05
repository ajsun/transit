import csv
import math

HOME_LAT = 40.714000
HOME_LON = -74.009564
EARTH_RADIUS_MILES = 3959
RADIUS = 0.25 

def deg2rad(deg):
    return deg * (math.pi / 180)

def get_distance_from_lat_lon(source_lat, source_lon, target_lat, target_lon):
    R = EARTH_RADIUS_MILES
    lat_distance = deg2rad(target_lat - source_lat)
    lon_distance = deg2rad(target_lon - source_lon)

    # haversine formula
    a = math.sin(lat_distance / 2) * math.sin(lat_distance / 2) + \
        math.cos(deg2rad(source_lat)) * math.cos(deg2rad(target_lat)) * \
        math.sin(lon_distance / 2) * math.sin(lon_distance / 2)
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c



def get_close_stops():
    close_stops = {}

    with open('google_transit/stops.txt') as stopsfile:
        stops = csv.DictReader(stopsfile)    
        for stop in stops:
            distance = get_distance_from_lat_lon(HOME_LAT, HOME_LON, float(stop['stop_lat']), float(stop['stop_lon']))
            if distance < RADIUS:
                close_stops[stop['stop_id']] = stop

    return close_stops