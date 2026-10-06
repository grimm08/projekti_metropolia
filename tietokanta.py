import mysql.connector
import pwinput

# ==========================================
# YHTEYS TIETOKANTAAN
# ==========================================

connection = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="ak08mh77",
    database="flight_game"
)

cursor = connection.cursor()

START_MONEY = 15000.00  # one place for the starting money (used by register and by the game reset)


# ==========================================
# PELAAJATAULU
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS players (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    money DECIMAL(10,2) DEFAULT 15000.00,
    points INT DEFAULT 0,
    current_airport VARCHAR(10) DEFAULT 'EFHK',
    country VARCHAR(50) DEFAULT 'Finland',
    iso_country VARCHAR(10) DEFAULT 'FI',
    foreign key (current_airport) references airport(ident),
    foreign key (iso_country) references country(iso_country)
);
""")

connection.commit()



# REKISTERÖINTI


def register():

    print("\n=== REGISTER ===")

    username = input("Anna käyttäjänimi: ")
    password = pwinput.pwinput("Anna salasana: ")

    # Tarkistetaan löytyykö käyttäjä jo
    cursor.execute(
        "SELECT id FROM players WHERE username = %s",
        (username,)
    )

    existing_player = cursor.fetchone()

    if existing_player:
        print("Käyttäjänimi on jo käytössä.")
        return None

    # Uusi pelaaja
    cursor.execute("""
        INSERT INTO players
        (username, password, money, points, current_airport, country, iso_country)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        username,
        password,
        START_MONEY,  
        0,
        "EFHK",
        "Finland",
        "FI"
    ))

    connection.commit()

    print("\nRekisteröinti onnistui!")
    print("Saat 15000 € aloitusrahaa.")

    return cursor.lastrowid



# LOGIN


def login():

    print("\n=== LOGIN ===")

    username = input("Käyttäjänimi: ")
    password = pwinput.pwinput("Salasana: ")

    cursor.execute("""
        SELECT id, username, money, points, current_airport, country, iso_country
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
        SELECT username, money, points, current_airport, country, iso_country
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
    print("Nykyinen lentokenttä:", player[3])
    print("Maa:", player[4])
    print("ISO-koodi:", player[5])
    print("==========================")
    
    
def gamer_location(player_id):
    cursor.execute("""
        SELECT current_airport FROM players WHERE id = %s
    """, (player_id,))

    location = cursor.fetchone()
    return location[0] if location else None

def ensure_scores_table():  #score table
    cur = connection.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            id INT AUTO_INCREMENT PRIMARY KEY,
            player_id INT NOT NULL,
            target_country VARCHAR(50) NOT NULL,
            stops INT NOT NULL,
            money_spent DECIMAL(10,2) NOT NULL,
            money_left DECIMAL(10,2) NOT NULL,
            score INT NOT NULL,
            completed BOOLEAN NOT NULL,
            played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (player_id) REFERENCES players(id)
        );
    """)
    connection.commit()
    cur.close()
    
# PÄÄOHJELMA


if __name__ == "__main__":
    print("==========================")
    print("       FLIGHT GAME")
    print("==========================")

    while True:
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

    cursor.close()
    connection.close()