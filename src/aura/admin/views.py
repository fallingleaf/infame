from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from aura.database.model import db, User

def register_admin(app):
    admin = Admin(app, name='aura', template_mode='bootstrap3')
    admin.add_view(ModelView(User, db.session))
