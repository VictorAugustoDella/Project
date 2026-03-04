from flask import Blueprint

price_bp = Blueprint('price', __name__, url_prefix='/api/v1')

from . import price_routes