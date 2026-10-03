"""Application entry point for the Knowledge Hub."""

import os
from dotenv import load_dotenv

load_dotenv()

import uvicorn


def main() -> None:
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    display_host = "127.0.0.1" if host == "0.0.0.0" else host
    print(f"Knowledge Hub UI and API: http://{display_host}:{port}")
    print(f"Interactive API docs: http://{display_host}:{port}/docs")
    uvicorn.run("backend.main:app", host=host, port=port, reload=True)


if __name__ == "__main__":
    main()
