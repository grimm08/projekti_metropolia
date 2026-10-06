from tietokanta import login, register, show_player, gamer_location, ensure_scores_table, connection, START_MONEY  
from geopy.distance import geodesic



PRICE_PER_KM = 0.10  #ticket price constant (km * 0.10)
POINTS_FOR_GOAL = 100  #base points when you reach the target country
POINTS_PER_STOP = 5  #5 points every stop
MIN_MONEY = 50 #minimum money for game over





def calc_score(stops, money_left):  #1 point per 100 EUR you still have
    return POINTS_FOR_GOAL + POINTS_PER_STOP * stops + int(money_left // 100)


def record_score(player_id, target, stops, spent, money_left, score, completed):  
    cur = connection.cursor()
    cur.execute("insert into scores (player_id, target_country, stops, money_spent, money_left, score, completed) "
                "values (%s, %s, %s, %s, %s, %s, %s)",
                (player_id, target, stops, round(spent, 2), round(money_left, 2), score, completed))
    connection.commit()
    cur.close()


def completed_rounds(player_id):  #counts only rounds won since the last reset, so a new game starts easy again
    cur = connection.cursor()
    cur.execute("select count(*) from scores where player_id = %s and completed = 1 "
                "and id > (select coalesce(max(id), 0) from scores where player_id = %s and target_country = 'RESET')",
                (player_id, player_id))
    n = cur.fetchone()[0]
    cur.close()
    return n


def show_scores(player_id):  #latest rounds
    cur = connection.cursor()
    print("\n===== TOP 5 PLAYERS =====")
    cur.execute("select username, points from players order by points desc limit 5")
    for i, (name, pts) in enumerate(cur.fetchall(), start=1):
        print(f"{i}. {name}: {pts} points")
    print("\n===== YOUR LAST 5 ROUNDS =====")
    cur.execute("select played_at, target_country, stops, money_spent, score, completed from scores "
                "where player_id = %s order by id desc limit 5", (player_id,))
    rows = cur.fetchall()
    if not rows:
        print("No rounds played yet.")
    for played_at, target, stops, spent, score, done in rows:
        if target == 'RESET':  
            print(f"{played_at:%Y-%m-%d %H:%M}  --- new game started ---")
            continue
        status = "reached" if done else "failed"
        print(f"{played_at:%Y-%m-%d %H:%M}  {target}: {status}, {stops} stop(s), spent {spent} EUR, score {score}")
    cur.close()


def cheapest_ticket(ident):  #price of the closest airport in ANOTHER country (the cheapest trip that is still possible)
    sql = ("select min(6371 * acos(least(1, greatest(-1, "
           "cos(radians(a.latitude_deg)) * cos(radians(b.latitude_deg)) * cos(radians(b.longitude_deg) - radians(a.longitude_deg)) "
           "+ sin(radians(a.latitude_deg)) * sin(radians(b.latitude_deg)))))) "
           "from airport a join airport b on b.iso_country != a.iso_country "
           "where a.ident = %s and b.type in ('large_airport', 'small_airport')")
    cur = connection.cursor()
    cur.execute(sql, (ident,))
    km = cur.fetchone()[0]
    cur.close()
    return float(km) * PRICE_PER_KM if km is not None else 0.0

class OutOfMoney(Exception):
    pass

def cheapest_to_country(from_ident, country):  # NEW: price of the cheapest flight from the current airport to the target country
    sql = ("select min(6371 * acos(least(1, greatest(-1, "
           "cos(radians(a.latitude_deg)) * cos(radians(b.latitude_deg)) * cos(radians(b.longitude_deg) - radians(a.longitude_deg)) "
           "+ sin(radians(a.latitude_deg)) * sin(radians(b.latitude_deg)))))) "
           "from airport a, airport b join country c on b.iso_country = c.iso_country "
           "where a.ident = %s and c.name = %s and b.type in ('large_airport', 'small_airport')")
    cur = connection.cursor()
    cur.execute(sql, (from_ident, country))
    km = cur.fetchone()[0]
    cur.close()
    return float(km) * PRICE_PER_KM if km is not None else 0.0

def game_over(player_id):  #True when money has run out or is not enough for any flight to another country
    money = get_money(player_id)
    return money <= 0 or money < cheapest_ticket(gamer_location(player_id))


def game_score(player_id):  # total score of the game that just ended (rounds since the last reset)
    cur = connection.cursor()
    cur.execute("select coalesce(sum(score), 0) from scores where player_id = %s "
                "and id > (select coalesce(max(id), 0) from scores where player_id = %s and target_country = 'RESET')",
                (player_id, player_id))
    total = cur.fetchone()[0]
    cur.close()
    return int(total)


def reset_player(player_id):  # Reset player data to default
    cur = connection.cursor()
    cur.execute("update players set money = %s, points = 0, current_airport = 'EFHK', country = 'Finland', "
                "iso_country = 'FI'"
                "where id = %s", (START_MONEY, player_id))
    connection.commit()
    cur.close()
    record_score(player_id, 'RESET', 0, 0, START_MONEY, 0, False)  


def rand_choice(start_ident):  #random choice 
   
    sql = ("select distinct country.name from country "
           "join airport on country.iso_country = airport.iso_country "
           "where airport.type in ('large_airport', 'small_airport') "
           "and country.iso_country != (select iso_country from airport where ident = %s) "
           "order by rand() limit 1;")
    crosri = connection.cursor()
    crosri.execute(sql, (start_ident,))
    values = crosri.fetchone()
    crosri.close()
    return values[0] if values else None


def check_name(country):  # checking the input (country name) is correct
    chk = "select iso_country from country where name = %s"  
    cur = connection.cursor() 
    cur.execute(chk, (country,))
    result = cur.fetchall()
    cur.close()
    return bool(result) 


def airport_list(place):  # getting the airports from a country
    sql_large = ("select airport.name, ident from airport join country on airport.iso_country = country.iso_country "
                 "where airport.type = 'large_airport' and country.name = %s order by airport.name;")  # CHANGED: order by name
    crosri = connection.cursor()
    crosri.execute(sql_large, (place,))
    values = crosri.fetchall()
    if not values:
        sql_small = ("select airport.name, ident from airport join country on airport.iso_country = country.iso_country "
                     "where airport.type = 'small_airport' and country.name = %s order by airport.name;")
        crosri.execute(sql_small, (place,))
        values = crosri.fetchall()
    crosri.close()  
    return {ident: name for name, ident in values}


def airport_locations(ident):  #locations from airports code
    sql = "select latitude_deg, longitude_deg from airport where ident = %s"
    crosri = connection.cursor()
    crosri.execute(sql, (ident,))
    row = crosri.fetchone()
    crosri.close()
    return (float(row[0]), float(row[1])) if row else None


def country_from_code(code):
    sql = ("select country.name, country.iso_country from country "
           "join airport on airport.iso_country = country.iso_country where airport.ident = %s")
    cur = connection.cursor()  
    cur.execute(sql, (code,))
    values = cur.fetchall()
    cur.close()  
    return values[0] if values else None  


def choose_airport(country):  
    airports = airport_list(country)
    if not airports:
        print("No suitable airports in that country.")
        return None
    print(f"Airports in {country}:")
    for ident, name in airports.items():
        print(f"  {ident}: {name}")
    while True:
        ident = input("Enter airport code: ").strip().upper()
        if ident in airports:
            return ident
        print("Invalid airport code, please try again.")


def ticket_price(from_ident, to_ident):  #calculate prices by km using geopy
    a = airport_locations(from_ident)
    b = airport_locations(to_ident)
    km = geodesic(a, b).km
    return km, km * PRICE_PER_KM


def get_money(player_id):  
    cur = connection.cursor()
    cur.execute("select money from players where id = %s", (player_id,))
    row = cur.fetchone()
    cur.close()
    return float(row[0])


def fly(player_id, from_ident, to_ident):  #charge the ticket and move the player in the database
    km, price = ticket_price(from_ident, to_ident)
    money = get_money(player_id)
    print(f"Distance {km:.0f} km, ticket price {price:.2f} EUR (you have {money:.2f} EUR)")
    if price > money:
        print("Not enough money for this flight.")
        raise OutOfMoney
    name, iso = country_from_code(to_ident)
    cur = connection.cursor()
    cur.execute("update players set money = money - %s, current_airport = %s, country = %s, iso_country = %s "
                "where id = %s", (round(price, 2), to_ident, name, iso, player_id))
    connection.commit()
    cur.close()
    return True


def add_points(player_id, amount):  # NEW
    cur = connection.cursor()
    cur.execute("update players set points = points + %s where id = %s", (amount, player_id))
    connection.commit()
    cur.close()


def finish_round(player_id, target, stops, money_start, reached):  #score the round and save it to the database
    money_left = get_money(player_id)
    spent = money_start - money_left
    score = calc_score(stops, money_left) if reached else 0  
    if reached:
        add_points(player_id, score)
        print(f"You reached {target}! Round score: {score} (spent {spent:.2f} EUR)")
    else:
        print("Round failed, score 0.")
    record_score(player_id, target, stops, spent, money_left, score, reached)
    return reached


def play_round(player_id):
    starts = gamer_location(player_id)
    print(f"Your current location is: {starts}")

    next_country = rand_choice(starts)
    if next_country is None:
        print("No destination found.")
        return
    print(f"Next country to fly to: {next_country}")

    if get_money(player_id) < cheapest_to_country(starts, next_country):
        print(f"You don't have enough money to fly to {next_country}.")
        return "GAME_OVER"

    stops = 1 + completed_rounds(player_id)
    money_start = get_money(player_id)
    print(f"Make {stops} stop(s) before reaching {next_country}")

    try:  # catches OutOfMoney raised by fly()
        for n in range(1, stops + 1):
            while True:
                trip = input(f"Stop {n}/{stops} - which country? ").strip()
                if check_name(trip):
                    break
                print("Invalid name, please try again")
            ident = choose_airport(trip)
            if ident is None:
                return finish_round(player_id, next_country, stops, money_start, False)
            fly(player_id, gamer_location(player_id), ident)

        print(f"Final leg: fly to {next_country}")
        ident = choose_airport(next_country)
        if ident is None:
            return finish_round(player_id, next_country, stops, money_start, False)
        fly(player_id, gamer_location(player_id), ident)
    except OutOfMoney:
        finish_round(player_id, next_country, stops, money_start, False)
        return "GAME_OVER"
    return finish_round(player_id, next_country, stops, money_start, True)


# ==================== main program ====================

cursor = connection.cursor()
PLAYER_COLUMNS = "id, username, money, points, current_airport, country, iso_country"  #column order for login and register

print("1. Login")
print("2. Register")
print("0. Exit")

choice = input("Enter your choice: ")

gamer = None

if choice == "1":
    gamer = login()
    if gamer:
        show_player(gamer[0])
    else:
        print("Login failed.")

elif choice == "2":
    while True:
        gamer_id = register()
        if gamer_id:
            cursor.execute(f"SELECT {PLAYER_COLUMNS} FROM players WHERE id = %s", (gamer_id,))
            gamer = cursor.fetchone()
            print(f"Registration successful. Welcome, {gamer[1]}!")
            show_player(gamer[0])
            break
        else:
            print("Registration failed. Please try again.")
elif choice == "0":
    print("Exiting the program.")

# the game will runs when login/register succeeded
if gamer:
    ensure_scores_table()
    print("Welcome to the Flight Game!")
    forced_over = False

    while True:
        if forced_over or game_over(gamer[0]):  #the game ends when money is gone or not enough to travel
            print("\n*** GAME OVER *** You don't have enough money to travel anywhere.")  
            print(f"Score of this game: {game_score(gamer[0])}")  
            show_player(gamer[0])
            show_scores(gamer[0])
            reset_player(gamer[0])  
            print(f"\nNew game started with {START_MONEY:.0f} EUR in Helsinki (EFHK).")
            show_player(gamer[0])
            continue
        print("\n1. play a round")
        print("2. show scores")
        print("3. reset player")
        print("0. exit")  
        choice = input("Enter your choice: ")
        if choice == "1":
            forced_over = play_round(gamer[0]) == "GAME OVER"
            play_round(gamer[0])
            show_player(gamer[0])
        elif choice == "2":
            show_scores(gamer[0])
        elif choice == "3":
            reset_player(gamer[0])
            print(f"\nnew game started with {START_MONEY:.0f} EUR in Helsinki (EFHK).")
            show_player(gamer[0])
        elif choice == "0":
            break
        else:
            print("Invalid choice.")

print("see you next time!")

cursor.close()
connection.close()
