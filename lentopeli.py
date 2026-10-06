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

def ask_where():
    maa = input('Where?: ')
    if len(maa) < 1:
        print("No country given. Try again...")
        maa = ask_where()
    return maa

def rand_maa():
    kursori = yhteys.cursor(buffered=True)
    kursori.execute("select name from country where country.continent = 'EU' order by rand() limit 1")
    value = kursori.fetchone()[0]
    kursori.close()
    return value

def satunnainen_tapahtuma():
    print("You have encountered something...")
    valinta = input("Do you take the chance? Y/N: ")
    if valinta.lower() == "y" or valinta.lower() == "yes":
        chance = randrange(3)
        global rahat
        if chance == 0:
            print("You have been robbed. You lost all your money")
            rahat = 0
            return
        if chance == 1:
            rand_raha = randrange(20) + 10
            print("You did a good deed. You're rewarded for it.")
            print(f"You receive {rand_raha}€")
            rahat += rand_raha
            return
        if chance == 2:
            print("Nothing happened. You continue your journey.")
            return
    print("You continue your journey.")

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
    global arvauskerrat
    global kertoja_oikein
    global taso
    if arvauskerrat == kertoja_oikein + (taso * 3):
        taso += 1
        arvauskerrat = 0

rahat = 100
taso = 0
maksu = 10
arvauskerrat = 0
kertoja_oikein = 4

arvattava_paikka = rand_maa()
print(arvattava_paikka)
print(maan_sekoitus(arvattava_paikka))
print(maan_sekoitus(arvattava_paikka))
print(maan_sekoitus(arvattava_paikka))

maa = ask_where()
while rahat > 0:
    if maa.lower() == arvattava_paikka.lower():
        rahat = min(rahat + 10, 500)
        arvauskerrat += 1
        arvattava_paikka = rand_maa()
        print(arvattava_paikka)
        print(":D")
    else:
        print("D:")
        rahat -= 30
    levelup()
    maa = ask_where()
    if randrange(100) + 1 >= 50:
        satunnainen_tapahtuma()
print()
print(taso)