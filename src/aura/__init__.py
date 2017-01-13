from flask import Flask

from database.model import db
from home.views import home
from insta.views import insta
from admin.views import register_admin
from auth.views import load_auth


class Aura(object):
    app = None

    def register_blueprint(self, app):
        app.register_blueprint(home)
        app.register_blueprint(insta)
        register_admin(app)
        load_auth(app)

    def create_app(self, config):
        if self.app:
            return self.app

        app = Flask(__name__)
        app.config.from_object(config)

        db.init_app(app)
        db.create_all(app=app)
        app.db = db

        self.register_blueprint(app)
        self.app = app

        return app

app = Aura.app
