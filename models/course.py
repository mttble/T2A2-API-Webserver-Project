from init import db, ma

class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100),nullable=False)

    user_courses = db.relationship('UserCourse', back_populates='course')

class CourseSchema(ma.Schema):

    class Meta:
        fields = ('id', 'title')


