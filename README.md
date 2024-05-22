```python
#usuarios app web__________________
#controllers/book_controller.py______________________________________________________
from flask import Blueprint, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models.book_model import Book
from views import book_view

# Importamos el decorador de roles
from utils.decorators import role_required

book_bp = Blueprint("book", __name__)


@book_bp.route("/books")
@login_required
@role_required(roles=["admin","user"])
def list_books():
    books = Book.get_all()
    return book_view.list_books(books)


@book_bp.route("/books/create", methods=["GET", "POST"])
@login_required
@role_required(roles=["admin"])
def create_book():
    if request.method == "POST":
        if current_user.has_role("admin"):
            title = request.form["title"]
            author = request.form["author"]
            edition = request.form["edition"]
            availability = request.form["availability"]
            book = Book(title=title, author=author, edition=edition, availability=availability)
            book.save()
            flash("Libro creado exitosamente", "success")
            return redirect(url_for("book.list_books"))
        else:
            return jsonify({"message": "Unauthorized"}), 403
    return book_view.create_book()


@book_bp.route("/books/<int:id>/update", methods=["GET", "POST"])
@login_required
@role_required(roles=["admin"])
def update_book(id):
    book = Book.get_by_id(id)
    if not book:
        return "Libro no encontrado", 404
    if request.method == "POST":
        if current_user.has_role("admin"):
            title = request.form["title"]
            author = request.form["author"]
            edition = request.form["edition"]
            availability = request.form["availability"]
            book.update(title=title, author=author, edition=edition, availability=availability)
            flash("Libro actualizado exitosamente", "success")
            return redirect(url_for("book.list_books"))
        else:
            return jsonify({"message": "Unauthorized"}), 403
    return book_view.update_book(book)


@book_bp.route("/books/<int:id>/delete")
@login_required
@role_required(roles=["admin"])
def delete_book(id):
    book = Book.get_by_id(id)
    if not book:
        return "Libro no encontrado", 404
    if current_user.has_role("admin"):
        book.delete()
        flash("Libro eliminado exitosamente", "success")
        return redirect(url_for("book.list_books"))
    else:
        return jsonify({"message": "Unauthorized"}), 403
#models/book_model.py_____________________________________________
from database import db

# Define la clase `Book` que hereda de `db.Model`
# `Book` representa la tabla `books` en la base de datos
class Book(db.Model):
    __tablename__ = "books"

    # Define las columnas de la tabla `books`
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    edition = db.Column(db.String(100), nullable=False)
    availability = db.Column(db.String(100), nullable=False)

    # Inicializa la clase `Book`
    def __init__(self, title, author, edition, availability):
        self.title = title
        self.author = author
        self.edition = edition
        self.availability = availability

    # Guarda un libro en la base de datos
    def save(self):
        db.session.add(self)
        db.session.commit()

    # Obtiene todos los libros de la base de datos
    @staticmethod
    def get_all():
        return Book.query.all()

    # Obtiene un libro por su ID
    @staticmethod
    def get_by_id(id):
        return Book.query.get(id)

    # Actualiza un libro en la base de datos
    def update(self, title=None, author=None, edition=None, availability=None):
        if title is not None:
            self.title = title
        if author is not None:
            self.author = author
        if edition is not None:
            self.edition = edition
        if availability is not None:
            self.availability = availability
        db.session.commit()

    # Elimina un libro de la base de datos
    def delete(self):
        db.session.delete(self)
        db.session.commit()
#views/book_view.py________________________
from flask import render_template
from flask_login import current_user


# La función `list_books` recibe una lista de
# libros y renderiza el template `books.html`
def list_books(books):
    return render_template(
        "books.html",
        books=books,
        title="Lista de libros",
        current_user=current_user,
    )


# La función `create_book` renderiza el
# template `create_book.html` o devuelve un JSON
# según la solicitud
def create_book():
    return render_template(
        "create_book.html", title="Crear Libro", current_user=current_user
    )


# La función `update_book` recibe un libro
# y renderiza el template `update_book.html`
def update_book(book):
    return render_template(
        "update_book.html",
        title="Editar Libro",
        book=book,
        current_user=current_user,
    )
#controllers/user_controller.py___________________
from flask import Blueprint, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash

# Importamos el decorador de roles
from utils.decorators import role_required

# Importamos la vista de usuarios
from views import user_view

# Importamos el modelo de usuario
from models.user_model import User

# Un Blueprint es un objeto que agrupa
# rutas y vistas
user_bp = Blueprint("user", __name__)


# Ruta de la página raíz redirige a
# la página de inicio de sesión
@user_bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("user.profile", id=current_user.id))
    return redirect(url_for("user.login"))


@user_bp.route("/users")
@login_required
def list_users():
    # Obtenemos todos los usuarios
    users = User.get_all()
    # Llamamos a la vista de usuarios
    return user_view.usuarios(users)


# Definimos la ruta "/users" asociada a la función registro
# que nos devuelve la vista de registro
@user_bp.route("/users/create", methods=["GET", "POST"])
def create_user():
    if request.method == "POST":
        # Obtenemos los datos del formulario
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("El nombre de usuario ya está en uso", "error")
            return redirect(url_for("user.create_user"))
        # Creamos un nuevo usuario
        user = User(first_name, last_name, username, password, role=role)
        user.set_password(password)
        # Guardamos el usuario
        user.save()
        flash("Usuario registrado exitosamente", "success")
        return redirect(url_for("user.list_users"))
    # Llamamos a la vista de registro
    return user_view.registro()


# Actualizamos la información del usuario por su id
# Ya estamos en la vista de actualizar
# por lo que obtenemos los datos del formulario
# y actualizamos la información del usuario
@user_bp.route("/users/<int:id>/update", methods=["GET", "POST"])
@login_required
@role_required(roles=["admin"])
def update_user(id):
    user = User.get_by_id(id)
    if not user:
        return "Usuario no encontrado", 404
    if request.method == "POST":
        # Obtenemos los datos del formulario
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        # Actualizamos los datos del usuario
        user.first_name = first_name
        user.last_name = last_name
        # Guardamos los cambios
        user.update()
        return redirect(url_for("user.list_users"))
    return user_view.actualizar(user)


@user_bp.route("/users/<int:id>/delete")
@login_required
@role_required(roles=["admin"])
def delete_user(id):
    user = User.get_by_id(id)
    if not user:
        return "Usuario no encontrado", 404
    user.delete()
    return redirect(url_for("user.list_users"))


# Ruta para el inicio de sesión
@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.get_user_by_username(username)
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash("Inicio de sesión exitoso", "success")
            if user.has_role("admin"):
                # Redirigir a su perfil si el usuario es de rol "admin"
                return redirect(url_for("user.list_users"))
            else:
                # Redirigir a la lista de usuarios para otros roles
                return redirect(url_for("user.profile", id=user.id))
        else:
            flash("Nombre de usuario o contraseña incorrectos", "error")
    return user_view.login()


# Ruta para cerrar sesión
@user_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada exitosamente", "success")
    return redirect(url_for("user.login"))


@user_bp.route("/profile/<int:id>")
@login_required
def profile(id):
    user = User.get_by_id(id)
    return user_view.perfil(user)
#models/user_model.py________________________
from database import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


# `db.Model` es una clase base para todos los modelos de SQLAlchemy
# Define la clase `User` que hereda de `db.Model`
# `User` representa la tabla `users` en la base de datos
class User(UserMixin, db.Model):
    __tablename__ = "users"
    # Define las columnas de la tabla `users`
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(50), nullable=False, default="user")

    # Inicializa la clase `User`
    def __init__(self, first_name, last_name, username, password, role="user"):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.set_password(password)
        self.role = role

    # Genera un hash seguro de la contraseña
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Guarda un usuario en la base de datos
    def save(self):
        db.session.add(self)
        db.session.commit()

    # Obtiene todos los usuarios de la base de datos
    @staticmethod
    def get_all():
        return User.query.all()

    # Obtiene un usuario por su id
    @staticmethod
    def get_by_id(id):
        return User.query.get(id)

    # Actualiza un usuario en la base de datos
    def update(self):
        db.session.commit()

    # Elimina un usuario de la base de datos
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    # Obtiene un usuario por su nombre de usuario
    @staticmethod
    def get_user_by_username(username):
        return User.query.filter_by(username=username).first()

    def has_role(self, role):
        return self.role == role
#views/user_view.py_________________________
# render_template() es una función de Flask
# que renderiza un template de Jinja2.
from flask import render_template
from flask_login import current_user


# La función `usuarios` recibe una lista de
# usuarios y renderiza el template `usuarios.html`
def usuarios(users):
    return render_template(
        "usuarios.html",
        users=users,
        title="Lista de usuarios",
        current_user=current_user,
    )


# La función `registro` renderiza el
# template `registro.html`
def registro():
    return render_template(
        "registro.html", title="Registro de usuarios", current_user=current_user
    )


# La función `actualizar` recibe un usuario
# y renderiza el template `actualizar.html`
def actualizar(user):
    return render_template(
        "actualizar.html",
        title="Actualizar usuario",
        user=user,
        current_user=current_user,
    )


# La función `login` renderiza el template `login.html`
def login():
    return render_template(
        "login.html", title="Inicio de sesión", current_user=current_user
    )


# La función `perfil` renderiza el template `perfil.html`
def perfil(user):
    return render_template(
        "profile.html", title="Perfil de usuario", current_user=current_user, user=user
    )
#database.py__________________________
from flask_sqlalchemy import SQLAlchemy

# Crea una instancia de `SQLAlchemy`
db = SQLAlchemy()
#run.py_______________________________
from flask import Flask
from flask_login import LoginManager

# Importamos el controlador de usuarios
from controllers import user_controller

# Importamos el controlador de libros
from controllers import book_controller

# Importamos la base de datos
from database import db
from models.user_model import User

# Inicializa la aplicación Flask
app = Flask(__name__)
# Configuración de la base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///library.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "clave-secreta"
# Configuración de Flask-Login
login_manager = LoginManager()
# Especifica la ruta de inicio de sesión
login_manager.login_view = "user.login"
login_manager.init_app(app)


# Función para cargar un usuario basado en su ID
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Inicializa `db` con la aplicación Flask
db.init_app(app)
# Registra el Blueprint de usuarios
app.register_blueprint(user_controller.user_bp)
app.register_blueprint(book_controller.book_bp)

if __name__ == "__main__":
    # Crea las tablas si no existen
    with app.app_context():
        db.create_all()
    app.run(debug=True)
#utils/decorators.py________________________
from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def role_required(roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or not any(current_user.has_role(role) for role in roles):
                flash("No tienes permisos para acceder a esta página.", "error")
                # Redirige a la misma página
                return redirect(url_for("user.profile", id=current_user.id))
            return f(*args, **kwargs)
        return decorated_function
    return decorator
    
#templates/base.html___________________________
<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@1.0.0/css/bulma.min.css">
    <title>{{ title }}</title>
</head>

<body>
    <h1 class="title">Gestión de Libros</h1>
    {% if current_user.is_authenticated %}
    <nav class="breadcrumb" aria-label="breadcrumbs">
        <div id="navbarBasicExample" class="navbar-menu">
            <div class="navbar-start">
                <a class="navbar-item" href="{{ url_for('book.list_books') }}">
                    Lista de Libros
                </a>
                {% if current_user.has_role("admin") %}
                <a class="navbar-item" href="{{ url_for('user.list_users') }}">
                    Lista de Usuarios
                </a>
                <a class="navbar-item" href="{{ url_for('book.create_book') }}">
                    Añadir Libro
                </a>
                {% endif %}
                <a class="navbar-item" href="{{ url_for('user.profile', id=current_user.id) }}">
                    Perfil
                </a>
                <a class="navbar-item" href="{{ url_for('user.logout') }}">
                    Cerrar Sesión
                </a>
            </div>
        </div>
    </nav>
    {% endif %}
    <div class="columns is-mobile is-centered">
        <div class="column is-half">
            {% block content %}{% endblock %}
        </div>
    </div>
</body>

</html>
#templates/actualizar.html
{% extends 'base.html' %}

{% block content %}
<h2 class="subtitle is-2">Actualizar Usuario</h2>

<form method="post" action="/users/{{ user.id }}/update">
    <div class="field">
        <label for="first_name">Nombre:</label>
        <div class="control">
            <input type="text" id="first_name" name="first_name" 
            required class="input" value="{{ user.first_name }}">
        </div>
    </div>
    <div class="field">
        <label for="last_name">Apellido:</label>
        <div class="control">
            <input type="text" id="last_name" name="last_name" 
            required class="input" value="{{ user.last_name }}">
        </div>
    </div>
    <div class="field">
        <label for="username">Nombre de Usuario:</label>
        <div class="control">
            <input type="text" id="username" name="username" 
            required class="input" value="{{ user.username }}">
        </div>
    </div>
    
    <div class="field">
        <label for="role">Rol:</label>
        <div class="control">
            <div>
                <input type="text" id="role" name="role" 
                required class="input" value="{{ user.role }}">
        </div>
    </div>
    <input type="submit" value="Actualizar" class="button is-primary">

{% endblock %}
#templates/books.html
{% extends 'base.html' %}

{% block content %}
<h2 class="subtitle is-2">Lista de Libros</h2>
    <!-- Lista en una tarjeta donde cada libro tenga sus datos y botones para editar y eliminar, solo visibles para administradores -->
    <div class="columns is-multiline">
        {% for book in books %}
            <div class="column is-one-third">
                <div class="card">
                    <div class="card-content">
                        <div class="content">
                            <p><strong>Título: {{ book.title }} </strong></p>
                            <p><strong>Autor: {{ book.author }}</strong></p>
                            <p><strong>Edición: {{ book.edition }}</strong></p>
                            <p><strong>Disponibilidad: {{ book.availability }}</strong></p>
                            <div class="buttons">
                                {% if current_user.has_role('admin') %}
                                    <a href="{{ url_for('book.update_book', id=book.id) }}" 
                                    class="button is-info">Editar</a>
                                    <a href="{{ url_for('book.delete_book', id=book.id) }}" 
                                    class="button is-danger">Eliminar</a>
                                {% endif %}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        {% endfor %}
    </div>
{% endblock %}
#templates/create_book.html
{% extends 'base.html' %}

{% block content %}
<h2 class="subtitle is-2">Registrar Libro</h2>
<form method="post">
    <div class="field">
        <label for="title">Título:</label>
        <div class="control">
            <input type="text" id="title" name="title" required class="input">
        </div>
    </div>
    <div class="field">
        <label for="author">Autor:</label>
        <div class="control">
            <input type="text" id="author" name="author" required class="input">
        </div>
    </div>
    <div class="field">
        <label for="edition">Edición:</label>
        <div class="control">
            <input type="text" id="edition" name="edition" required class="input">
        </div>
    </div>
    <div class="field">
        <label for="availability">Disponibilidad:</label>
        <div class="control">
            <input type="text" id="availability" name="availability" required class="input">
        </div>
    </div>
    <input type="submit" value="Registrar" class="button is-primary">
</form>
{% endblock %}
#templates/login.html
{% extends 'base.html' %}

{% block content %}
    <h1 class="title">Iniciar Sesión</h1>
    <div class="columns is-mobile is-centered">
        <div class="column is-half">
            <form method="post">
                <div class="field">
                    <label class="label">Nombre de Usuario</label>
                    <div class="control">
                        <input class="input" type="text" name="username" required>
                    </div>
                </div>
                <div class="field">
                    <label class="label">Contraseña</label>
                    <div class="control">
                        <input class="input" type="password" name="password" required>
                    </div>
                </div>
                <div class="field is-grouped">
                    <div class="control">
                        <button class="button is-primary" type="submit">Iniciar Sesión</button>
                    </div>
                    <div class="control">
                        <a href="{{ url_for('user.create_user') }}" class="button is-info">Crear Usuario</a>
                    </div>
                </div>
            </form>
        </div>
    </div>
{% endblock %}
#templates/profile.html
{% extends 'base.html' %}

{% block content %}
<h2 class="subtitle is-2">Perfil de Usuario</h2>
<div class="card">
    <div class="card-content">
        <div class="content">
            <p><strong>Nombre:</strong> {{ user.first_name }}</p>
            <p><strong>Apellido:</strong> {{ user.last_name }}</p>
            <p><strong>Nombre de Usuario:</strong> {{ user.username }}</p>
            <p><strong>Rol:</strong> {{ user.role }}</p>
        </div>
    </div>
</div>
{% endblock %}
#templates/registro.html
{% extends 'base.html' %}

{% block content %}
<h2 class="subtitle is-2">Registrar Usuario</h2>
<form method="post">
    <div class="field">
        <label for="first_name">Nombre:</label>
        <div class="control">
            <input type="text" id="first_name" name="first_name" 
            required class="input">
        </div>
    </div>
    <div class="field">
        <label for="last_name">Apellido:</label>
        <div class="control">
            <input type="text" id="last_name" name="last_name" 
            required class="input">
        </div>
    </div>
    <div class="field">
        <label for="username">Nombre de Usuario:</label>
        <div class="control">
            <input type="text" id="username" name="username" 
            required class="input">
        </div>
    </div>
    <div class="field">
        <label for="password">Contraseña:</label>
        <div class="control">
            <input type="password" id="password" name="password" 
            required class="input">
        </div>
    </div>
    <div class="field">
        <label for="role">Rol:</label>
        <div class="control">
            <input type="text" id="role" name="role" 
            required class="input">
        </div>
    </div>
    <input type="submit" value="Registrar" class="button is-primary">
</form>
{% endblock %}
#templates/update_book.html
{% extends 'base.html' %}

{% block content %}
<h2 class="subtitle is-2">Editar Libro</h2>
<form method="post">
    <div class="field">
        <label for="title">Título:</label>
        <div class="control">
            <input type="text" id="title" name="title" required class="input" value="{{ book.title }}">
        </div>
    </div>
    <div class="field">
        <label for="author">Autor:</label>
        <div class="control">
            <input type="text" id="author" name="author" required class="input" value="{{ book.author }}">
        </div>
    </div>
    <div class="field">
        <label for="edition">Edición:</label>
        <div class="control">
            <input type="text" id="edition" name="edition" required class="input" value="{{ book.edition }}">
        </div>
    </div>
    <div class="field">
        <label for="availability">Disponibilidad:</label>
        <div class="control">
            <input type="text" id="availability" name="availability" required class="input" value="{{ book.availability }}">
        </div>
    </div>
    <input type="submit" value="Guardar Cambios" class="button is-primary">
</form>
{% endblock %}
#templates/usuarios.html
{% extends 'base.html' %}

{% block content %}
<h2 class="subtitle is-2">Lista de Usuarios</h2>
    <!--Lista en una tarjeta donde cada usuario tenga sus datos y dos botones para editar y eliminar utilizando grid-->
    <div class="columns is-multiline">
        {% for user in users %}
            <div class="column is-one-third">
                <div class="card">
                    <div class="card-content">
                        <div class="content">
                            <p><strong>Nombre: {{ user.first_name }} </strong></p>
                            <p><strong>Apellido: {{ user.last_name }}</strong></p>
                            <div class="buttons">
                                <a href="{{ url_for('user.update_user', id=user.id) }}" 
                                class="button is-info">Editar</a>
                                <a href="{{ url_for('user.delete_user', id=user.id) }}" 
                                class="button is-danger">Eliminar</a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        {% endfor %}
    </div>

{% endblock %}
#usuarios api mvc__________________
#controller/candy_controller.py
from flask import Blueprint, request, jsonify
from models.candy_model import Candy
from views.candy_view import render_candy_detail, render_candy_list
from flask_jwt_extended import get_jwt_identity
from utils.decorators import roles_required, jwt_required

# Crear un blueprint para el controlador de dulces
candy_bp = Blueprint("candy", __name__)

# Ruta para obtener la lista de dulces
@candy_bp.route("/candies", methods=["GET"])
@jwt_required
#@roles_required(roles=["admin", "user"])
def get_candies():
    candies = Candy.get_all()
    return jsonify(render_candy_list(candies))

# Ruta para obtener un dulce específico por su ID
@candy_bp.route("/candies/<int:id>", methods=["GET"])
@jwt_required
@roles_required(roles=["admin", "user"])
def get_candy(id):
    candy = Candy.get_by_id(id)
    if candy:
        return jsonify(render_candy_detail(candy))
    return jsonify({"error": "Dulce no encontrado"})

# Ruta para crear un nuevo dulce
@candy_bp.route("/candies", methods=["POST"])
@jwt_required
@roles_required(roles=["admin"])
def create_candy():
    data = request.json
    brand = data.get("brand")
    weight = data.get("weight")
    flavor = data.get("flavor")
    origin = data.get("origin")
    
    if not (brand and weight and flavor and origin):
        return jsonify({"error": "Faltan datos requeridos"}), 400
    
    candy = Candy(brand=brand, weight=weight, flavor=flavor, origin=origin)
    candy.save()
    return jsonify(render_candy_detail(candy)), 201
    
# Ruta para actualizar un dulce existente por su ID
@candy_bp.route("/candies/<int:id>", methods=["PUT"])
@jwt_required
@roles_required(roles=["admin"])
def update_candy(id):
    candy = Candy.get_by_id(id)
    if not candy:
        return jsonify({"error": "Dulce no encontrado"}), 404
    
    data = request.json 
    brand = data.get("brand")
    weight = data.get("weight")
    flavor = data.get("flavor")
    origin = data.get("origin")
    
    candy.update(brand=brand, weight=weight, flavor=flavor, origin=origin)
    
    return jsonify(render_candy_detail(candy))

# Ruta para eliminar un dulce existente por su ID
@candy_bp.route("/candies/<int:id>", methods=["DELETE"])
@jwt_required
@roles_required(roles=["admin"])
def delete_candy(id):
    candy = Candy.get_by_id(id)
    if not candy:
        return jsonify({"error": "Dulce no encontrado"}), 404
    
    candy.delete()
    return "", 204
#models/candy_models.py
from database import db

# Define la clase Candy que hereda de db.Model
# "Candy" representa la tabla "candies" en la base de datos
class Candy(db.Model):
    __tablename__ = "candies"
    
    # Define las columnas de la tabla 'candies'
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    flavor = db.Column(db.String, nullable=False)
    origin = db.Column(db.String, nullable=False)
    
    def __init__(self, brand, weight, flavor, origin):
        self.brand = brand
        self.weight = weight
        self.flavor = flavor
        self.origin = origin
    
    # Guarda los datos
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    # Obtiene todos los dulces de la base de datos
    @staticmethod
    def get_all():
        return Candy.query.all()
    
    # Obtiene un dulce por su ID
    @staticmethod
    def get_by_id(id):
        return Candy.query.get(id)
    
    # Actualiza un dulce en la base de datos
    def update(self, brand=None, weight=None, flavor=None, origin=None):
        if brand is not None:
            self.brand = brand
        if weight is not None:
            self.weight = weight
        if flavor is not None:
            self.flavor = flavor
        if origin is not None:
            self.origin = origin
        db.session.commit()
    
    # Elimina un dulce de la base de datos
    def delete(self):
        db.session.delete(self)
        db.session.commit()
#views/candy_views.py        
def render_candy_list(candies):
    # Representa una lista de dulces como una lista de diccionarios
    return [
        {
            "id": candy.id,
            "brand": candy.brand,
            "weight": candy.weight,
            "flavor": candy.flavor,
            "origin": candy.origin
        }
        for candy in candies
    ]

def render_candy_detail(candy):
    # Representa los detalles de un dulce como un diccionario
    return {
        "id": candy.id,
        "brand": candy.brand,
        "weight": candy.weight,
        "flavor": candy.flavor,
        "origin": candy.origin
    }
    
#controllers/user_controller.py
from flask import Blueprint, request, jsonify
from models.user_model import User
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from views.user_view import render_user_detail, render_user_list
from utils.decorators import roles_required, jwt_required

user_bp = Blueprint("user", __name__)

@user_bp.route("/users", methods=["GET"])
#@roles_required(roles=["admin", "user"])
@jwt_required
def get_users():
    users = User.get_all()
    return jsonify(render_user_list(users))

@user_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    roles = data.get("roles")

    if not username or not password:
        return jsonify({"error": "Se requieren nombre de usuario y contraseña"}), 400

    existing_user = User.find_by_username(username)
    if existing_user:
        return jsonify({"error": "El nombre de usuario ya está en uso"}), 400

    new_user = User(username, password,roles)
    new_user.save()

    return jsonify({"message": "Usuario creado exitosamente"}), 201


@user_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = User.find_by_username(username)
    if user and check_password_hash(user.password_hash, password):
        # Si las credenciales son válidas, genera un token JWT
        access_token = create_access_token(identity={"username":username,"roles":user.roles})
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"error": "Credenciales inválidas"}), 401
    
    
@user_bp.route("/users/<int:id>", methods=["PUT"])
@roles_required(roles=["admin"])
@jwt_required
def update_user(id):
    user = User.get_by_id(id)
    if not user:
        return jsonify({"error": "Dulce no encontrado"}), 404
    data = request.json 
    
    username = data.get("username")
    password_hash = data.get("password_hash")
    roles = data.get("roles")
    
    user.update(username=username, password_hash=password_hash, roles=roles)
    
    return jsonify(render_user_detail(user))

# Ruta para eliminar un dulce existente por su ID
@user_bp.route("/users/<int:id>", methods=["DELETE"])
@roles_required(roles=["admin"])
@jwt_required
def delete_user(id):
    user = User.get_by_id(id)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404
    
    user.delete()
    return "", 204
#models/user_model.py
from database import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import json

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    roles=db.Column(db.String(50), nullable=False)

    def __init__(self, username, password, roles=["user"]):
        self.username = username
        self.roles = json.dumps(roles)
        self.password_hash = generate_password_hash(password)

    @staticmethod
    def get_all():
        return User.query.all()
    
    @staticmethod
    def get_by_id(id):
        return User.query.get(id)
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    # Esta funcion encuentra un usuario por su nombre de usuario
    @staticmethod
    def find_by_username(username):
        return User.query.filter_by(username=username).first()
    
    def update(self, username=None, password_hash=None, roles=None):
        if username is not None:
            self.username = username
        if password_hash is not None:
            self.password_hash = password_hash
        if roles is not None:
            self.roles = json.dumps(roles)  # Convertir lista a cadena
        db.session.commit()
    
    # Elimina un dulce de la base de datos
    def delete(self):
        db.session.delete(self)
        db.session.commit()
#views/user_view.py
def render_user_list(users):
    # Representa una lista de dulces como una lista de diccionarios
    return [
        {
            "id": user.id,
            "username": user.username,
            "password": user.password_hash,
            "roles": user.roles,
        }
        for user in users
    ]

def render_user_detail(user):
    # Representa los detalles de un dulce como un diccionario
    return {
            "id": user.id,
            "username": user.username,
            "password": user.password_hash,
            "roles": user.roles,
        }
    
#statics/swagger.json
{
    "openapi": "3.0.1",
    "info": {
        "title": "API de Dulces",
        "version": "1.0.0"
    },
    "paths": {
        "/api/candies": {
            "get": {
                "summary": "Obtiene la lista de todos los Dulces",
                "security": [
                    {
                        "JWTAuth": []
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Lista de dulces",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {
                                        "$ref": "#/components/schemas/Candy"
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "post": {
                "summary": "Crea un nuevo dulce",
                "security": [
                    {
                        "JWTAuth": []
                    }
                ],
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/Candy"
                            }
                        }
                    }
                },
                "responses": {
                    "201": {
                        "description": "Dulce creado",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Candy"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/api/candies/{id}": {
            "get": {
                "summary": "Obtiene un Dulce específico por su ID",
                "security": [
                    {
                        "JWTAuth": []
                    }
                ],
                "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "required": true,
                        "schema": {
                            "type": "integer"
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Detalles del Dulce",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Candy"
                                }
                            }
                        }
                    },
                    "404": {
                        "description": "Dulce no encontrado"
                    }
                }
            },
            "put": {
                "summary": "Actualiza un Dulce existente por su ID",
                "security": [
                    {
                        "JWTAuth": []
                    }
                ],
                "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "required": true,
                        "schema": {
                            "type": "integer"
                        }
                    }
                ],
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/Candy"
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Dulce actualizado",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Candy"
                                }
                            }
                        }
                    },
                    "404": {
                        "description": "Dulce no encontrado"
                    }
                }
            },
            "delete": {
                "summary": "Elimina un Dulce existente por su ID",
                "security": [
                    {
                        "JWTAuth": []
                    }
                ],
                "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "required": true,
                        "schema": {
                            "type": "integer"
                        }
                    }
                ],
                "responses": {
                    "204": {
                        "description": "Dulce eliminado"
                    },
                    "404": {
                        "description": "Dulce no encontrado"
                    }
                }
            }
        },
        "/api/register": {
            "post": {
                "summary": "Registra un nuevo usuario",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/User"
                            }
                        }
                    }
                },
                "responses": {
                    "201": {
                        "description": "Usuario creado"
                    },
                    "400": {
                        "description": "Solicitud incorrecta"
                    }
                }
            }
        },
        "/api/users":{
            "get": {
                "summary": "Obtiene la lista de todos los Usuarios",
                "security": [
                    {
                        "JWTAuth": []
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Lista de Usuarios",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {
                                        "$ref": "#/components/schemas/User"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "/api/users/{id}": {
            "put": {
                "summary": "Actualiza un Usuario existente por su ID",
                "security": [
                    {
                        "JWTAuth": []
                    }
                ],
                "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "required": true,
                        "schema": {
                            "type": "integer"
                        }
                    }
                ],
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/User"
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Usuario actualizado",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/User"
                                }
                            }
                        }
                    },
                    "404": {
                        "description": "Usuario no encontrado"
                    }
                }
            },
            "delete": {
                "summary": "Elimina un Usuario existente por su ID",
                "security": [
                    {
                        "JWTAuth": []
                    }
                ],
                "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "required": true,
                        "schema": {
                            "type": "integer"
                        }
                    }
                ],
                "responses": {
                    "204": {
                        "description": "Usuario eliminado"
                    },
                    "404": {
                        "description": "Usuario no encontrado"
                    }
                }
            }
        },
        "/api/login": {
            "post": {
                "summary": "Inicia sesión con un usuario existente",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/Login"
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Inicio de sesión exitoso",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "access_token": {
                                            "type": "string",
                                            "description": "Token de acceso JWT para el usuario"
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "401": {
                        "description": "Credenciales inválidas"
                    }
                }
            }
        }
    },
    "components": {
        "securitySchemes": {
            "JWTAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT"
            }
        },
        "schemas": {
            "Candy": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer",
                        "readOnly": true
                    },
                    "brand": {
                        "type": "string"
                    },
                    "weight": {
                        "type": "float"
                    },
                    "flavor": {
                        "type": "string"
                    },
                    "origin": {
                        "type": "string"
                    }
                },
                "required": [
                    "brand",
                    "weight",
                    "flavor",
                    "origin"
                ]
            },
            "User": {
                "type": "object",
                "properties": {
                    "username": {
                        "type": "string"
                    },
                    "password": {
                        "type": "string"
                    },
                    "roles":{
                        "type":"array",
                        "items":{
                            "type":"string",
                            "enum":[
                                "admin",
                                "user"
                            ]
                        }
                    }
                },
                "required": [
                    "username",
                    "password",
                    "role"
                ]
            },
            "Login": {
                "type": "object",
                "properties": {
                    "username": {
                        "type": "string"
                    },
                    "password": {
                        "type": "string"
                    }
                },
                "required": [
                    "username",
                    "password"
                ]
            }
        }
    }
}
#utils/decorators.py
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from functools import wraps
import json


def jwt_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return fn(*args, **kwargs)
        except Exception as e:
            return jsonify({"error": str(e)}), 401

    return wrapper


def roles_required(roles=[]):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()
                current_user = get_jwt_identity()
                user_roles = json.loads(current_user.get("roles", []))
                if not set(roles).intersection(user_roles):
                    return jsonify({"error": "Acceso no autorizado para este rol"}), 403
                return fn(*args, **kwargs)
            except Exception as e:
                return jsonify({"error": str(e)}), 401

        return wrapper

    return decorator
#database.py
from flask_sqlalchemy import SQLAlchemy


# Crea una instancia de SQLAlchemy, crea la base de datos
db = SQLAlchemy()
#run.py    
from flask import Flask
from flask_jwt_extended import JWTManager
from controllers.candy_controller import candy_bp
from controllers.user_controller import user_bp
from flask_swagger_ui import get_swaggerui_blueprint
from database import db

app = Flask(__name__)

# Configuracion de la clave secreta para JWT
app.config["JWT_SECRET_KEY"]="tu_clave_secreta_aqui"

# Cofigura la URL de la documentacion OpenAPI
SWAGGER_URL = "/api/docs"

# Ruta de tu archivo OpenAPI/Swagger
API_URL="/static/swagger.json"

# Inicialicza el Blueprint de Swagger UI
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,API_URL,config={"app_name":"Dulceria API"}
)
app.register_blueprint(swagger_ui_blueprint,url_prefix=SWAGGER_URL)

# Configuracion de la base de datos 
app.config["SQLALCHEMY_DATABASE_URI"]= "sqlite:///dulceria.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

# Inicializa la base de datos
db.init_app(app)

# Inicializa la extension JWTManager
jwt=JWTManager(app)

# Registra el blueprint de animales en la aplicacion

app.register_blueprint(user_bp, url_prefix="/api")
app.register_blueprint(candy_bp, url_prefix="/api")

# Crea las tablas si no existen
with app.app_context():
    db.create_all()

#ejecuta la aplicacion
if __name__ == "__main__":
    app.run(debug=True)
```
#Requirements
```txt
flask==2.1.2
flask-sqlalchemy==2.5.1
werkzeug==2.1.2
flask-login==0.6.1
flask-jwt-extended==4.4.4
flask-swagger-ui==4.11.1
jinja2==3.1.2
sqlite3==3.38.5
```
