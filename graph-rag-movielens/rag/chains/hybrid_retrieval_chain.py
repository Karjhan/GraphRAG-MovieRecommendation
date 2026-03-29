from rag.retrievers.hybrid_retriever import hybrid_search
from rag.context_builder import build_context
from rag.prompts.vector_answer_prompt import vector_answer_prompt
from rag.services.llm_service import llm
from rag.services.response_guard import filter_to_context

def hybrid_chain(question):
    rows = hybrid_search(question)
    context = build_context(rows)

    response = llm.invoke(
        vector_answer_prompt.format(
            context=context,
            question=question
        )
    )
    raw_answer = response.content if hasattr(response, "content") else str(response)

    return filter_to_context(raw_answer, context)