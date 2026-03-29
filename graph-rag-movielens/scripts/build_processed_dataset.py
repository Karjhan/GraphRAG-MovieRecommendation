import json
import pandas as pd
from tqdm import tqdm
import ollama
import pyarrow as pa
import pyarrow.parquet as pq
from pathlib import Path
import math
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_DIR = Path(__file__).resolve().parents[1]

MOVIES_PATH = BASE_DIR / "data/raw/archive/movie.csv"
ENRICH_PATH = BASE_DIR / "data/external/tmdb_enrichment.json"

OUTPUT_MOVIES = BASE_DIR / "data/processed/movies_clean.csv"
OUTPUT_EMBED = BASE_DIR / "data/processed/embeddings.parquet"

EMBED_MODEL = "bge-m3"

MAX_WORKERS = 12

print("Loading datasets...")

movies = pd.read_csv(MOVIES_PATH)
enrichment = json.load(open(ENRICH_PATH))
enrichment_clean = {int(float(k)): v for k, v in enrichment.items()}
records = []

print("Cleaning movies")

for _, row in movies.iterrows():
    movie_id = row.movieId
    enrich = enrichment_clean.get(movie_id, {})
    overview = enrich.get("overview", "")

    if overview is None or (isinstance(overview, float) and math.isnan(overview)):
        overview = ""

    genres = row.genres.split("|") if isinstance(row.genres, str) else []
    genres_clean = [g.strip() for g in genres if g.strip()]
    if not overview and len(genres_clean) == 0:
        continue

    text = f"""
Title: {row.title}
Genres: {', '.join(genres_clean)}
Overview: {overview}
""".strip()
    text = text[:1500]
    records.append({
        "movieId": int(row.movieId),
        "title": row.title,
        "genres": "|".join(genres_clean),
        "overview": overview,
        "embedding_text": text
    })

df = pd.DataFrame(records)
print(f"Remaining movies after filtering: {len(df)}")
OUTPUT_MOVIES.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT_MOVIES, index=False)
print("Saved cleaned movie dataset")

def embed_movie(row):
    text = row.embedding_text
    movie_id = row.movieId

    for _ in range(3):
        try:
            response = ollama.embeddings(
                model=EMBED_MODEL,
                prompt=text
            )
            return {
                "movieId": movie_id,
                "embedding": response["embedding"]
            }
        except Exception as e:
            time.sleep(0.5)

    print(f"Failed embedding movie {movie_id}")
    return None


print("Generating embeddings (parallel)...")
embeddings = []

with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    futures = [executor.submit(embed_movie, row) for _, row in df.iterrows()]
    for future in tqdm(as_completed(futures), total=len(futures)):
        result = future.result()
        if result:
            embeddings.append(result)

embed_df = pd.DataFrame(embeddings)
table = pa.Table.from_pandas(embed_df)
pq.write_table(table, OUTPUT_EMBED)
print("Embeddings saved")
print("Dataset build complete")