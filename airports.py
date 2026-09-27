#this code  shows how many large airports in giving country

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
    chk = f"select iso_country from country where name = '{country}'"
    cursor = datastorage.cursor()
    cursor.execute(chk)
    result = cursor.fetchall()
    if  result:
        return True
    else:
        print("the is False")
        return False



while True:
    my_place = input("Enter country: ")
    if not check_name(my_place):
        print("Please enter a valid place")

    else:
        sql = f"select airport.name, ident from airport join country on airport.iso_country = country.iso_country where airport.type = 'large_airport' and country.name = '{my_place}' order by airport.iso_country;"
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

        for code, airport in flights.items():
            print( code, airport )

        break



