from flask import Flask
from .extensions import db, socketio, migrate
from .routes import main_bp
from .sockets import register_socketio_handlers

def create_app():
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config.from_object("config.Config")

    db.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app)

    app.register_blueprint(main_bp)
    register_socketio_handlers()

    return app

    