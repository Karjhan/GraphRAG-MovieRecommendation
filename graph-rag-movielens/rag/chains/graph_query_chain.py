from rag.prompts.cypher_prompt import cypher_prompt
from rag.retrievers.graph_retriever import run_cypher
from rag.context_builder import build_context
from rag.prompts.graph_answer_prompt import graph_answer_prompt
from rag.services.llm_service import llm
from rag.services.response_guard import filter_to_context

def graph_query(question):
    cypher = llm.invoke(cypher_prompt.format(question=question))
    rows = run_cypher(cypher)
    context = build_context(rows)

    response = llm.invoke(
        graph_answer_prompt.format(
            context=context,
            question=question
        )
    )
    raw_answer = response.content if hasattr(response, "content") else str(response)

    return filter_to_context(raw_answer, context)