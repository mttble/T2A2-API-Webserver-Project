from flask import Blueprint, request
from models.licence import Licence, LicenceSchema
from init import db
from flask_jwt_extended import jwt_required
from blueprints.auth_bp import admin_required
from datetime import date

licences_bp = Blueprint('licences', __name__, url_prefix='/licences')

@licences_bp.route('/')
@jwt_required()
def all_licences():
    # select * from cards;
    stmt = db.select(Licence)
    licences = db.session.scalars(stmt).all()
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