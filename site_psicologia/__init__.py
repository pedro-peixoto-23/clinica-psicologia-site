from flask import Flask
from config import Config


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    from site_psicologia.main.routes import main
    from site_psicologia.users.routes import users
    from site_psicologia.employees.routes import employees
    from site_psicologia.manager.routes import manager

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(employees)
    app.register_blueprint(manager)

    return app
