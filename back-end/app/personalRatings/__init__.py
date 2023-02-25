from flask import Blueprint

pr_dp = Blueprint('personalRatings', __name__, url_prefix='/personalRatings')
from . import views
