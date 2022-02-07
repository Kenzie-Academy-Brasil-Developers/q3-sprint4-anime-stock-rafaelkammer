from app.models import DatabaseConnector
from psycopg2 import sql

class Animes(DatabaseConnector):
    def __init__(self, *args, **kwargs):
        self.anime = kwargs["anime"].title()
        self.seasons = kwargs["seasons"]
        self.released_date = kwargs["released_date"]

    def create(self):

        self.get_conn_cur()

        query = """
            INSERT INTO
                animes (anime, seasons, released_date)
            VALUES
                (%s, %s, %s)
            RETURNING *
        """

        query_values = list(self.__dict__.values())

        self.cur.execute(query, query_values)

        inserted_anime = self.cur.fetchone()

        self.commit_and_close()

        return inserted_anime

    @classmethod
    def animes(cls):
        cls.get_conn_cur()

        create_db_query = """
        CREATE TABLE IF NOT EXISTS animes (
                id              BIGSERIAL PRIMARY KEY,
                anime           VARCHAR(100) NOT NULL UNIQUE, 
                released_date   DATE NOT NULL,
                seasons         INTEGER NOT NULL
            );
        """

        cls.cur.execute(create_db_query)

        query = "SELECT * FROM animes;"

        cls.cur.execute(query)

        animes = cls.cur.fetchall()

        cls.commit_and_close()

        return animes

    @classmethod
    def select_by_id(cls, anime_id: int):
        cls.get_conn_cur()

        query = "SELECT * FROM animes WHERE id = (%s)"

        cls.cur.execute(query, (anime_id,))

        anime = cls.cur.fetchone()

        cls.commit_and_close()

        return anime
    
    @classmethod
    def update_by_id(cls, anime_id: int, payload):
        cls.get_conn_cur()

        for key in payload.keys():
            if key not in ["anime", "released_date", "seasons"]:
                raise KeyError

        columns = [sql.Identifier(key) for key in payload.keys()]
        values = [sql.Literal(value) for value in payload.values()]

        query = sql.SQL(
            """
                UPDATE
                    animes
                SET
                    ({columns}) = ROW({values})
                WHERE
                    id={id}
                RETURNING *
            """
        ).format(
            id=sql.Literal(anime_id),
            columns=sql.SQL(",").join(columns),
            values=sql.SQL(",").join(values),
        )

        cls.cur.execute(query)
        updated_user = cls.cur.fetchone()

        cls.commit_and_close()

        return updated_user

    @classmethod
    def delete_by_id(cls, anime_id: int):
        cls.get_conn_cur()

        query = "DELETE FROM animes WHERE id = (%s) RETURNING *"

        cls.cur.execute(query, (anime_id,))

        anime = cls.cur.fetchone()

        cls.commit_and_close()

        return anime