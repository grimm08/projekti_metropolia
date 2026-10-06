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

def kysy_maata():
    maa = input('Where?: ')
    if len(maa) < 1:
        print("No country given. Try again...")
        maa = kysy_maata()
    return maa

def rand_maa():
    kursori = yhteys.cursor(buffered=True)
    kursori.execute("select distinct name from country where name is not null order by rand() limit 1")
    value = kursori.fetchone()[0]
    kursori.close()
    return value

def levelup():
    global arvauskerrat
    #global kertoja_oikein
    global taso
    if arvauskerrat == kertoja_oikein * (taso + 1):
        taso += 1
        arvauskerrat = 0

rahat = 100
taso = 0
arvauskerrat = 0
kertoja_oikein = 4

arvattava_maa = rand_maa()
print(arvattava_maa)

maa = kysy_maata()
while rahat > 0:
    if maa.lower() == arvattava_maa.lower():
        rahat += 10
        arvauskerrat += 1
        arvattava_maa = rand_maa()
        print(arvattava_maa)
        print(":D")
    else:
        print("D:")
        rahat -= 30
    levelup()
    maa = kysy_maata()

print(taso)