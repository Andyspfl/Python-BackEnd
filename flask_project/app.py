from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3


app = Flask(__name__)
def get_db():
    db = sqlite3.connect("contacts.db")
    return db

app.secret_key = 'mysecretkey'

def add_bd(fullname, phone, email):
    conn = get_db()
    conn.execute(
    '''
        INSERT INTO CONTACTS(fullname, phone, email)
        VALUES (?,?,?)
    ''',(fullname,phone,email),
    )
    conn.commit()
    conn.close()

@app.route('/')
def Index():
    conn = get_db()
    cur = conn.execute('SELECT * FROM CONTACTS')
    return render_template("index.html", contacts = cur)

@app.route('/add' , methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        add_bd(fullname, phone,email)
        print(phone, fullname, email)
        flash('Contact added successfuly')
        return redirect(url_for("Index"))

@app.route('/edit/<id>')
def get_contact(id):
    conn = get_db()
    data =conn.execute('SELECT * FROM CONTACTS WHERE id = {0}'.format(id))
    data  = data.fetchall()
    return render_template("edit_contact.html", contact = data[0])
    
@app.route('/update/<id>' ,methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        conn = get_db()
        cursor = conn.execute("""
                            UPDATE CONTACTS SET fullname = ?,
                            phone = ?,
                            email = ?
                            WHERE id =?""", (fullname,phone,email,id))
        conn.commit()
        conn.close()
        flash('Contact updated Successfuly')
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>')
def delete_contact(id):
    conn = get_db()
    cur = conn.execute('DELETE FROM CONTACTS WHERE id = {0}'.format(id))
    conn.commit()
    flash('Contact delete successfuly')
    return redirect(url_for("Index"))


if __name__ == "__main__":
    app.run(port = 3000)
