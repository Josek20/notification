import sqlite3
import datetime
date = datetime.date.today()
day = date.strftime("%d")
# print(type(day))
db = sqlite3.connect('database.db')
c = db.cursor()

# c.execute("""CREATE TABLE last_date (
#         todaty_is integer
# )""")

# print(type(c.execute("SELECT * FROM last_date").fetchall()[-1][0]))

# c.execute("""CREATE TABLE things_to_watch (
#         name text,
#         episode_number integer,
#         website text,
#         new text
# )""")

def receive_anm(dct):
    with db:
        c.execute("SELECT * FROM things_to_watch WHERE website='darkanime.stream'")
        for i in c.fetchall():
            dct[i[0]] = list(i[1:])

    print(dct)
    return dct


def receive_ytb(dct):
    with db:
        c.execute("SELECT * FROM things_to_watch") #WHERE website='www.youtube.com/channel/UCDK9qD5DAQML-pzrtA7A4oA'")
        for i in c.fetchall():
            if 'youtube' in i[2]:
                dct[i[0]] = list(i[1:])
    return dct


def write_to(lst):
    with db:
        c.execute("INSERT INTO things_to_watch VALUES('{}','{}','{}','{}')".format(lst[0],lst[1],lst[2],lst[3]))


def update_db(dc):
    with db:
        for i in dc.keys():
            c.execute("UPDATE things_to_watch SET episode_number = {},new = '{}' WHERE name = '{}'".format(dc[i][0],dc[i][-1],i))


# with db:
#     c.execute("UPDATE things_to_watch SET new = 'True\n' WHERE name = 'Uzaki-chan wa Asobitai!'")