import pytest
from flask_jwt_extended import create_access_token
from app.run import app
from app.database import db


@pytest.fixture(scope="module")
def test_client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["JWT_SECRET_KEY"] = "test_secret_key"

    with app.test_client() as testing_client:
        with app.app_context():  # Cambiar esto
            db.create_all()
            yield testing_client
            db.drop_all()



@pytest.fixture(scope="module")
def admin_auth_header():
    with app.app_context():
        access_token = create_access_token(
            identity="andy@gmail.com", additional_claims={"role": "admin"}
        )
        headers = {"Authorization": f"Bearer {access_token}"}

        return headers


@pytest.fixture(scope="module")
def user_auth_header():
    with app.app_context():
        access_token = create_access_token(
            identity="andy@gmail.com", additional_claims={"role": "user"}
        )

        headers = {"Authorization": f"Bearer {access_token}"}
        return headers
