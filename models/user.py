from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length

# SqlAlchemy creates table structure with column names and data types
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String, nullable=False, unique=True)
    is_admin = db.Column(db.Boolean, default=False)

    user_courses = db.relationship('UserCourse', back_populates='user', cascade='all, delete')
    user_licences = db.relationship("UserLicence", back_populates="user", cascade='all, delete')


# Marshmallow converts these datatypes into readable format via the Schema the use of fields allows each column item to be retrieved by the blueprint
class UserSchema(ma.Schema):
    licences = fields.List(fields.Nested('LicenceSchema', exclude=['user', 'id']))
    courses = fields.List(fields.Nested('CourseSchema', exclude=['user', 'id']))
    password = fields.String(required=True, validate=Length(min=7))
    phone_number = fields.String(required=True, validate=Length(min=10))

    class Meta:
        fields = ('name', 'email', 'phone_number', 'password', 'is_admin', 'licences', 'courses')
