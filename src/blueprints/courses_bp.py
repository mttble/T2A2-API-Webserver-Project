from flask import Blueprint, request
from models.course import Course, CourseSchema
from init import db
from flask_jwt_extended import jwt_required
from blueprints.auth_bp import admin_required
from datetime import date

# auth route url is defined in the blueprint which is registered in main.
courses_bp = Blueprint('courses', __name__, url_prefix='/courses')


# allows user to get all courses
@courses_bp.route('/')
@jwt_required()
def all_courses():
    # retrieves all existing courses using the select function to select class Course
    stmt = db.select(Course)
    # sessions object handles the database and scalars filters result into rows.
    courses = db.session.scalars(stmt).all()
    # The CourseSchema and dump converts results into JSON to be displayed
    return CourseSchema(many=True).dump(courses)


# Allows admin to add courses
@courses_bp.route('/', methods=['POST'])
@jwt_required()
def create_course():
    admin_required()
    # Parse and validate the incoming JSON data using the CourseSchema
    course_info = CourseSchema().load(request.json)
    # Create a new Course object with the provided information
    course = Course(
        title = course_info['title']
    )
    # Add the new course to the database session
    db.session.add(course)
    # Commit the changes to the database
    db.session.commit()
    # Return the serialized representation of the created course as a response
    return CourseSchema().dump(course), 201


# Allows admin to delete courses
@courses_bp.route('/<int:course_id>', methods=['DELETE'])
@jwt_required()
def delete_course(course_id):
    admin_required()
    # Select the course from the database by its ID
    stmt = db.select(Course).filter_by(id=course_id)
    course = db.session.scalar(stmt)
    if course:
        # Delete the course from the database session
        db.session.delete(course)
        # Commit the changes to the database
        db.session.commit()
        return {}, 200
    else:
        return {'error':'Course not found'}, 404