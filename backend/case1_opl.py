"""Generate a standardized English One Point Lesson from a chat session."""

from textwrap import dedent


OPL_TEMPLATE = dedent("""\
    ONE POINT LESSON (OPL)
    Title:
    Equipment:
    Objective:
    Safety precautions:
    Tools and materials:
    Procedure / Steps:
    Common issues and troubleshooting:
    Key learning points:
    Source references:
    """)


def generate_opl(session_text: str) -> str:
    """Summarize only the supplied session; mark absent facts as not stated."""
    session_text = session_text.strip()
    if not session_text:
        raise ValueError("Session text is required to generate an OPL.")

    from backend.case1_agent import groq_api_key
    from backend.config_groq import get_groq_model

    api_key = groq_api_key()
    from langchain_groq import ChatGroq

    model = ChatGroq(
        model=get_groq_model(),
        temperature=0,
        api_key=api_key,
    )
    prompt = (
        "Summarize the following troubleshooting session as an English One Point "
        "Lesson (OPL). Preserve industrial technical terms such as troubleshooting, "
        "start-up, RCA, and P&ID. Use the section headings below exactly and number "
        "the steps. Do not add facts or safety procedures that are not stated in the "
        "session; write 'Not stated in the session' when information is unavailable.\n\n"
        f"{OPL_TEMPLATE}\n"
        "Troubleshooting session:\n"
        f"{session_text[:24000]}"
    )
    try:
        response = model.invoke(prompt)
    except Exception as error:
        raise RuntimeError("Groq request failed; no OPL was generated.") from error
    return str(response.content).strip()