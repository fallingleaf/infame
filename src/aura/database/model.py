from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()


class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                                onupdate=db.func.current_timestamp())


class User(Base):
    __tablename__ = 'auth_user'

    name = db.Column(db.String(128), nullable=False)

    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(192), nullable=False)

    role = db.Column(db.SmallInteger, nullable=False)
    status = db.Column(db.SmallInteger, nullable=False)

    is_active = db.Column(db.Boolean, default=False)
    is_authenticated = db.Column(db.Boolean, default=False)
    is_anynomous = db.Column(db.Boolean, default=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.set_password(password)

    def set_password(self, passwd):
        self.password = generate_password_hash(passwd)

    def check_password(self, passwd):
        return check_password_hash(self.password, passwd)

    def __repr__(self):
        return '<User %r>' % self.name

    def get_id(self):
        return self.email
