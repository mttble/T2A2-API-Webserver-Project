from init import db
from datetime import date

class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    status = db.Column(db.String(30))
    date_of_completion = db.Column(db.Date)
    date_of_expiry = db.Column(db.Date)

