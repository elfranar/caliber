# backend/groq_helper.py
"""
Groq Cloud LLM integration for CALIBER AI pipeline.
Provides a simple interface to call Groq's LLM API for:
  - RAG-grounded answer generation
  - Critical thinking / multi-step reasoning
  - OPL document generation
"""

from typing import Optional, List, Dict

from groq import Groq
from backend.config_groq import get_groq_api_key, get_groq_model


def _get_client() -> Groq:
    """Initialize the Groq client from explicitly consented environment config."""
    return Groq(api_key=get_groq_api_key())


def _check_consent() -> None:
    """Ensure Groq processing consent is explicitly enabled."""
    get_groq_api_key()


def groq_chat(
    prompt: str,
    model: Optional[str] = None,
    temperature: float = 0.3,
    max_tokens: int = 1024,
    system_prompt: Optional[str] = None,
) -> str:
    """
    Send a single-turn chat to Groq and return the assistant's text.
    
    Args:
        prompt: The user's question/prompt.
        model: Groq model ID (defaults to GROQ_MODEL or openai/gpt-oss-120b).
        temperature: Sampling temperature (lower = more deterministic).
        max_tokens: Maximum tokens in the response.
        system_prompt: Optional system instruction for the model.
    
    Returns:
        The model's response text.
    """
    _check_consent()
    client = _get_client()
    model = model or get_groq_model()

    messages: List[Dict[str, str]] = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_completion_tokens=max_tokens,
    )
    return response.choices[0].message.content


def groq_rag_answer(
    question: str,
    context_chunks: List[str],
    model: Optional[str] = None,
    temperature: float = 0.2,
    max_tokens: int = 1500,
) -> Dict[str, str]:
    """
    Generate a RAG-grounded answer using Groq.
    
    The model receives retrieved document chunks as context and must
    answer ONLY based on the provided evidence. This enforces grounded,
    citation-backed responses.
    
    Args:
        question: The engineer's technical question.
        context_chunks: List of retrieved text chunks from vector search.
        model: Groq model ID.
        temperature: Sampling temperature.
        max_tokens: Max response tokens.
    
    Returns:
        Dict with 'answer', 'model', and 'generation_mode' keys.
    """
    _check_consent()
    model = model or get_groq_model()

    # Build the context block
    context_block = "\n\n---\n\n".join(
        f"[Dokumen {i+1}]\n{chunk}" for i, chunk in enumerate(context_chunks)
    )

    system_prompt = """You are an AI Technical Assistant for PT Chandra Asri Pacific Tbk.
Your task is to answer technical questions ONLY based on the provided context documents.

STRICT RULES:
1. Answer ONLY using information from the context documents below.
2. If information is absent from the context, clearly say that it was not found.
3. Cite relevant document numbers (e.g., [Document 1], [Document 2]).
4. Respond in clear, formal, technical English.
5. If safety (HSE) procedures are relevant, ALWAYS mention them first.
6. Structure the answer so it is easy for a plant engineer to understand.
7. Never invent information that is not in the context."""

    user_prompt = f"""CONTEXT DOCUMENTS:
{context_block}

ENGINEER'S QUESTION:
{question}

Provide an accurate technical answer based on the context above."""

    answer = groq_chat(
        prompt=user_prompt,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        system_prompt=system_prompt,
    )

    return {
        "answer": answer,
        "model": model,
        "generation_mode": "groq_rag_grounded",
    }


def groq_classify_query(query: str) -> str:
    """
    Classify the type of user query for the orchestrator router.
    Returns one of: 'document', 'maintenance', 'diagram', 'general'.
    """
    _check_consent()

    system_prompt = """Classify the following query into exactly one category.
Return ONLY the category name, nothing else.

Categories:
- document: Questions about SOPs, procedures, datasheets, technical documents
- maintenance: Questions about maintenance history, failure records, repair logs
- diagram: Questions about P&ID diagrams, process flow, piping, instrumentation
- general: General questions that don't fit the above categories"""

    result = groq_chat(
        prompt=f"Query: {query}",
        model=get_groq_model(),
        temperature=0.0,
        max_tokens=20,
        system_prompt=system_prompt,
    )
    
    category = result.strip().lower()
    valid_categories = {"document", "maintenance", "diagram", "general"}
    return category if category in valid_categories else "general"
