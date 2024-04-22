from flask import render_template
from app.models.pizza import get_all_pizzas

from app import app

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/order')
def order_pizza():
    pizzas = get_all_pizzas()
    return render_template('order.html', pizzas=pizzas)
