from flask import Blueprint

movies_dp = Blueprint('movie', __name__, url_prefix='/movieInfo')
from . import views