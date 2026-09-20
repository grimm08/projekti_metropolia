import mysql.connector
datastorage = mysql.connector.connect(
    host='127.0.0.1',
    port= 3306,
    database= 'a_game',
    user= 'root',
    password= 'ak08mh77',
    autocommit= True
)


def name_checker(user):
    chk = f"select * from a_player where username = '{user}'"
    crsori = datastorage.cursor()
    crsori.execute(chk)
    outcome = crsori.fetchall()
    print(outcome)
    return outcome




def name_add(name, pas, place):
    addcrsori = datastorage.cursor()
    sql = f"INSERT INTO a_player (username, pin, a_location) VALUES (%s, %s, %s)"
    val = (name, pas, place)
    addcrsori.execute(sql, val)
    datastorage.commit()
    print(addcrsori.rowcount)
    print(f"user {name} from {place} has been add")
    return


while True:
    print("1. New user")
    print("2. Existing user")
    print("0. Exit")
    choice = input("input the number of your choice:\n")
    if choice == '0':
        print("see you soon!")
        break
    elif choice =='1':
        uname = input("create username:")
        chkr = name_checker(uname)
        if not chkr:
            psw = input("create pin of four digit:")
            if len(psw) != 4:
                print("your pin should in 4 digits")
                continue
            else:
                la = input("inter your country:")
            name_add(uname, psw, la)
            break




