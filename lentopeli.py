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

rahat = 100
taso = 0

def kysy_maata():
    maa = input('Where?: ')
    if len(maa) < 1:
        print("No country given. Try again...")
        maa = kysy_maata()
    return maa

def rand_maa():
    kursori = yhteys.cursor(buffered=True)
    kursori.execute("select distinct name from country order by rand() limit 1")
    value = kursori.fetchone()[0]
    kursori.close()
    return value
    pass

arvattava_maa = rand_maa()
print(arvattava_maa)

maa = kysy_maata()
while rahat > 0:
    if maa.lower() == arvattava_maa.lower():
        rahat += 10
        arvattava_maa = rand_maa()
        print(arvattava_maa)
        print(":D")
    else:
        print("D:")
        rahat -= 30
    maa = kysy_maata()