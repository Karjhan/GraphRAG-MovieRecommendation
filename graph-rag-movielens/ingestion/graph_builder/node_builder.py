from db.neo4j.connection import Neo4jConnection


class NodeBuilder:

    def __init__(self):

        self.db = Neo4jConnection()

    def create_movie(self, movie):

        query = """
        MERGE (m:Movie {movieId:$movieId})
        SET m.title=$title,
            m.overview=$overview
        """

        self.db.query(query, movie)

    def create_genre(self, genre):

        query = """
        MERGE (g:Genre {name:$name})
        """

        self.db.query(query, {"name": genre})