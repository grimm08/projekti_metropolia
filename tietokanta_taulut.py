import mysql.connector


# ==========================================
# YHTEYS TIETOKANTAAN
# ==========================================

connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="filmon",
    database="flight_game"
)

cursor = connection.cursor()


# ==========================================
# PELAAJATAULU
# ==========================================
# Luodaan players-taulu, jos sitä ei vielä ole. #
# players-taulu tallentaa pelaajan perustiedot:

cursor.execute("""
CREATE TABLE IF NOT EXISTS players (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    money DECIMAL(10,2) DEFAULT 1000.00,
    points INT DEFAULT 0,
    current_airport VARCHAR(10) DEFAULT 'EFHK'
)
""")

connection.commit()


# Tähän tauluun voidaan myöhemmin tallentaa
# pelaajan tekemät lennot.


cursor.execute("""
CREATE TABLE IF NOT EXISTS flight_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    player_id INT NOT NULL,
    departure_airport VARCHAR(10) NOT NULL,
    arrival_airport VARCHAR(10) NOT NULL,
    flight_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (player_id) REFERENCES players(id)
)
""")

connection.commit()



#######REKISTERÖINTI


def register():

    print("\n=== REGISTER ===")

    username = input("Anna käyttäjänimi: ")
    password = input("Anna salasana: ")

    #### Tarkistetaan löytyykö käyttäjä jo
    cursor.execute(
        "SELECT id FROM players WHERE username = %s",
        (username,)
    )

    existing_player = cursor.fetchone()

    if existing_player:
        print("Käyttäjänimi on jo käytössä.")
        return None

    ######## Uusi pelaaja #########

    cursor.execute("""
        INSERT INTO players
        (username, password, money, points, current_airport)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        username,
        password,
        1000,
        0,
        "EFHK"
    ))

    connection.commit()

    print("\nRekisteröinti onnistui!")
    print("Saat 1000 € aloitusrahaa.")

    return cursor.lastrowid



# LOGIN


def login():

    print("\n=== LOGIN ===")

    username = input("Käyttäjänimi: ")
    password = input("Salasana: ")

    cursor.execute("""
        SELECT id, username, password, money, points, current_airport
        FROM players
        WHERE username = %s AND password = %s
    """, (username, password))

    player = cursor.fetchone()

    if player is None:
        print("Väärä käyttäjänimi tai salasana.")
        return None

    print("\nTervetuloa takaisin,", player[1] + "!")

    return player



# PELAAJAN TIEDOT


def show_player(player_id):

    cursor.execute("""
        SELECT username, money, points, current_airport
        FROM players
        WHERE id = %s
    """, (player_id,))

    player = cursor.fetchone()

    print("\n==========================")
    print("      PELAAJAN TIEDOT")
    print("==========================")
    print("Nimi:", player[0])
    print("Rahaa:", player[1], "€")
    print("Pisteet:", player[2])
    print("Nykyinen lentokenttä:", player[3],"Helsinki")
    print("==========================")



# PÄÄOHJELMA


print("==========================")
print("       FLIGHT GAME")
print("==========================")

while True:
    print("==>Valitse mistä aloittaa<==")
    print("\n1. Register")
    print("2. Login")
    print("3. Lopeta")

    choice = input("Valitse: ")

    if choice == "1":

        player_id = register()

        if player_id is not None:
            show_player(player_id)
            break

    elif choice == "2":

        player = login()

        if player is not None:
            player_id = player[0]
            show_player(player_id)
            break

    elif choice == "3":

        print("Peli lopetetaan.")
        break

    else:
        print("Virheellinen valinta.")



# SULJETAAN YHTEYS..


cursor.close()
connection.close()