import sqlite3
conn = sqlite3.connect("contacts.db")
conn.execute(
    '''
        CREATE TABLE CONTACTS (
        id INTEGER PRIMARY KEY,
        fullname VARCHAR(255) NOT NULL,
        phone INTEGER NOT NULL,
        email VARCHAR(255) NOT NULL
        );
    '''
)

conn.commit()
conn.close()