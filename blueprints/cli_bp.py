from flask import Blueprint
from init import db, bcrypt
from models.user import User

cli_bp = Blueprint('db', __name__)

@cli_bp.cli.command("create")
def create_db():
    db.drop_all()
    db.create_all()
    print("Tables created successfully")

@cli_bp.cli.command("seed")
def seed_db():
    users = [
        User(
            email='admin@foo.com',
            password=bcrypt.generate_password_hash('mushroompie').decode('utf-8'),
            is_admin=True
        ),
        User(
            name='Thomas Anderson',
            email='mranderson@foo.com',
            password=bcrypt.generate_password_hash('iknowkungfu').decode('utf-8')
        )
    ]
    db.session.query(User).delete()
    db.session.add_all(users)
    db.session.commit()