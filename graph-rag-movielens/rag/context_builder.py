def build_context(graph_results):
    context = ""

    for r in graph_results:
        context += f"Movie: {r.get('title')}\n"

        if r.get("genres"):
            context += f"Genres: {', '.join(r['genres'])}\n"

        if r.get("similar_movies"):
            context += f"Similar Movies: {', '.join(r['similar_movies'])}\n"

        if r.get("shared_genres"):
            context += f"Shared Genres: {', '.join(r['shared_genres'])}\n"

        context += "\n"

    return context