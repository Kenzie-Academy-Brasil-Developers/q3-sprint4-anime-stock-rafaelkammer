from flask import Blueprint, Flask

from app.routes.animes_route import bp as bp_anime

bp_api = Blueprint("api", __name__, url_prefix="")


def init_app(app: Flask):

    bp_api.register_blueprint(bp_anime)

    app.register_blueprint(bp_api)
