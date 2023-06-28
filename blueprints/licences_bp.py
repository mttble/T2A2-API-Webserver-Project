from flask import Blueprint, request
from models.licence import Licence, LicenceSchema
from init import db
from flask_jwt_extended import jwt_required
from blueprints.auth_bp import admin_required
from datetime import date

# auth route url is defined in the blueprint which is registered in main.
licences_bp = Blueprint('licences', __name__, url_prefix='/licences')


# allows users to get all licenses
@licences_bp.route('/')
@jwt_required()
def all_licences():
    # retrieves all existing licences using the select function to select class Licence
    stmt = db.select(Licence)
    # sessions object handles the database and scalars filters result into rows.
    licences = db.session.scalars(stmt).all()
    # The LicenceSchema and dump converts results into JSON to be displayed
    return LicenceSchema(many=True).dump(licences)


# Allows admin to add licences
@licences_bp.route('/', methods=['POST'])
@jwt_required()
def create_licence():
    admin_required()
    licence_info = LicenceSchema().load(request.json)
    licence = Licence(
        title = licence_info['title']
    )
    db.session.add(licence)
    db.session.commit()
    return LicenceSchema().dump(licence), 201


# Allows admin to delete licences
@licences_bp.route('/<int:licence_id>', methods=['DELETE'])
@jwt_required()
def delete_course(licence_id):
    admin_required()
    stmt = db.select(Licence).filter_by(id=licence_id)
    licence = db.session.scalar(stmt)
    if licence:
        db.session.delete(licence)
        db.session.commit()
        return {}, 200
    else:
        return {'error':'Licence not found'}, 404