from init import db, ma
from marshmallow import fields

class UserLicence(db.Model):
    __tablename__ = 'user_licences'

    id = db.Column(db.Integer, primary_key=True)
    licence_number = db.Column(db.String(50),nullable=False)
    description = db.Column(db.String(50))
    date_of_expiry = db.Column(db.DateTime,nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", back_populates="user_licences")

    licence_id = db.Column(db.Integer, db.ForeignKey('licences.id'))
    licence = db.relationship("Licence", back_populates="user_licences")

class UserLicenceSchema(ma.Schema):
    date_of_expiry = fields.Date(error_messages={'invalid': 'Invalid date format. Try YYYY-MM-DD'})
    class Meta:
        fields = ('user_id', 'licence_id', 'licence_number', 'description', 'date_of_expiry')
