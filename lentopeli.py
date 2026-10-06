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
    maa = input('Do you know where you are?: ')
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

def info_teksti(nimi):
    chance = randrange(3)
    if chance == 0:
        print(f"You travel through big and small towns in {nimi}.")
        return
    if chance == 1:
        print(f"You look at the great monuments of {nimi}. They are marvelous.")
        return
    if chance == 2:
        print(f"You enjoy the food {nimi} offers.")
        return

def oikea_vastaus(nimi, raha):
    chance = randrange(3)
    if chance == 0:
        print(f"Correct! You are indeed in {nimi}!")
        return
    if chance == 1:
        print(f"Yes! {nimi} is where you are currently.")
        return
    if chance == 2:
        print(f"Good job! I knew you knew you were in {nimi} the whole time.")
        return
    print(f"You receive {raha}€")

def vaara_vastaus(nimi, raha):
    chance = randrange(3)
    if chance == 0:
        print(f"Wrong. You are actually in {nimi}.")
        return
    if chance == 1:
        print(f"Oh dear! {nimi} was the correct answer.")
        return
    if chance == 2:
        print(f"No no, {nimi} is the correct answer.")
        return
    print(f"You lose {raha}€")

def satunnainen_tapahtuma():
    print("You have encountered something...")
    valinta = input("Do you take the chance? Y/N: ")
    if valinta.lower() == "y" or valinta.lower() == "yes":
        chance = randrange(3)
        global rahat
        if chance == 0:
            print("You have been robbed. You lost all your money.")
            rahat = 0
            return
        if chance == 1:
            rand_raha = randrange(40) + 10
            print("You did a good deed. You're rewarded for it.")
            print(f"You receive {rand_raha}€")
            rahat += rand_raha
            return
        if chance == 2:
            print("Nothing happened. You continue your journey.")
            return
    print("You continue your journey.")

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

info_teksti(maan_sekoitus(arvattava_paikka))
maa = kysy_maata()
while rahat > 0:
    if maa.lower() == arvattava_paikka.lower():
        saatava_raha = 10
        oikea_vastaus(arvattava_paikka, saatava_raha)
        rahat = min(rahat + saatava_raha, 500)
        arvauskerrat += 1
        arvattava_paikka = rand_maa()
    else:
        menetettava_raha = 30
        vaara_vastaus(arvattava_paikka, menetettava_raha)
        rahat -= menetettava_raha
        arvattava_paikka = rand_maa()
    levelup()
    print()
    if randrange(100) + 1 >= 80:
        satunnainen_tapahtuma()
    info_teksti(maan_sekoitus(arvattava_paikka))
    maa = kysy_maata()

print()
print("You have run out of money to travel")
print(f"Your level: {taso}")