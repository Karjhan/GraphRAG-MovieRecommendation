from tqdm import tqdm
from ingestion.loaders.movielens_loader import load_movies, load_embeddings
from ingestion.graph_builder.node_builder import NodeBuilder
from ingestion.graph_builder.relationship_builder import RelationshipBuilder
from ingestion.embeddings.embedding_pipeline import create_collection, upload_embeddings
from ingestion.graph_builder.schema import CREATE_INDEXES
from db.neo4j.connection import Neo4jConnection


def run_ingestion():

    db = Neo4jConnection()

    print("Creating schema")

    for q in CREATE_INDEXES:
        db.query(q)

    movies = load_movies()

    node_builder = NodeBuilder()
    rel_builder = RelationshipBuilder()

    print("Ingesting movies")

    for _, row in tqdm(movies.iterrows(), total=len(movies)):

        node_builder.create_movie({
            "movieId": int(row.movieId),
            "title": row.title,
            "overview": row.overview
        })

        genres = row.genres.strip("[]").replace("'", "").split(",")

        for g in genres:

            g = g.strip()

            if not g:
                continue

            node_builder.create_genre(g)
            rel_builder.link_movie_genre(row.movieId, g)

    print("Uploading embeddings")

    embed_df = load_embeddings()

    vector_size = len(embed_df.iloc[0].embedding)

    create_collection(vector_size)

    upload_embeddings(embed_df)

    print("Ingestion complete")