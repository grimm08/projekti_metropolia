#part of the game where asking about player location and the player distinction
#also the ticket prices
#the code not ready, it works as it is.

from geopy.distance import geodesic
import mysql.connector
from tietokanta1 import gamer_location, login, register


datastorage = mysql.connector.connect(
    host='127.0.0.1',
    port= 3306,
    database= 'flight_game',
    user= 'root',
    password= 'ak08mh77',
    autocommit= True
)

def check_name(country):            #checking the input (country name) is correct
    chk = f"select iso_country from country where name = '{country}'"
    cursor = datastorage.cursor()
    cursor.execute(chk)
    result = cursor.fetchall()
    cursor.close()
    if result:
        return True
    else:
        return False

def ticket_price(x,y):     #price calculation based on the distance between two airports
    dis = geodesic(x,y).km
    price = dis * 0.10
    return price

def rand_choice(starts): #random choise to next country.
    next_location = (f"select country.name from country join airport on  country.iso_country = airport.iso_country "
                     f"where airport.ident != %s order by rand() limit 1;")
    crosri = datastorage.cursor()
    crosri.execute(next_location, (starts,))
    values = crosri.fetchone()
    crosri.close()
    return values[0]

def airport_list(place):
    sql_large = (f"select airport.name, ident from airport join country on airport.iso_country = country.iso_country where "
           f"airport.type = 'large_airport' and country.name = '{place}' order by airport.iso_country;")
    crosri = datastorage.cursor()
    crosri.execute(sql_large)
    values = crosri.fetchall()
    if not values:
        sql_small = (f"select airport.name, ident from airport join country on airport.iso_country = country.iso_country "
                     f"where airport.type = 'small_airport' and country.name = '{place}' order by airport.iso_country;")
        crosri.execute(sql_small)
        values = crosri.fetchall()
    places = []
    codes = []
    for i  in range(len(values)):
        places.append(values[i][0])

    for j in range(len(values)):
        codes.append(values[j][1])

    flights = dict(zip(codes, places))
    return flights

def airport_locations(airport_code): #pulling out locations
    gps_airport = f"select latitude_deg, longitude_deg from airport where ident = %s"
    crosri = datastorage.cursor()
    crosri.execute(gps_airport, (airport_code,))
    values = crosri.fetchall()
    crosri.close()
    return values
def get_country_airport(iso_code):
    sql = f"select ident, name from airport where iso_country = %s and type in ('large_airport', 'small_airport')"
    cursor = datastorage.cursor()
    cursor.execute(sql, (iso_code,))
    airports = dict(cursor.fetchall())
    cursor.close()
    return airports

def game_data(game_id):
    sql = f"select * from players where id = {game_id}"
    cursor = datastorage.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return result

def player_location(player_id):
    sql = f"select country from players join country on players.iso_country = country.iso_country where players.id = {player_id}"
    cursor = datastorage.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return result

def player_id(player_id):
    sql = f"select id from players where id = {player_id}"
    cursor = datastorage.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    locate = player_location(result[0][0])
    
    return locate

print("Welcome to the flight game!")
print("1. login")
print("2. register")
print("0. Exit")
choice = input("Enter your choice: ")
if choice == "1":
    player_id = login()
elif choice == "2":
    player_id = register()
elif choice == "0":
    print("Exiting the game. Goodbye!")
    exit()

first = None
print("Welcome to the flight game!")
print("1. Start the game")
print("0. Exit")
choice = input("Enter your choice: ")
    
while choice != "0":           
        while True:
            
            first = gamer_location(player_id)  # Assuming game_id is available
            final = input("where you want to go?  ").lower()

            if check_name(final):
                codes = airport_list(final)

                if len(codes) > 1: #dictionary for distinction country
                    for code, airport in codes.items():
                        print(f"{code}: {airport}")
                    airport_choise2 = input("\nwhat airport are you to go(entre airport code)?  ").upper()
                    print(f"you're going to {codes[airport_choise2]}")
                else:
                    airport_choise2, airport_name = next(iter(codes.items()))
                    print(f"you're going to {airport_name}")
                break

            else:
                print("Please enter a valid name")
        loc1 = first
        loc2 = airport_locations(airport_choise2)

        print(f"{ticket_price(loc1,loc2):.2f}€")

        next_location = rand_choice(airport_choise2)
        print(f"next destination: {next_location}")
        print("countentue to play or exit the game (y/n)")
        continue_choice = input().lower()
        if continue_choice == "n":
            break
        
print("Exiting the game. Goodbye!")