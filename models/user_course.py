from init import db, ma
from datetime import date

class UserCourse(db.Model):
    __tablename__ = 'user_courses'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(30),nullable=False)
    date_of_completion = db.Column(db.Date)
    date_of_expiry = db.Column(db.Date,nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', back_populates='user_courses')

    course_id = db.Column(db.Integer, db.ForeignKey("courses.id", ondelete='CASCADE'), nullable=False)
    course = db.relationship('Course', back_populates='user_courses')

class UserCourseSchema(ma.Schema):

    class Meta:
        fields = ('user_id', 'course_id', 'status', 'date_of_completion', 'date_of_expiry')