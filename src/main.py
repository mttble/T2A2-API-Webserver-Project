from flask import Flask
from os import environ
from init import db, ma, bcrypt, jwt
from blueprints.cli_bp import cli_bp
from blueprints.auth_bp import auth_bp
from blueprints.courses_bp import courses_bp
from blueprints.licences_bp import licences_bp
from blueprints.user_courses_bp import user_courses_bp
from blueprints.user_licences_bp import user_licences_bp
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import DataError, IntegrityError


def setup():
    app = Flask(__name__)

    # retrieves key and DB_URI connection string from .env for database security
    app.config['JWT_SECRET_KEY'] = environ.get('JWT_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URI')

    # initialising these objects from init.py to be used in the app
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    
    # Error handlers below help handle errors gracefully by returning JSON responses
    @app.errorhandler(400)
    def bad_request(err):
        return {'error': str(err)}, 400
    
    @app.errorhandler(ValidationError)
    def validationerror(err):
        return {'error': str(err)}, 400
    
    @app.errorhandler(KeyError)
    def keyerror(err):
        missing_field = err
        error_message = f"Missing required field: {(missing_field)}"
        return {'error': error_message}, 400
    
    @app.errorhandler(401)
    def unauthorized(err):
        return {'error': str(err)}, 401
    
    @app.errorhandler(404)
    def not_found(err):
        return {'error': str(err)}, 404
    
    @app.errorhandler(405)
    def method_not_allowed(err):
        return {'error': str(err)}, 405
    
    @app.errorhandler(DataError)
    def handle_data_error(err):
        return {'error': str(err)}, 500
    
    @app.errorhandler(IntegrityError)
    def integrity_error(err):
        return {'error': str(err)}, 409
    
    # Registering the blueprints to be used in the app
    app.register_blueprint(cli_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(courses_bp)
    app.register_blueprint(licences_bp)
    app.register_blueprint(user_courses_bp)
    app.register_blueprint(user_licences_bp)

    return app