from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from models.database import db


def create_app():
    app = Flask(__name__)
    # db stuff (SQLite)
    # use some config file here
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'some-secret-string'
    db.init_app(app)  # CAN WE DO THAT???

    @app.route('/')
    def index():
        return jsonify({"message": "Hello, World!"})

    return app


def setup_database(app):
    with app.app_context():  # CAN WE DO THAT???
        @app.before_first_request
        def create_tables():
            db.create_all()


def setup_jwt(app):
    app.config['JWT_SECRET_KEY'] = 'jwt-secret-key'
    jwt = JWTManager(app)

    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

    # DO IT SOMEPLACE HIGHER???
    from models.revoked_token_model import RevokedTokenModel
    # WHERE SHOULD THIS BE???

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return RevokedTokenModel.is_jti_blacklisted(jti)


if __name__ == "__main__":
    app = create_app()
    setup_database(app)
    setup_jwt(app)

    # adding resources. Do that AFTER setup_database()
    from views.manage_blueprints import users, add_users_routes
    add_users_routes()  # creates it's own api and adds it there
    app.register_blueprint(users)  # blueprint connects that api and app

    app.run(debug=True)
