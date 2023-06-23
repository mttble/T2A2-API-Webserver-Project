from flask import Blueprint
from models.course import Course, CourseSchema
from init import db
from flask_jwt_extended import jwt_required
from datetime import date

courses_bp = Blueprint('courses', __name__, url_prefix='/courses')

@courses_bp.route('/')
@jwt_required()
def all_courses():
    # select * from cards;
    stmt = db.select(Course)
    courses = db.session.scalars(stmt).all()
    return CourseSchema(many=True).dump(courses)