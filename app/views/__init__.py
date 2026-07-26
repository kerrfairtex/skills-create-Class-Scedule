from flask import Blueprint

bp = Blueprint('views', __name__)

from app.views import routes  # noqa: E402, F401
