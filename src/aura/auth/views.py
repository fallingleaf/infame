from flask import (Blueprint, current_app, request, redirect, render_template,
                    flash, session, url_for,)

from werkzeug import check_password_hash, generate_password_hash

from flask_login import login_user, logout_user, login_required, current_user, LoginManager
from aura.database.model import User

from .forms import LoginForm, SignupForm


auth = Blueprint('auth', __name__, url_prefix='/auth')
login_manager = LoginManager()


def load_auth(app):
    app.register_blueprint(auth)

    # Set up login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please login to access this page'

    login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.first(email=user_id)


# @login_manager.request_loader
# def load_user_from_request(request):
#     api_key = request.args.get('api_key')
#     if api_key:
#         user = User.query.filter_by(api_key=api_key).first()
#         if user:
#             return user
#
#     api_key = request.headers.get('Authorization')
#     if api_key:
#         api_key = api_key.replace('Basic ', '', 1)
#         try:
#             api_key = base64.b64decode(api_key)
#         except TypeError:
#             pass
#         user = User.query.filter_by(api_key=api_key).first()
#         if user:
#             return user
#     return None



@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and user.check_password(form.password.data):
            if form.remember.data:
                login_user(user, remember=True)
            else:
                login_user(user)

            flash('Welcome %s' % user.name)
            next_url = request.args.get('next') or url_for('home.index')
            return redirect(next_url)

        flash('Wrong email or password', 'error-message')
    return render_template('auth/login.html', form=form)




@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home.index'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm(request.form)

    if form.validate_on_submit():
        user = User(form.username.data, form.email.data, form.password.data)

        # Hardcoded role, status, replace with flask principal
        user.role = 1
        user.status = 1

        db = current_app.db
        db.session.add(user)
        db.session.commit()

        login_user(user)
        return redirect(url_for('home.index'))

    return render_template('auth/signup.html', form=form)
