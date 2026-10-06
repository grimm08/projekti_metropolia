import mysql.connector
from random import randrange

yhteys = mysql.connector.connect(
    host='127.0.0.1',
    port= 3306,
    database='lentopeli',
    user='kayttaja1',
    password='Munpiha',
    autocommit=True,
    collation='utf8mb4_general_ci'
    )

def kysy_maata():
    maa = input('Where?: ')
    if len(maa) < 1:
        print("No country given. Try again...")
        maa = kysy_maata()
    return maa

def rand_maa():
    kursori = yhteys.cursor(buffered=True)
    kursori.execute("select name from country where country.continent = 'EU' order by rand() limit 1")
    value = kursori.fetchone()[0]
    kursori.close()
    return value

def maan_sijainti(haettava_maa):
    kursori = yhteys.cursor(buffered=True)
    kursori.execute(f"select latitude_deg, longitude_deg from airport "
                    f"inner join country on country.iso_country = airport.iso_country "
                    f"where country.name = '{haettava_maa}' "
                    f"order by rand() limit 1")
    value = kursori.fetchone()
    kursori.close()
    return value

def maan_sekoitus(haettava_maa):
    peitetty_maa = ""
    for i in range(len(haettava_maa)):
        if randrange(len(haettava_maa)) >= len(haettava_maa) // 3 * 2:
           if i % (randrange(2) + 1) == 0 and haettava_maa[i] != " ":
               peitetty_maa += "*"
           else:
               peitetty_maa += haettava_maa[i]
        else:
            peitetty_maa += haettava_maa[i]
    return peitetty_maa

def levelup():
    if arvauskerrat == kertoja_oikein + (taso * 3):
        taso += 1
        arvauskerrat = 0

rahat = 100
taso = 0
maksu = 10
arvauskerrat = 0
kertoja_oikein = 4

arvattava_maa = rand_maa()
print(arvattava_maa)
print(maan_sekoitus(arvattava_maa))
print(maan_sekoitus(arvattava_maa))
print(maan_sekoitus(arvattava_maa))



maa = kysy_maata()
while rahat > 0:
    if maa.lower() == arvattava_maa.lower():
        rahat = min(rahat + 10, 500)
        arvauskerrat += 1
        arvattava_maa = rand_maa()
        print(maan_sijainti(arvattava_maa))
        print(arvattava_maa)
        print(":D")
    else:
        print("D:")
        rahat -= 30
    levelup()
    maa = kysy_maata()
print()
print(taso)