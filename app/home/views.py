from flask import render_template, redirect
from flask_login import login_required

from . import home
from .. import db

@home.route('/')
@home.route('/index')
def homepage():
    """
    Handles requests to `/` and `/index` routes
    It's the landing page, index page, homepage or whatever you like to call it
    """
    return render_template("home/index.html", title="Homepage")


@home.route('/dashboard')
@login_required
def dashboard():
    """
    Handles requests to `/dashboard` route
    It's the first page that's seen after login
    """
    return render_template("home/dashboard.html", title='Dashboard')
