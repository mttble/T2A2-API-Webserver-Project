from flask import Blueprint, request
from models.user_licence import UserLicence, UserLicenceSchema
from models.licence import Licence
from models.user import User
from init import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from blueprints.auth_bp import admin_required
from datetime import datetime

user_licences_bp = Blueprint('user_licences', __name__, url_prefix='/user_licences')


# Current user can see all of their licenses
@user_licences_bp.route('/')
@jwt_required()
def current_user_licences():
    current_user_id = get_jwt_identity()
    # select * from licences;
    stmt = db.select(UserLicence).where(UserLicence.user_id == current_user_id)
    user_licences = db.session.scalars(stmt).all()
    return UserLicenceSchema(many=True).dump(user_licences)


#  Admin can get all user licences
@user_licences_bp.route('users/all')
@jwt_required()
def all_user_licences():
    admin_required()
    # select * from licences;
    stmt = db.select(UserLicence)
    user_licences = db.session.scalars(stmt).all()
    return UserLicenceSchema(many=True).dump(user_licences)


# Admin can get individual user_licences
@user_licences_bp.route('/users/<int:user_id>')
@jwt_required()
def individual_user_licences(user_id):
    admin_required()
    # select * from licences;
    stmt = db.select(UserLicence).filter_by(user_id=user_id)
    user_licences = db.session.scalars(stmt).all()
    if user_licences:
        return UserLicenceSchema(many=True).dump(user_licences)
    else:
        return {'error': 'User not found or has no licences'}


# Allows user to create a new user_licences
@user_licences_bp.route('/', methods=['POST'])
@jwt_required()
def create_user_licence():
    user_licence_info = UserLicenceSchema().load(request.json)
    user_id = get_jwt_identity()
    # Get the user
    user = User.query.get(user_id)
    if not user:
        return {'error': 'User not found'}, 404
    # Get the licence
    licence = Licence.query.get(user_licence_info['licence_id'])
    if not licence:
        return {'error': 'Licence not found'}, 404
    # prevent multiple entries. If licence is existing they can update
    existing_licence = UserLicence.query.filter_by(user_id=user_id, licence_id=user_licence_info['licence_id']).first()
    if existing_licence:
        return {'error': 'User already has a licence with the same user_id and licence_id'}, 400

    # Create a new UserLicence instance
    user_licence = UserLicence(
        user = user,
        licence = licence,
        licence_number = user_licence_info['licence_number'],
        date_of_expiry = user_licence_info['date_of_expiry']
    )
    db.session.add(user_licence)
    db.session.commit()
    return UserLicenceSchema().dump(user_licence), 201


# Allows user to update their user_licence info
@user_licences_bp.route('/<int:licence_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_user_licence(licence_id):
    user_id = get_jwt_identity()
    stmt = db.select(UserLicence).filter_by(user_id=user_id, licence_id=licence_id)
    user_licence = db.session.scalar(stmt)
    user_licence_info = UserLicenceSchema().load(request.json)
    if user_licence:
        user_licence.licence_number = user_licence_info.get('licence_number', user_licence.licence_number)
        user_licence.description = user_licence_info.get('description', user_licence.description)
        user_licence.date_of_expiry = user_licence_info.get('date_of_expiry', user_licence.date_of_expiry)
        db.session.commit()
        return UserLicenceSchema().dump(user_licence)


# Allows admin to update users user_licence info
@user_licences_bp.route('/user/<int:user_id>/licence/<int:licence_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def admin_update_user_licence(user_id, licence_id):
    admin_required()
    stmt = db.select(UserLicence).filter_by(user_id=user_id, licence_id=licence_id)
    user_licence = db.session.scalar(stmt)
    user_licence_info = UserLicenceSchema().load(request.json)
    if user_licence:
        user_licence.licence_number =user_licence_info.get('licence_number', user_licence.licence_number)
        user_licence.description = user_licence_info.get('description', user_licence.description)
        user_licence.date_of_expiry = user_licence_info.get('date_of_expiry', user_licence.date_of_expiry)
        db.session.commit()
        return UserLicenceSchema().dump(user_licence)
    else:
        return {'error': 'User or licence not found'}, 404


# Allows user to delete user_licence
@user_licences_bp.route('/<int:licence_id>', methods=['DELETE'])
@jwt_required()
def delete_user_licence(licence_id):
    user_id = get_jwt_identity()
    stmt = db.select(UserLicence).filter_by(user_id=user_id, licence_id=licence_id)
    user_licence = db.session.scalar(stmt)
    if user_licence:
        db.session.delete(user_licence)
        db.session.commit()
        return {}, 200
    else:
        return {'error':'User licence not found'}, 404


# allows admin to delete a users user_licence
@user_licences_bp.route('user/<int:user_id>/licence/<int:licence_id>', methods=['DELETE'])
@jwt_required()
def admin_delete_user_course(user_id, licence_id):
    admin_required()
    stmt = db.select(UserLicence).filter_by(user_id=user_id, licence_id=licence_id)
    user_licence = db.session.scalar(stmt)
    if user_licence:
        db.session.delete(user_licence)
        db.session.commit()
        return {}, 200
    else:
        return {'error':'User licence not found'}, 404