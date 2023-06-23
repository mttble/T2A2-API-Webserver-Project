from init import db, ma

class UserCourse(db.Model):
    __tablename__ = 'user_courses'

    id = db.Column(db.Integer, primary_key=True)
    date_of_completion = db.Column(db.Date,nullable=False)
    date_of_expiry = db.Column(db.Date,nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='user_courses')

    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    course = db.relationship('Course', back_populates='user_courses')

class UserCourseSchema(ma.Schema):

    class Meta:
        fields = ('user_id', 'course_id', 'date_of_completion', 'date_of_expiry')