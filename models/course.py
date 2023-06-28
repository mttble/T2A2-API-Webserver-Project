from init import db, ma

# SqlAlchemy creates table structure with column names and data types
class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100),nullable=False)

    user_courses = db.relationship('UserCourse', back_populates='course', cascade='all, delete')


# Marshmallow converts these datatypes into readable format via the Schema
class CourseSchema(ma.Schema):

    class Meta:
        fields = ('id', 'title')


