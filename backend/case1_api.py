"""Backend-only API routes for the Case 1 LangChain workflow."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.dataset_catalog import DATASET_DEFINITIONS

router = APIRouter(prefix="/api/case1", tags=["Case 1 AI Backend"])


class Case1QueryRequest(BaseModel):
    query: str = Field(min_length=1, max_length=4000)
    dataset_id: str | None = Field(default=None, max_length=64)


class Case1OPLRequest(BaseModel):
    session_text: str = Field(min_length=1, max_length=24000)


@router.post("/query")
def query_case1(request: Case1QueryRequest):
    from backend.case1_agent import answer_case1_query

    if request.dataset_id and request.dataset_id not in {
        dataset["dataset_id"] for dataset in DATASET_DEFINITIONS
    }:
        raise HTTPException(status_code=400, detail="Selected dataset is not available in the catalog.")
    try:
        return answer_case1_query(request.query, dataset_id=request.dataset_id)
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    except RuntimeError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error
    except ImportError as error:
        raise HTTPException(status_code=503, detail="Install the Case 1 backend dependencies from requirements.txt.") from error


@router.post("/opl")
def generate_case1_opl(request: Case1OPLRequest):
    from backend.case1_opl import generate_opl

    try:
        return {"opl": generate_opl(request.session_text)}
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    except RuntimeError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error
    except ImportError as error:
        raise HTTPException(status_code=503, detail="Install the Case 1 backend dependencies from requirements.txt.") from error