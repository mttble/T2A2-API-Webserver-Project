from flask import Blueprint, request, abort
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import  create_access_token, get_jwt_identity, jwt_required
from datetime import timedelta
from models.user import User, UserSchema
from init import db, bcrypt

# auth route url is defined in the blueprint which is registered in main.
auth_bp = Blueprint('auth', __name__)

# allows users to get employee contact details
@auth_bp.route('/users')
@jwt_required()
def all_users():
    # retrieves all existing users using the select function to select class User
    stmt = db.select(User)
    # sessions object handles the database and scalars filters result into rows.
    users = db.session.scalars(stmt)
    # The UserSchema and dump converts results into JSON to be displayed (excluding password)
    return UserSchema(many=True, exclude=['password']).dump(users)


# Allows user to register
@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        # Parse, sanitise and validate the incoming JSON data via the schema.
        user_info = UserSchema().load(request.json)
        user = User(
            name=user_info['name'],
            email=user_info['email'],
            phone_number=user_info['phone_number'],
            password=bcrypt.generate_password_hash(user_info['password']).decode('utf8'),
        )
        
        # Add and commit the new user
        db.session.add(user)
        db.session.commit()

        # Return new user information (exlcuding password and is_admin)
        return UserSchema(exclude=['password','is_admin']).dump(user), 201
    except IntegrityError:
        return {'error': 'User already exists'}, 409


# Allows user to login via POST method
@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        # login finds an existing user in the database that matches email
        stmt = db.select(User).where(User.email==request.json['email'])
        # session object handles database and scalar filters result by email
        user = db.session.scalar(stmt)
        # if user email and password exist it creates a token and the user is logged in.
        if user and bcrypt.check_password_hash(user.password, request.json['password']):
            token = create_access_token(identity=user.id, expires_delta=timedelta(hours=1))
            return {'token':token, 'user': UserSchema(exclude=['password']).dump(user)}
        else:
            return {'error': 'Invalid email address or password'}, 401
    except KeyError:
        return {'error': 'Email and password are required'}, 400


# Allows admin to delete user and cascade delete in User model will delete all their user_courses and user_licences
@auth_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    # Select the User from the database based on the provided user_id
    stmt = db.select(User).filter_by(id=user_id)
    # Execute the query and retrieve the User object from the database
    user = db.session.scalar(stmt)
    if user:
        # Check if the requesting user is an admin
        admin_required()
        # Delete the User from the database
        db.session.delete(user)
        # Commit the changes to the database
        db.session.commit()
        return {}, 200
    else:
        return {'error':'User not found'}, 404


# Allows user or admin to update user information
@auth_bp.route('/users/<int:user_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_user(user_id):
    # Retrieve the User from the database based on the provided user_id
    user = db.session.query(User).get(user_id)
    if not user:
        # If the user does not exist, return an error response
        return {'error': 'User not found'}, 404
    current_user_id = get_jwt_identity()
    # Check if the requesting user is an admin or the same user being updated
    admin_or_user_required(current_user_id,user_id)
    user_info = UserSchema().load(request.json, partial=True)
    # Update user information if fields are provided
    if 'name' in user_info:
        user.name = user_info['name']
    if 'email' in user_info:
        user.email = user_info['email']
    if 'phone_number' in user_info:
        user.phone_number = user_info['phone_number']
    if 'password' in user_info:
        user.password = bcrypt.generate_password_hash(user_info['password']).decode('utf8')
    # Commit the changes to the database
    db.session.commit()
    # Return the updated user information, excluding the password field
    return UserSchema(exclude=['password']).dump(user), 200


def admin_required():
    # Retrieve the user ID from the JWT token
    user_id = get_jwt_identity()
    # Construct a select statement to retrieve the user with the specified user_id
    stmt = db.select(User).filter_by(id=user_id)
    # Execute the select statement and retrieve the user object from the database
    user = db.session.scalar(stmt)
    # Check if the user exists and if the user is an admin
    if not (user and user.is_admin):
        abort(401, description="You must be an admin")


def admin_or_user_required(current_user_id, user_id):
    # Retrieve the user with the current_user_id from the database
    user = db.session.query(User).get(current_user_id)
    # Check if the user exists and if the user is either an admin or the same user as user_id
    if not (user and (user.is_admin or current_user_id == user_id)):
        abort(401, description='You must be an admin or the user')