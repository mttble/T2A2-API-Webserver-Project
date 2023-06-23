from init import db, ma
from marshmallow import fields


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.Integer, nullable=False, unique=True)
    is_admin = db.Column(db.Boolean, default=False)

    user_courses = db.relationship('UserCourse', back_populates='user', cascade='all, delete')
    user_licences = db.relationship("UserLicence", back_populates="user", cascade='all, delete')



class UserSchema(ma.Schema):
    licences = fields.List(fields.Nested('LicenceSchema', exclude=['user', 'id']))
    courses = fields.List(fields.Nested('CourseSchema', exclude=['user', 'id']))

    class Meta:
        fields = ('name', 'email', 'password', 'is_admin', 'licences', 'courses')
