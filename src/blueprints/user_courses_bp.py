from flask import Blueprint, request
from models.user_course import UserCourse, UserCourseSchema
from models.course import Course
from models.user import User
from init import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from blueprints.auth_bp import admin_required
from datetime import datetime

# auth route url is defined in the blueprint which is registered in main.
user_courses_bp = Blueprint('user_courses', __name__, url_prefix='/user_courses')


# current user can see all of their courses
@user_courses_bp.route('/')
@jwt_required()
def current_user_courses():
    current_user_id = get_jwt_identity()
    # select * from courses;
    stmt = db.select(UserCourse).where(UserCourse.user_id == current_user_id)
    # sessions object handles the database and scalars filters result into rows.
    user_courses = db.session.scalars(stmt).all()
    # The UserCourseSchema and dump converts results into JSON to be displayed
    return UserCourseSchema(many=True).dump(user_courses)


# Allows admin to get all user courses
@user_courses_bp.route('/users/all')
@jwt_required()
def all_user_courses():
    admin_required()
    # Retrieve all user courses from the database
    stmt = db.select(UserCourse)
    user_courses = db.session.scalars(stmt).all()
    return UserCourseSchema(many=True).dump(user_courses)


# Allows admin to get individual users user_courses
@user_courses_bp.route('/users/<int:user_id>')
@jwt_required()
def individual_user_courses(user_id):
    admin_required()
    # Retrieve user courses for the specified user from the database
    stmt = db.select(UserCourse).filter_by(user_id=user_id)
    user_courses = db.session.scalars(stmt).all()
    if user_courses:
        return UserCourseSchema(many=True).dump(user_courses)
    else:
        return {'error': 'User not found or has no courses'}, 400


# Allows user to create user_courses
@user_courses_bp.route('/', methods=['POST'])
@jwt_required()
def create_user_course():
    # Deserialise the incoming JSON data into a UserCourse object using UserCourseSchema
    user_course_info = UserCourseSchema().load(request.json)
    # Get the user ID from the JWT token
    user_id = get_jwt_identity()
    # Retrieve the user from the database based on the user ID
    user = User.query.get(user_id)
    if not user:
        return {'error': 'User not found'}, 404
    # Retrieve the course from the database based on the course ID specified in the request
    course = Course.query.get(user_course_info['course_id'])
    if not course:
        return {'error': 'Course not found'}, 404
    # Check if the user already has an existing user course entry with the same user ID and course ID
    existing_course = UserCourse.query.filter_by(user_id=user_id, course_id=user_course_info['course_id']).first()
    if existing_course:
        return {'error': 'User already has a course with the same user_id and course_id'}, 400

    # Create a new UserCourse instance
    user_course = UserCourse(
        user=user,
        course=course,
        date_of_completion=user_course_info['date_of_completion'],
        date_of_expiry=user_course_info['date_of_expiry']
    )
    db.session.add(user_course)
    db.session.commit()
    return UserCourseSchema().dump(user_course), 201


# Allows user to update their user_course information
@user_courses_bp.route('/<int:course_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_user_course(course_id):
    # Get the user ID from the JWT token
    user_id = get_jwt_identity()
    # Retrieve the user course from the database based on the user ID and course ID
    stmt = db.select(UserCourse).filter_by(user_id=user_id, course_id=course_id)
    user_course = db.session.scalar(stmt)
    # Deserialise the incoming JSON data into a UserCourse object using UserCourseSchema
    user_course_info = UserCourseSchema().load(request.json)
    if user_course:
        # Update the user course with the new information
        user_course.date_of_completion = user_course_info.get('date_of_completion', user_course.date_of_completion)
        user_course.date_of_expiry = user_course_info.get('date_of_expiry', user_course.date_of_expiry)
        db.session.commit()
        # Return the updated user course information
        return UserCourseSchema().dump(user_course)
    else:
        return {'error':'Course not found'}, 404


# Allows admin to update users user_course info
@user_courses_bp.route('/user/<int:user_id>/course/<int:course_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def admin_update_user_course(user_id, course_id):
    admin_required()
    # Retrieve the user course from the database based on the user ID and course ID
    stmt = db.select(UserCourse).filter_by(user_id=user_id, course_id=course_id)
    user_course = db.session.scalar(stmt)
    # Deserialize the incoming JSON data into a UserCourse object using UserCourseSchema
    user_course_info = UserCourseSchema().load(request.json)
    if user_course:
        # Update the user course with the new information
        user_course.date_of_completion = user_course_info.get('date_of_completion', user_course.date_of_completion)
        user_course.date_of_expiry = user_course_info.get('date_of_expiry', user_course.date_of_expiry)
        db.session.commit()
        # Return the updated user course information
        return UserCourseSchema().dump(user_course)
    else:
        return {'error': 'User or course not found'}, 404


# Allows user to delete user_course
@user_courses_bp.route('/<int:course_id>', methods=['DELETE'])
@jwt_required()
def delete_user_course(course_id):
    # Get the user ID from the JWT token
    user_id = get_jwt_identity()
    # Retrieve the user course from the database based on the user ID and course ID
    stmt = db.select(UserCourse).filter_by(user_id=user_id, course_id=course_id)
    user_course = db.session.scalar(stmt)
    if user_course:
        # Delete the user_course from the database
        db.session.delete(user_course)
        db.session.commit()
        return {}, 200
    else:
        return {'error':'User course not found'}, 404
    
# Allows admin to delete a users user_course
@user_courses_bp.route('user/<int:user_id>/course/<int:course_id>', methods=['DELETE'])
@jwt_required()
def admin_delete_user_course(user_id, course_id):
    admin_required()
    # Retrieve the user course from the database based on the user ID and course ID
    stmt = db.select(UserCourse).filter_by(user_id=user_id, course_id=course_id)
    user_course = db.session.scalar(stmt)
    if user_course:
        db.session.delete(user_course)
        db.session.commit()
        return {}, 200
    else:
        return {'error':'User course not found'}, 404