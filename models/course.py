from init import db, ma
from datetime import date

class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100),nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete='CASCADE'))
    user = db.relationship('User', back_populates='courses')
    user_courses = db.relationship('UserCourse', back_populates='course', cascade='all, delete')

class CourseSchema(ma.Schema):

    class Meta:
        fields = ('id', 'title')


