from db.neo4j.connection import Neo4jConnection

db = Neo4jConnection()

def run_cypher(query, params=None):
    if params is None:
        params = {}
    return db.query(query, params)

def get_movies_basic(movie_ids):
    query = """
    MATCH (m:Movie)
    WHERE m.movieId IN $ids
    OPTIONAL MATCH (m)-[:HAS_GENRE]->(g:Genre)
    RETURN m.movieId as movieId,
           m.title as title,
           collect(g.name) as genres
    """
    return db.query(query, {"ids": movie_ids})