from init import db, ma

class Licence(db.Model):
    __tablename__ = 'licences'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)

    user_licences = db.relationship('UserLicence', back_populates='licence', cascade='all, delete')

class LicenceSchema(ma.Schema):

    class Meta:
        fields = ('id', 'title')