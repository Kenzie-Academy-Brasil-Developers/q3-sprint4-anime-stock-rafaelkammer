from flask import Flask, Blueprint
from app.controllers import animes_controller

bp = Blueprint("animes", __name__, url_prefix="/animes")

bp.get("")(animes_controller.get_all_animes)
bp.post("")(animes_controller.create_anime)
bp.get("<int:anime_id>")(animes_controller.get_anime_by_id)
bp.patch("<int:anime_id>")(animes_controller.update_anime_by_id)
bp.delete("<int:anime_id>")(animes_controller.delete_anime_by_id)