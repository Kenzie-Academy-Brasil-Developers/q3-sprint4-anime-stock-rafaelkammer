from xml.dom import WrongDocumentErr
from flask import jsonify, request
from http import HTTPStatus
from app.models.animes_model import Animes
from psycopg2.errors import UniqueViolation


def get_all_animes():
    animes = Animes.animes()

    anime_keys = ["id", "anime", "released_date", "seasons"]
    animes_list = [dict(zip(anime_keys, anime)) for anime in animes]

    return jsonify({"data": animes_list}), HTTPStatus.OK


def create_anime():
    Animes.animes()

    data = request.get_json()
   
    try:
        anime = Animes(**data)
        inserted_anime = anime.create()

    except UniqueViolation:
        return (
            jsonify({"error": "anime already exists"}),
            HTTPStatus.UNPROCESSABLE_ENTITY,
        )
    except KeyError:

        wrong_keys = []

        for key in data.keys():
            if key not in ["anime", "released_date", "seasons"]:
                wrong_keys.append(key)

        return (
            jsonify({"Available_keys": [
                "anime",
                "released_date",
                "seasons"
            ],
            "wrong_keys_sent":wrong_keys}
        ), HTTPStatus.UNPROCESSABLE_ENTITY)

    anime_keys = ["id", "anime", "released_date", "seasons"]
    inserted_anime = dict(zip(anime_keys, inserted_anime))

    return jsonify(inserted_anime), HTTPStatus.CREATED

def get_anime_by_id(anime_id: int):

    try:

        anime_values = Animes.select_by_id(anime_id)
        anime_keys = ["id", "anime", "released_date", "seasons"]

        anime = [dict(zip(anime_keys, anime_values))]

        return jsonify({"data": anime}), HTTPStatus.OK

    except:
        return (
            jsonify({"error": "Not found"}),
            HTTPStatus.NOT_FOUND
            )

def update_anime_by_id(anime_id: int):

    try:
        payload = request.get_json()

        updated_anime_values = Animes.update_by_id(anime_id, payload)
        anime_keys = ["id", "anime", "released_date", "seasons"]

        anime = [dict(zip(anime_keys, updated_anime_values))]

        return jsonify({"data": anime}), HTTPStatus.OK

    except KeyError:
        wrong_keys = []

        for key in payload.keys():
            if key not in ["anime", "released_date", "seasons"]:
                wrong_keys.append(key)

        return (
            jsonify({"Available_keys": [
                "anime",
                "released_date",
                "seasons"
            ],
            "wrong_keys_sent":wrong_keys}
        ), HTTPStatus.UNPROCESSABLE_ENTITY)

    except:
        return (
            jsonify({"error": "Not found"}),
            HTTPStatus.NOT_FOUND
            )

def delete_anime_by_id(anime_id: int):    

    deleted_anime = Animes.delete_by_id(anime_id)

    if not deleted_anime:
        return (
            jsonify({"error": "Not found"}),
            HTTPStatus.NOT_FOUND
            )

    return jsonify(deleted_anime), HTTPStatus.NO_CONTENT
