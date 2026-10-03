"""Environment-based Groq configuration with explicit transfer consent."""

import os


_ENABLED_VALUES = {"1", "true", "yes", "on"}
DEFAULT_GROQ_MODEL = "qwen/qwen3.8-27b"


def groq_processing_enabled() -> bool:
    """Return whether Groq processing was explicitly enabled by the operator."""
    return (
        os.getenv("CALIBER_ALLOW_GROQ_PROCESSING", "").strip().lower()
        in _ENABLED_VALUES
    )


def get_groq_api_key() -> str:
    """Return the configured Groq key only when transfer consent is enabled."""
    if not groq_processing_enabled():
        raise RuntimeError(
            "Groq processing is disabled. Set CALIBER_ALLOW_GROQ_PROCESSING=true "
            "only after authorizing transfer of query and retrieved excerpts."
        )

    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("Set GROQ_API_KEY to enable Groq processing.")
    return api_key


def get_groq_model() -> str:
    """Return the configured Groq model, or the current recommended default."""
    model = os.getenv("GROQ_MODEL", DEFAULT_GROQ_MODEL).strip()
    if not model:
        raise RuntimeError("GROQ_MODEL cannot be empty.")
    return model
