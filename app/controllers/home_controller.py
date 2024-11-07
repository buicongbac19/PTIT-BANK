from sqlalchemy.exc import IntegrityError
from app.models import User


def create_user(username, email):
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        print("Email already exists.")
        return "Email already exists."

    new_user = User(username=username, email=email)
    try:
        db.session.add(new_user)
        db.session.commit()
        return "User created successfully."
    except IntegrityError:
        db.session.rollback()
        print("An error occurred. Email might already exist.")
        return "Failed to create user due to unique constraint."
