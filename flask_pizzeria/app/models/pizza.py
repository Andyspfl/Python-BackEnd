import sqlite3
from app import app

def get_all_pizzas():
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO PIZZAS(name,description) VALUES(?,?)',("pizza rica","description"))
    cursor.execute('SELECT * FROM PIZZAS')
    pizzas = cursor.fetchall()
    conn.close()
    return pizzas
