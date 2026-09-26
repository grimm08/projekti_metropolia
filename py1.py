import random
from geopy.distance import geodesic

import mysql.connector
datastorage = mysql.connector.connect(
    host='127.0.0.1',
    port= 3306,
    database= 'flight_game',
    user= 'root',
    password= 'ak08mh77',
    autocommit= True
)

#def pullout_data(location, location2):


def ticket_price(xlat,xlot, ylat,ylot):
    dis = geodesic(xlat,xlot,ylat,ylot).km
    ticket_price = dis * 0.50
    return ticket_price
def check_name(country):
    chk = f"select iso_country from country where iso_country = '{country}'"
    cursor = datastorage.cursor()
    cursor.execute(chk)
    result = cursor.fetchall()
    if not result:
        return False
    else:
        return True
#def travel_plan(location, location2):


while True:
    my_place = input("Enter your place: ")
    if check_name(my_place):
        print("Please enter a valid place")

    else:
        sql = f"select airport.name, ident from airport join country on airport.iso_country = country.iso_country where airport.type = 'large_airport' and country.name = '{my_place}' order by airport.iso_country;"
        crosri = datastorage.cursor()
        crosri.execute(sql)
        values = crosri.fetchall()
        for i  in range(len(values)):
            print(values[i])
        break



