from flask import Blueprint
from init import db, bcrypt
from datetime import date
from models.user import User
from models.course import Course
from models.licence import Licence
from models.vaccination import Vaccination

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

    courses_data = [
        Course(
            title="LV Rescue and Resuscitation",
            status="In date" if date(2024, 6, 21) >= date.today() else "Out of date",
            date_of_completion=date(2023, 6, 21),
            date_of_expiry=date(2024, 6, 21)
        ),
        Course(
            title="High Voltage Terminations",
            status="In date" if date(2024, 5, 22) >= date.today() else "Out of date",
            date_of_completion=date(2023, 5, 22),
            date_of_expiry=date(2022, 5, 22)
        )
    ]

    # Auto fill for status In date or Out of date depending on date of expiry
    courses = []
    for course in courses_data:
        course.status = "In date" if course.date_of_expiry >= date.today() else "Out of date"
        courses.append(course)

    db.session.query(Course).delete()
    db.session.add_all(courses)
    db.session.commit()

    licences_data = [
        Licence(
            title="Electrical",
            number="PGE123456",
            description="",
            status="",
            date_of_completion=date(2023, 6, 21),
            date_of_expiry=date(2024, 6, 21)
        ),
        Licence(
            title="White Card",
            number="A123456",
            description="",
            status="",
            date_of_completion=date(2023, 5, 22),
            date_of_expiry=date(2024, 5, 22)
        ),
        Licence(
            title="Yellow Card",
            number="B123456",
            description="",
            status="",
            date_of_completion=date(2023, 5, 22),
            date_of_expiry=date(2024, 5, 22)
        )
    ]

    # Auto fill for status In date or Out of date depending on date of expiry
    licences = []
    for licence in licences_data:
        licence.status = "In date" if licence.date_of_expiry >= date.today() else "Out of date"
        licences.append(licence)

    db.session.query(Licence).delete()
    db.session.add_all(licences)
    db.session.commit()

    vaccinations_data = [
        Vaccination(
            title="Influenza",
            status="",
            date_of_completion=date(2023, 6, 21),
            date_of_expiry=date(2024, 6, 21)
        ),
        Vaccination(
            title="Covid",
            status="",
            date_of_completion=date(2023, 5, 22),
            date_of_expiry=date(2024, 5, 22)
        ),
        Vaccination(
            title="Tetanus",
            status="",
            date_of_completion=date(2023, 5, 22),
            date_of_expiry=date(2024, 5, 22)
        ),
        Vaccination(
            title="Hepatitis A",
            status="",
            date_of_completion=date(2023, 5, 22),
            date_of_expiry=date(2024, 5, 22)
        ),
        Vaccination(
            title="Hepatitis B",
            status="",
            date_of_completion=date(2023, 5, 22),
            date_of_expiry=date(2024, 5, 22)
        )
    ]

    # Auto fill for status In date or Out of date depending on date of expiry
    vaccinations = []
    for vaccination in vaccinations_data:
        vaccination.status = "In date" if vaccination.date_of_expiry >= date.today() else "Out of date"
        vaccinations.append(vaccination)

    db.session.query(Vaccination).delete()
    db.session.add_all(vaccinations)
    db.session.commit()

    print("Models seeded")
