from flask import Blueprint

users_dp = Blueprint('user', __name__, url_prefix='/userLibrary')
from . import views