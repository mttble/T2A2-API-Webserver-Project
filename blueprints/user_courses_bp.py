from flask import Blueprint, request
from models.user_course import UserCourse, UserCourseSchema
from models.course import Course
from models.user import User
from init import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from blueprints.auth_bp import admin_required
from datetime import date

user_courses_bp = Blueprint('user_courses', __name__, url_prefix='/user_courses')

@user_courses_bp.route('/')
@jwt_required()
def all_user_courses():
    # select * from courses;
    stmt = db.select(UserCourse)
    user_courses = db.session.scalars(stmt).all()
    return UserCourseSchema(many=True).dump(user_courses)


@user_courses_bp.route('/', methods=['POST'])
@jwt_required()
def create_user_course():
    user_course_info = UserCourseSchema().load(request.json)

    user_id = get_jwt_identity()

    # Get the user
    user = User.query.get(user_id)
    if not user:
        return {'error': 'User not found'}, 404

    # Get the course
    course = Course.query.get(user_course_info['course_id'])
    if not course:
        return {'error': 'Course not found'}, 404

    # Create a new UserCourse instance
    user_course = UserCourse(
        user=user,
        course=course,
        date_of_completion=user_course_info['date_of_completion'],
        date_of_expiry=user_course_info['date_of_expiry']
    )

    # Add the user_course to the session
    db.session.add(user_course)
    db.session.commit()
    return UserCourseSchema().dump(user_course), 201