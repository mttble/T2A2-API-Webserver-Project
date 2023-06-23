from flask import Blueprint
from models.licence import Licence, LicenceSchema
from init import db
from flask_jwt_extended import jwt_required
from datetime import date

licences_bp = Blueprint('licences', __name__, url_prefix='/licences')

@licences_bp.route('/')
@jwt_required()
def all_licences():
    # select * from cards;
    stmt = db.select(Licence)
    licences = db.session.scalars(stmt).all()
    return LicenceSchema(many=True).dump(licences)