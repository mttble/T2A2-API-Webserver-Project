from flask import Blueprint, request
from models.course import Course, CourseSchema
from init import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from blueprints.auth_bp import admin_required
from datetime import date

courses_bp = Blueprint('courses', __name__, url_prefix='/courses')

@courses_bp.route('/')
@jwt_required()
def all_courses():
    # select * from cards;
    stmt = db.select(Course)
    courses = db.session.scalars(stmt).all()
    return CourseSchema(many=True).dump(courses)

# Allows admin to add courses
@courses_bp.route('/', methods=['POST'])
@jwt_required()
def create_course():
    admin_required()
    course_info = CourseSchema().load(request.json)
    course = Course(
        title = course_info['title']
    )
    db.session.add(course)
    db.session.commit()

    return CourseSchema().dump(course), 201