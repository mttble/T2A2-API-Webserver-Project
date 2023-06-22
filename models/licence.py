from init import db, ma
from datetime import date

class Licence(db.Model):
    __tablename__ = 'licences'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    number = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(100))
    status = db.Column(db.String(30), nullable=False)
    date_of_completion = db.Column(db.Date, nullable=False)
    date_of_expiry = db.Column(db.Date,nullable=False)

class LicenceSchema(ma.Schema):

    class Meta:
        fields = ('title', 'number', 'description', 'status', 'date_of_completion', 'date_of_expiry')