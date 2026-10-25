"""Anthropic LLM Layer for Answer Rephrasing.

=============================================================================
VIVA / ORAL EXAM CHEAT-SHEET:
- Grounding & Anti-Hallucination:
  The LLM is strictly constrained via prompt engineering to ONLY rephrase
  or synthesize verified FAQ snippets retrieved in the context window.
- Graceful Degradation:
  If ANTHROPIC_API_KEY is omitted, the chatbot operates 100% deterministically
  and for free using direct retrieval.
- Viva Point: Why not let the LLM answer freely?
  Because LLMs hallucinate policies, dates, and fee amounts. RAG with strict
  grounding ensures administrative accuracy.
=============================================================================
"""

import os
from typing import List, Dict, Any, Optional

DEFAULT_MODEL = "claude-haiku-5-5"


def is_llm_enabled() -> bool:
    """Check if Anthropic API key is configured."""
    key = os.getenv("ANTHROPIC_API_KEY", "").strip()
    return bool(key)


def rephrase_with_llm(
    query: str,
    top_faqs: List[Dict[str, Any]],
    model_name: Optional[str] = None
) -> Optional[str]:
    """Rephrase verified FAQ answers using Anthropic Claude.

    Returns:
        Rephrased response string if successful, or None to fall back to direct retrieval.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY", "").strip()
    if not api_key:
        return None

    target_model = model_name or os.getenv("ANTHROPIC_MODEL", DEFAULT_MODEL)

    try:
        import anthropic

        client = anthropic.Anthropic(api_key=api_key)

        # Build clean grounded context from top FAQs
        context_blocks = []
        for i, faq in enumerate(top_faqs, 1):
            context_blocks.append(
                f"[Document {i}] ({faq['category']})\nQuestion: {faq['question']}\nAnswer: {faq['answer']}"
            )
        context_str = "\n\n".join(context_blocks)

        system_instruction = (
            "You are the official College FAQ Assistant. Your role is to answer student questions "
            "politely and clearly using ONLY the verified college FAQ context provided below.\n\n"
            "STRICT RULES:\n"
            "1. Answer using ONLY information found directly in the provided FAQ context.\n"
            "2. If the context does not contain the answer, reply EXACTLY: 'I'm sorry, but our official "
            "college documents do not contain that information. Please contact the administrative office.'\n"
            "3. Do NOT make up any dates, fee figures, percentages, or college policies.\n"
            "4. Keep your answer concise, conversational, and direct."
        )

        user_content = (
            f"VERIFIED FAQ CONTEXT:\n{context_str}\n\n"
            f"STUDENT QUERY: {query}\n\n"
            "Provide the answer strictly based on the context above:"
        )

        response = client.messages.create(
            model=target_model,
            max_tokens=400,
            temperature=0.0,  # Zero temperature for deterministic adherence to context
            system=system_instruction,
            messages=[{"role": "user", "content": user_content}]
        )

        if response.content and len(response.content) > 0:
            return response.content[0].text.strip()
        return None

    except Exception as e:
        print(f"[LLM Warning] Anthropic API call failed ({e}). Falling back to direct retrieval.")
        return None
