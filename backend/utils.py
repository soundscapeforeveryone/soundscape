import psycopg2
from psycopg2.extras import NamedTupleCursor
import json
# import math

with open('config.json', 'r') as json_file:
    config = json.load(json_file)

# def latLng_to_tile(lat_deg, lon_deg, zoom):
#   lat_rad = math.radians(lat_deg)
#   n = 2.0 ** zoom
#   tile_x = int((lon_deg + 180.0) / 360.0 * n)
#   tile_y = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
#   return (tile_x, tile_y)

# def tile_to_latLng(tile_x, tile_y, zoom):
#   n = 2.0 ** zoom
#   lon_deg = tile_x / n * 360.0 - 180.0
#   lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * tile_y / n)))
#   lat_deg = math.degrees(lat_rad)
#   return (lat_deg, lon_deg)

def soundscape_tile(zoom, x, y):
    conn = cursor = None
    try:
        conn = psycopg2.connect(**config)
        cursor = conn.cursor(cursor_factory=NamedTupleCursor)
        tile_query = f"SELECT * FROM import.soundscape_tile ({zoom}, {x}, {y});"
        cursor.execute(tile_query)
        value = cursor.fetchall()
        obj = {
            'type': 'FeatureCollection',
            'features': list(map(lambda x: x._asdict(), value))
        }
        tile = json.dumps(obj, sort_keys=True)
        return tile
    except psycopg2.Error as e:
       print(e)
       raise
    finally:
        if cursor != None:
            cursor.close()
        if conn != None:
            conn.close()

def check_number(number):
    try:
        number = float(number)
        return True
    except Exception:
        return False
    
# if __name__=='__main__':
#     #lat_deg = float(input("Latitude : "))
#     #lon_deg = float(input('Longitude : '))
#     #x, y = latLng_to_tile(lat_deg= lat_deg, lon_deg = lon_deg, zoom=16)
#     tile = soundscape_tile(zoom=16,x=33645,y=23376)
#     print(f"tile={tile}\ntype of tile = {type(tile)}")
#     #print("{}, {}".format(x, y))
#     #print(tile_to_latLng(33645, 23376, 16))