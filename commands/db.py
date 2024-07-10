import sqlite3
from datetime import datetime
import config as cfg
from bot import bot
from decimal import Decimal


conn = sqlite3.connect('users.db')
cursor = conn.cursor()


cursor.execute('''CREATE TABLE IF NOT EXISTS users (user_id INTEGER, name TEXT, balance TEXT, btc INTEGER, 
bank INTEGER, depozit INTEGER, timedepozit NUMERIC, exp INTEGER, energy INTEGER, case1 INTEGER, case2 INTEGER, 
case3 INTEGER, case4 INTEGER, rating INTEGER, games INTEGER, ecoins INTEGER, per TEXT, dregister NUMERIC, corn INTEGER,
status INTEGER, issued NUMERIC, ban NUMERIC, yen TEXT, perlimit TEXT)''')


cursor.execute('''CREATE TABLE IF NOT EXISTS mine (user_id INTEGER, iron INTEGER, gold INTEGER, diamond INTEGER, 
amestit INTEGER, aquamarine INTEGER, emeralds INTEGER, matter INTEGER, plasma INTEGER, nickel INTEGER, 
titanium INTEGER, cobalt INTEGER, ectoplasm INTEGER, biores INTEGER, palladium INTEGER)''')


cursor.execute('''CREATE TABLE IF NOT EXISTS ferma
                (user_id INTEGER, balance NUMERIC, nalogs INTEGER, cards INTEGER)''')


cursor.execute('''CREATE TABLE IF NOT EXISTS generator
                (user_id INTEGER, balance NUMERIC, nalogs INTEGER, turbine INTEGER)''')


cursor.execute('''CREATE TABLE IF NOT EXISTS garden
                (user_id INTEGER, balance NUMERIC, nalogs INTEGER, tree INTEGER, water INTEGER)''')


cursor.execute('''CREATE TABLE IF NOT EXISTS business (user_id INTEGER, balance NUMERIC, 
nalogs INTEGER, territory INTEGER, bsterritory INTEGER)''')


cursor.execute('''CREATE TABLE IF NOT EXISTS tree (user_id INTEGER, balance NUMERIC, 
nalogs INTEGER, territory INTEGER, tree INTEGER, yen INTEGER)''')


cursor.execute('''CREATE TABLE IF NOT EXISTS quarry (user_id INTEGER, balance NUMERIC, 
nalogs INTEGER, territory INTEGER, bur INTEGER, lvl INTEGER)''')


cursor.execute('''CREATE TABLE IF NOT EXISTS promo (name TEXT, summ TEXT, activ INTEGER, data TEXT)''')


cursor.execute('''CREATE TABLE IF NOT EXISTS promo_activ (user_id INTEGER, name TEXT)''')


cursor.execute('''CREATE TABLE IF NOT EXISTS sett (ads TEXT, kursbtc INTEGER)''')


cursor.execute('''CREATE TABLE IF NOT EXISTS wedlock
                (user1 INTEGER, user2 NUMERIC, rtime INTEGER)''')


cursor.execute('''CREATE TABLE IF NOT EXISTS clans
                (clan_id INTEGER PRIMARY KEY, balance TEXT, name TEXT, inv INT, kick INT, ranks INT, kazna INT,
                 robbery INT, war INT, upd_name INT, type INT, shield INT, ratting INT, win INT, lose INT)''')


cursor.execute('''CREATE TABLE IF NOT EXISTS clan
                (user_id INTEGER, clan_id INTEGER, rank INT)''')


cursor.execute('''CREATE TABLE IF NOT EXISTS chats (chat_id INTEGER, users INTEGER)''')
conn.commit()


cursor.execute('''CREATE TABLE IF NOT EXISTS property (user_id INTEGER, helicopter INTEGER, 
car INTEGER, yahta INTEGER, phone INTEGER, house INTEGER, plane INTEGER)''')


current_kurs = cursor.execute('SELECT kursbtc FROM sett').fetchone()
if current_kurs is None:
    cursor.execute('INSERT INTO sett (ads, kursbtc) VALUES (?, ?)', ('', 65000))


async def reg_user(user_id):
    ex = cursor.execute('SELECT name FROM users WHERE user_id = ?', (user_id,)).fetchone()
    if not ex:
        dt = int(datetime.now().timestamp())
        cursor.execute('INSERT INTO users (user_id, name, balance, btc, bank, depozit, timedepozit, exp, energy, case1,'
                       'case2, case3, case4, rating, games, ecoins, per, dregister, corn, status, yen, perlimit)'
                       'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                       (user_id, 'Игрок', cfg.start_money, 200, 0, 0, dt, 5000000, 10, 0, 0, 0, 0, 0, 0, 0, 0, dt, 0, 0, 0, 0))

        cursor.execute('INSERT INTO mine (user_id, iron, gold, diamond, amestit, aquamarine, emeralds, matter, plasma, '
                       'nickel, titanium, cobalt, ectoplasm, biores, palladium)'
                       ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                       (user_id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))

        cursor.execute('INSERT INTO property (user_id, helicopter, car, yahta, phone, house, plane) '
                       'VALUES (?, ?, ?, ?, ?, ?, ?)', (user_id, 0, 0, 0, 0, 0, 0))

        conn.commit()


async def getperevod(perevod, user_id, reply_user_id):
    balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
    r_balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (reply_user_id,)).fetchone()[0]
    per = cursor.execute('SELECT per FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]

    balance = int(Decimal(balance) - Decimal(perevod))
    r_balance = int(Decimal(r_balance) + Decimal(perevod))
    per = int(Decimal(per) + Decimal(perevod))

    cursor.execute(f'UPDATE users SET balance = ? WHERE user_id = ?', (str(balance), user_id))
    cursor.execute(f'UPDATE users SET balance = ? WHERE user_id = ?', (str(r_balance), reply_user_id))
    cursor.execute(f'UPDATE users SET per = ? WHERE user_id = ?', (str(per), user_id))
    conn.commit()


async def get_name(user_id):
    return cursor.execute('SELECT name FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]


async def getbalance(user_id):
    data = cursor.execute('SELECT name, balance, btc, bank, yen FROM users WHERE user_id = ?', (user_id,)).fetchone()
    return data[0], int(float(data[1])), data[2], data[3], int(data[4])


async def getpofildb(user_id):
    data = cursor.execute('SELECT balance, btc, bank, games, rating, yen, exp, dregister, ecoins, energy '
                          'FROM users WHERE user_id = ?', (user_id,)).fetchone()

    ferma = cursor.execute('SELECT user_id FROM ferma WHERE user_id = ?', (user_id,)).fetchone()
    business = cursor.execute('SELECT user_id FROM business WHERE user_id = ?', (user_id,)).fetchone()
    garden = cursor.execute('SELECT user_id FROM garden WHERE user_id = ?', (user_id,)).fetchone()
    generator = cursor.execute('SELECT user_id FROM generator WHERE user_id = ?', (user_id,)).fetchone()

    property = cursor.execute('SELECT * FROM property WHERE user_id = ?', (user_id,)).fetchone()

    return data, (ferma, business, garden, generator), property


async def get_balance(user_id):
    i = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
    return int(Decimal(i))


async def getlimitdb(message):
    user_id = message.from_user.id
    i = cursor.execute('SELECT per FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
    return int(i)


async def getads(message=None):
    ads = cursor.execute("SELECT ads FROM sett").fetchone()[0]
    ads = ads.replace(r'\n', '\n')
    return ads


async def setname(name, id):
    cursor.execute("UPDATE users SET name = ? WHERE user_id = ?", (name, id))
    conn.commit()


async def bonus_db(user_id, table, v, summ):
    if table == 'users' and v == 'balance':
        balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
        summ = Decimal(balance) + Decimal(summ)
        cursor.execute(f"UPDATE users SET balance = ? WHERE user_id = ?", (str(summ), user_id))
    else:
        cursor.execute(f"UPDATE {table} SET {v} = {v} + ? WHERE user_id = ?", (summ, user_id))
    conn.commit()


async def top_db(id, st, table='users'):
    cursor.execute(f"SELECT * FROM {table} ORDER BY CAST({st} AS REAL) DESC LIMIT 1000")
    top_players = cursor.fetchall()

    cursor.execute(f"SELECT * FROM {table} WHERE user_id = ?", (id,))
    userinfo = cursor.fetchone()
    return userinfo, top_players


async def top_clans_db(id):
    top_clans = cursor.execute(f"SELECT * FROM clans ORDER BY CAST(ratting AS REAL) DESC LIMIT 1000").fetchall()
    claninfo = cursor.execute(f"SELECT * FROM clan WHERE user_id = ?", (id,)).fetchone()
    return claninfo, top_clans


async def get_colvo_users():
    users = cursor.execute(f"SELECT COUNT(*) FROM users").fetchone()[0]
    chats = cursor.execute(f"SELECT COUNT(*) FROM chats").fetchone()[0]
    uchats = cursor.execute("SELECT SUM(users) FROM chats").fetchone()[0]
    return users, chats, uchats


async def getstatus(id):
    return cursor.execute(f"SELECT status FROM users WHERE user_id = ?", (id,)).fetchone()[0]


async def getban(id):
    return cursor.execute(f"SELECT ban FROM users WHERE user_id = ?", (id,)).fetchone()[0]


async def upd_chat_db(chat_id):
    res = cursor.execute(f"SELECT users FROM chats WHERE chat_id = ?", (chat_id,)).fetchone()
    if not res:
        cursor.execute('INSERT INTO chats (chat_id, users) VALUES (?, ?)', (chat_id, 0))
        conn.commit()
        res = 0
    else:
        res = res[0]

    count = await bot.get_chat_members_count(chat_id)
    if res != count:
        cursor.execute("UPDATE chats SET users = ? WHERE chat_id = ?", (count, chat_id))
        conn.commit()


async def url_name(user_id):
    name = cursor.execute('SELECT name FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
    return f'<a href="tg://user?id={user_id}">{name}</a>'


async def chek_user(user_id):
    return cursor.execute('SELECT user_id FROM users WHERE user_id = ?', (user_id,)).fetchone()


async def get_doplimit(user_id):
    return cursor.execute('SELECT perlimit FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]