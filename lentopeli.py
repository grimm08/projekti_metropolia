import mysql.connector

yhteys = mysql.connector.connect(
    host='127.0.0.1',
    port= 3306,
    database='lentopeli',
    user='kayttaja1',
    password='Munpiha',
    autocommit=True,
    collation='utf8mb4_general_ci'
    )

koodi = input("Anna ICAO-koodi: ")
kursori = yhteys.cursor()
#kursori.execute(f"select name, municipality from airport where ident = '{koodi}'")

tulos = kursori.fetchall()[0]
print(f"\nKenttä: {tulos[0]}\nPaikkakunta: {tulos[1]}")

luku = input('Anna luku: ')
while luku != "":
    if float(luku) < pienin:
        pienin = float(luku)
    elif float(luku) > suurin:
        suurin = float(luku)
    luku = input('Anna luku: ')