from init import db, ma
from marshmallow import fields


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    courses = db.relationship('Course', back_populates='user', cascade='all, delete')
    user_courses = db.relationship('UserCourse', back_populates='user', cascade='all, delete')

class UserSchema(ma.Schema):

    class Meta:
        fields = ('name', 'email', 'password', 'is_admin')
