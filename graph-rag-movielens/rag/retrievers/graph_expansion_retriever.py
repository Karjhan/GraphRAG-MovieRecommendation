from db.neo4j.connection import Neo4jConnection

db = Neo4jConnection()

def expand_from_movies(movie_ids, limit_per_movie=5):
    query = """
    MATCH (m:Movie)
    WHERE m.movieId IN $ids
    
    MATCH (m)-[:HAS_GENRE]->(g:Genre)<-[:HAS_GENRE]-(rec:Movie)
    WHERE rec.movieId <> m.movieId
    
    WITH m, g, rec
    RETURN 
        m.title as title,
        collect(DISTINCT g.name) as genres,
        collect(DISTINCT rec.title)[0..5] as similar_movies,
        collect(DISTINCT g.name) as shared_genres
    """

    return db.query(query, {
        "ids": movie_ids,
        "limit": limit_per_movie
    })