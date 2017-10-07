from flask_login import login_required, login_user, logout_user
from flask import redirect, url_for, flash, render_template

from . import auth
from .forms import LoginForm, RegistrationForm
from .. import db
from ..models import User, Account


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle requests to `/login` route
    Log a user in through the login form
    """
    form = LoginForm()
    if form.validate_on_submit():

        # Check whether the user exists in the database
        # and if the provided password is correct
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            flash('Welcome again, {}!'.format(user.username), 'success')
            return redirect(url_for('home.dashboard'))
        else:
            flash('Invalid username or password', 'error')

    # Load login template
    return render_template('auth/login.html', form=form, title='Login')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle requests to `/register` route
    Add a user to database
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.flush()

        default_account = Account(user_id=user.id)
        db.session.add(default_account)
        db.session.commit()

        flash('You have successfully registered! You may now login.')

        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form, title='Register')


@auth.route('/logout')
@login_required
def logout():
    """
    Handle requests to `/logout` route
    Logout a user from session
    """
    logout_user()
    flash('You have been successfully logged out')
    return redirect(url_for('auth.login'))
