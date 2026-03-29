import os
import json
import time
import requests
import pandas as pd
from tqdm import tqdm
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

RAW_PATH = BASE_DIR / "data/raw/archive/link.csv"
OUTPUT_PATH = BASE_DIR / "data/external/tmdb_enrichment.json"

API_KEY = os.getenv("TMDB_API_KEY")

BASE_URL = "https://api.themoviedb.org/3/movie"

links = pd.read_csv(RAW_PATH)

results = {}

for _, row in tqdm(links.iterrows(), total=len(links)):

    tmdb_id = row["tmdbId"]
    movie_id = row["movieId"]

    if pd.isna(tmdb_id):
        continue

    url = f"{BASE_URL}/{int(tmdb_id)}?api_key={API_KEY}&language=en-US"

    try:
        r = requests.get(url)
        if r.status_code != 200:
            continue

        data = r.json()

        results[movie_id] = {
            "tmdb_id": tmdb_id,
            "overview": data.get("overview"),
            "release_date": data.get("release_date"),
            "runtime": data.get("runtime"),
            "vote_average": data.get("vote_average"),
            "vote_count": data.get("vote_count"),
            "genres": [g["name"] for g in data.get("genres", [])],
            "keywords": [],
            "production_companies": [
                c["name"] for c in data.get("production_companies", [])
            ]
        }

        time.sleep(0.05)

    except Exception as e:
        print("error", e)

with open(OUTPUT_PATH, "w") as f:
    json.dump(results, f)

print("TMDB enrichment saved")