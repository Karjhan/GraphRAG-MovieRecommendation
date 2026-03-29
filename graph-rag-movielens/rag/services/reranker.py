from rag.services.llm_service import llm
from rag.prompts.rerank_prompt import rerank_prompt

def score_movie(query, movie_text):
    response = llm.invoke(
        rerank_prompt.format(query=query, movie=movie_text)
    )
    text = response.content if hasattr(response, "content") else str(response)
    try:
        return float(text.strip())
    except:
        return 0.0


def rerank_results(query, rows, top_k=5):
    scored = []
    for r in rows:
        movie_text = f"{r.get('title', '')} {', '.join(r.get('genres', []))}"
        score = score_movie(query, movie_text)
        scored.append((score, r))

    scored.sort(key=lambda x: x[0], reverse=True)

    return [r for _, r in scored[:top_k]]

def rerank_movies(query, movies, top_k=5):
    scored = []
    for m in movies:
        text = f"{m['title']} | Genres: {', '.join(m['genres'])}"
        response = llm.invoke(
            rerank_prompt.format(query=query, movie=text)
        )

        content = response.content if hasattr(response, "content") else str(response)
        try:
            score = float(content.strip())
        except:
            score = 0.0
        scored.append((score, m))

    scored.sort(reverse=True, key=lambda x: x[0])
    return [m for _, m in scored[:top_k]]