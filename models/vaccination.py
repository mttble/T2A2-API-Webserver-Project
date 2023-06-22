from init import db, ma
from datetime import date

class Vaccination(db.Model):
    __tablename__ = 'vaccinations'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    status = db.Column(db.String(30),nullable=False)
    date_of_completion = db.Column(db.Date,nullable=False)
    date_of_expiry = db.Column(db.Date,nullable=False)

class VaccinationSchema(ma.Schema):

    class Meta:
        fields = ('title', 'status', 'date_of_completion', 'date_of_expiry')