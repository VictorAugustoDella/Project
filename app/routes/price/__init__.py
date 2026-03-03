from flask import Blueprint

price_bp = Blueprint('price', __name__)

from . import price_routes