from flask import Blueprint

recommend_dp = Blueprint('recommendResult', __name__, url_prefix='/recommendResult')
from . import views