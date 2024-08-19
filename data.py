import sqlite3

def create_table():
    con = sqlite3.connect("data.db")
    cur = con.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS users(
        id TEXT PRIMARY KEY,
        name TEXT,
        role TEXT,
        gender TEXT,
        status TEXT)''')

    con.commit()
    con.close()

def user():
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    cur.execute('SELECT * FROM users')
    USERS = cur.fetchall()
    con.close()
    return USERS

def iinsert(id, name, role, gender, status):
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    cur.execute('INSERT INTO users(id, name, role, gender, status) VALUES (?, ?, ?, ?, ?)',
                (id, name, role, gender, status))
    con.commit()
    con.close()

def idExists(id):
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    cur.execute('SELECT * FROM users WHERE id = ?', (id,))
    res = cur.fetchone()
    con.close()
    if res is not None:
        return res[0]
    else:
        return False

def delUser(id):
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    cur.execute('DELETE FROM users WHERE id = ?', (id,))
    con.commit()
    con.close()

def update_user(id, newName, newRole, newGender, newStatus):
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    cur.execute('UPDATE users SET name = ?, role = ?, gender = ?, status = ? WHERE id = ?', (newName, newRole, newGender, newStatus, id))
    con.commit()
    con.close()

create_table()