from init import db, ma

class UserLicence(db.Model):
    __tablename__ = 'user_licences'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(50))
    description = db.Column(db.Text)
    date_of_completion = db.Column(db.Date)
    date_of_expiry = db.Column(db.Date)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", back_populates="user_licences")

    licence_id = db.Column(db.Integer, db.ForeignKey('licences.id'))
    licence = db.relationship("Licence", back_populates="user_licences")

class UserLicenceSchema(ma.Schema):

    class Meta:
        fields = ('user_id', 'licence_id', 'date_of_completion', 'date_of_expiry')