from flask import Blueprint, request
from models.user_licence import UserLicence, UserLicenceSchema
from models.licence import Licence, LicenceSchema
from models.user import User
from init import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from blueprints.auth_bp import admin_required


user_licences_bp = Blueprint('user_licences', __name__, url_prefix='/user_licences')

@user_licences_bp.route('/')
@jwt_required()
def all_user_licences():
    # select * from licences;
    stmt = db.select(UserLicence)
    user_licences = db.session.scalars(stmt).all()
    return UserLicenceSchema(many=True).dump(user_licences)

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

    # Create a new UserLicence instance
    user_licence = UserLicence(
        user = user,
        licence =licence,
        licence_number = user_licence_info['licence_number'],
        date_of_expiry = user_licence_info['date_of_expiry']
    )

    # Add the user_licence to the session
    db.session.add(user_licence)
    db.session.commit()
    return UserLicenceSchema().dump(user_licence), 201