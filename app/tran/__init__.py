from flask import Blueprint

tran = Blueprint('tran', __name__)

from . import views
