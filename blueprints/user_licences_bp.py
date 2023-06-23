from flask import Blueprint, request
from models.user_licence import UserLicence, UserLicenceSchema
from init import db
from flask_jwt_extended import jwt_required
from blueprints.auth_bp import admin_required


user_licences_bp = Blueprint('user_licences', __name__, url_prefix='/user_licences')

@user_licences_bp.route('/')
@jwt_required()
def all_user_licences():
    # select * from licences;
    stmt = db.select(UserLicence)
    user_licences = db.session.scalars(stmt).all()
    return UserLicenceSchema(many=True).dump(user_licences)