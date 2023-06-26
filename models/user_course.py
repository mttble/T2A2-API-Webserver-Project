from init import db, ma
from marshmallow import fields

class UserCourse(db.Model):
    __tablename__ = 'user_courses'

    id = db.Column(db.Integer, primary_key=True)
    date_of_completion = db.Column(db.DateTime,nullable=False)
    date_of_expiry = db.Column(db.DateTime,nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='user_courses')

    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    course = db.relationship('Course', back_populates='user_courses')

class UserCourseSchema(ma.Schema):
    date_of_completion = fields.Date(error_messages={'invalid': 'Invalid date format. Try YYYY-MM-DD'})
    date_of_expiry = fields.Date(error_messages={'invalid': 'Invalid date format. Try YYYY-MM-DD'})
    class Meta:
        fields = ('user_id', 'course_id', 'date_of_completion', 'date_of_expiry')
