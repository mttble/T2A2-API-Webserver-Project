from flask import Blueprint
from init import db, bcrypt
from datetime import datetime
from models.user import User
from models.course import Course

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

    courses = [
        Course(
            title="LV Rescue and Resuscitation",
            status="In Date",
            date_of_completion=datetime.date(2023, 6, 21),
            date_of_expiry=datetime.date(2024, 6, 21)
            
        ),
        Course(
            title="High Voltage Terminations",
            status="In Date",
            date_of_completion=datetime.date(2023, 5, 22),
            date_of_expiry=datetime.date(2024, 5, 22)
            
        ),
        
    ]

    db.session.query(Course).delete()
    db.session.add_all(courses)
    db.session.commit()

    print("Models seeded")
