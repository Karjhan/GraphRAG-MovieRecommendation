from db.neo4j.connection import Neo4jConnection


class RelationshipBuilder:

    def __init__(self):

        self.db = Neo4jConnection()

    def link_movie_genre(self, movie_id, genre):

        query = """
        MATCH (m:Movie {movieId:$movieId})
        MATCH (g:Genre {name:$genre})

        MERGE (m)-[:HAS_GENRE]->(g)
        """

        self.db.query(query, {
            "movieId": movie_id,
            "genre": genre
        })