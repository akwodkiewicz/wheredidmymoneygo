from flask import Blueprint

cat = Blueprint('cat', __name__)

from . import views