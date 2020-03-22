""" A FastAPI app used to create an OpenAPI document for end-to-end testing """
import json
from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="My Test API", description="An API for testing openapi-python-client",)


class _ABCResponse(BaseModel):
    success: bool


@app.get("/ping", response_model=_ABCResponse)
async def ping():
    """ A quick check to see if the system is running """
    return {"success": True}


if __name__ == "__main__":
    path = Path(__file__).parent / "openapi.json"
    path.write_text(json.dumps(app.openapi()))
