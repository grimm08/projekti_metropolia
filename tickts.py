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

def check_name(country):
    chk = f"select iso_country from country where iso_country = '{country}'"
    cursor = datastorage.cursor()
    cursor.execute(chk)
    result = cursor.fetchall()
    if not result:
        return False
    else:
        return True

def ticket_price(xlat,xlot, ylat,ylot):
    dis = geodesic(xlat,xlot,ylat,ylot).km
    ticket_price = dis * 0.50
    return ticket_price

def airport_list(place):
    sql = (f"select airport.name, ident from airport join country on airport.iso_country = country.iso_country where "
           f"airport.type = 'large_airport' and country.name = '{place}' order by airport.iso_country;")
    crosri = datastorage.cursor()
    crosri.execute(sql)
    values = crosri.fetchall()
    places = []
    codes = []
    for i  in range(len(values)):
        places.append(values[i][0])

    for j in range(len(values)):
        codes.append(values[j][1])

    flights = dict(zip(codes, places))
    return flights

while True:
    first = input("where are you?  ").lower()
    todis = input("where you want to go?  ").lower()

    if not check_name(first) and not check_name(todis):
        codes = airport_list(todis)
        for code, airport in codes.items():
            print(f"{code}: {airport}")


        break
    else:
        print("Please enter a valid name")
