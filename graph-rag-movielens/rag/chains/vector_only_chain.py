from rag.retrievers.vector_metadata_retriever import vector_with_metadata
from rag.context_builder import build_context
from rag.prompts.vector_only_prompt import vector_only_prompt
from rag.services.llm_service import llm

def vector_only_chain(question):
    rows = vector_with_metadata(question)
    context = build_context(rows)

    return llm.invoke(
        vector_only_prompt.format(
            context=context,
            question=question
        )
    )