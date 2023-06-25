from flask import Blueprint
from init import db, bcrypt
from datetime import date
from models.user import User
from models.course import Course
from models.user_course import UserCourse
from models.licence import Licence
from models.user_licence import UserLicence

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
            name = "admin",
            email = 'admin@foo.com',
            password = bcrypt.generate_password_hash('mushroompie').decode('utf-8'),
            phone_number = "0448981222",
            is_admin = True
        ),
        User(
            name='Thomas Anderson',
            email='mranderson@foo.com',
            phone_number = "0448981223",
            password=bcrypt.generate_password_hash('iknowkungfu').decode('utf-8')
        ),
        User(
            name='Joe Dirt',
            email='joedirt@foo.com',
            phone_number = "0448981224",
            password=bcrypt.generate_password_hash('joedirtay').decode('utf-8')
        )
    ]
    db.session.query(User).delete()
    db.session.add_all(users)
    db.session.commit()

    courses = [
        Course(
            title="LV Rescue and Resuscitation"
        ),
        Course(
            title="High Voltage Terminations"
        ),
        Course(
            title="High Voltage Switching"
        ),
        Course(
            title="Thermography and Ultrasonic"
        )
    ]

    db.session.query(Course).delete()
    db.session.add_all(courses)
    db.session.commit()

    user_courses = [
        UserCourse(
            user = users[0],
            course = courses[0],
            date_of_completion = date(2023, 5, 22),
            date_of_expiry = date(2023, 6, 20)
        ),
        UserCourse(
            user = users[0],
            course = courses[1],
            date_of_completion = date(2023, 5, 22),
            date_of_expiry = date(2024, 5, 22)
        ),
        UserCourse(
            user = users[1],
            course = courses[2],
            date_of_completion = date(2023, 5, 22),
            date_of_expiry = date(2024, 5, 22)
        ),
        UserCourse(
            user = users[2],
            course = courses[2],
            date_of_completion = date(2023, 5, 22),
            date_of_expiry = date(2024, 5, 22)
        )
    ]

    db.session.query(UserCourse).delete()
    db.session.add_all(user_courses)
    db.session.commit()


    licences = [
        Licence(
            title="Drivers",
        ),
        Licence(
            title="Electrical",
        ),
        Licence(
            title="White Card",
        ),
        Licence(
            title="Yellow Card",
        )
    ]

    db.session.query(Licence).delete()
    db.session.add_all(licences)
    db.session.commit()

    user_licences = [
        UserLicence(
            user = users[0],
            licence = licences[3],
            licence_number = "A123456",
            description = "Boom lift, vertical lift",
            date_of_expiry = date(2023, 6, 20)
        ),
        UserLicence(
            user = users[0],
            licence = licences[1],
            licence_number = "B123456",
            description = "",
            date_of_expiry = date(2024, 5, 22)
        ),
        UserLicence(
            user = users[1],
            licence = licences[1],
            licence_number = "C123456",
            description = "",
            date_of_expiry = date(2024, 5, 22)
        )
    ]

    db.session.query(UserLicence).delete()
    db.session.add_all(user_licences)
    db.session.commit()

    print("Models seeded")
