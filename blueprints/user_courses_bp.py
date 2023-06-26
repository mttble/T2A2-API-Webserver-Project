from flask import Blueprint, request
from models.user_course import UserCourse, UserCourseSchema
from models.course import Course
from models.user import User
from init import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from blueprints.auth_bp import admin_required
from datetime import date

user_courses_bp = Blueprint('user_courses', __name__, url_prefix='/user_courses')

# current user can see all of their courses
@user_courses_bp.route('/')
@jwt_required()
def current_user_courses():
    current_user_id = get_jwt_identity()
    # select * from courses;
    stmt = db.select(UserCourse).where(UserCourse.user_id == current_user_id)
    user_courses = db.session.scalars(stmt).all()
    return UserCourseSchema(many=True).dump(user_courses)

#  admin can get all user courses
@user_courses_bp.route('/all')
@jwt_required()
def all_user_courses():
    admin_required()
    # select * from courses;
    stmt = db.select(UserCourse)
    user_courses = db.session.scalars(stmt).all()
    return UserCourseSchema(many=True).dump(user_courses)

# admin can get individual user_courses
@user_courses_bp.route('/user/<int:user_id>')
@jwt_required()
def individual_user_courses(user_id):
    admin_required()
    # select * from courses;
    stmt = db.select(UserCourse).filter_by(user_id=user_id)
    user_courses = db.session.scalars(stmt).all()
    if user_courses:
        return UserCourseSchema(many=True).dump(user_courses)
    else:
        return {'error': 'User not found or has no courses'}

# user can create user_courses
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

# allows user to update their user_course info
@user_courses_bp.route('/course/<int:course_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_user_course(course_id):
    user_id = get_jwt_identity()
    stmt = db.select(UserCourse).filter_by(user_id=user_id, course_id=course_id)
    user_course = db.session.scalar(stmt)
    user_course_info = UserCourseSchema().load(request.json)
    if user_course:
        user_course.date_of_completion = user_course_info.get('date_of_completion', user_course.date_of_completion)
        user_course.date_of_expiry = user_course_info.get('date_of_expiry', user_course.date_of_expiry)
        db.session.commit()
        return UserCourseSchema().dump(user_course)
    else:
        return {'error':'Course not found'}, 404

# allows admin to update users user_course info
@user_courses_bp.route('/user/<int:user_id>/course/<int:course_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def admin_update_user_course(user_id, course_id):
    admin_required()
    stmt = db.select(UserCourse).filter_by(user_id=user_id, course_id=course_id)
    user_course = db.session.scalar(stmt)
    user_course_info = UserCourseSchema().load(request.json)
    if user_course:
        user_course.date_of_completion = user_course_info.get('date_of_completion', user_course.date_of_completion)
        user_course.date_of_expiry = user_course_info.get('date_of_expiry', user_course.date_of_expiry)
        db.session.commit()
        return UserCourseSchema().dump(user_course)
    else:
        return {'error': 'User or course not found'}, 404

# allows user to delete user_course
@user_courses_bp.route('/course/<int:course_id>', methods=['DELETE'])
@jwt_required()
def delete_user_course(course_id):
    user_id = get_jwt_identity()
    stmt = db.select(UserCourse).filter_by(user_id=user_id, course_id=course_id)
    user_course = db.session.scalar(stmt)
    if user_course:
        db.session.delete(user_course)
        db.session.commit()
        return {}, 200
    else:
        return {'error':'User course not found'}, 404
    
# allows admin to delete a users user_course
@user_courses_bp.route('user/<int:user_id>/course/<int:course_id>', methods=['DELETE'])
@jwt_required()
def admin_delete_user_course(user_id, course_id):
    admin_required()
    stmt = db.select(UserCourse).filter_by(user_id=user_id, course_id=course_id)
    user_course = db.session.scalar(stmt)
    if user_course:
        db.session.delete(user_course)
        db.session.commit()
        return {}, 200
    else:
        return {'error':'User course not found'}, 404