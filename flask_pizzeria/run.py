from app import app
from app.models.create_pizza_bd import crete_db_if_not_exists


if __name__ == '__main__':
    crete_db_if_not_exists()
    app.run(debug=True)



