""" A FastAPI app used to create an OpenAPI document for end-to-end testing """
import json
from enum import Enum
from pathlib import Path
from typing import List

from fastapi import APIRouter, FastAPI, Query
from pydantic import BaseModel

app = FastAPI(title="My Test API", description="An API for testing openapi-python-client",)


class _ABCResponse(BaseModel):
    success: bool


@app.get("/ping", response_model=_ABCResponse)
async def ping():
    """ A quick check to see if the system is running """
    return {"success": True}


test_router = APIRouter()


class AnEnum(Enum):
    """ For testing Enums in all the ways they can be used """

    FIRST_VALUE = "FIRST_VALUE"
    SECOND_VALUE = "SECOND_VALUE"


class OtherModel(BaseModel):
    """ A different model for calling from TestModel """

    a_value: str


class AModel(BaseModel):
    """ A Model for testing all the ways custom objects can be used """

    an_enum_value: AnEnum
    a_list_of_enums: List[AnEnum]
    a_list_of_strings: List[str]
    a_list_of_objects: List[OtherModel]


@test_router.get("/", response_model=List[AModel])
def get_list(statuses: List[AnEnum] = Query(...),):
    """ Get users, filtered by statuses """
    return


app.include_router(test_router, prefix="/tests", tags=["users"])

if __name__ == "__main__":
    path = Path(__file__).parent / "openapi.json"
    path.write_text(json.dumps(app.openapi()))
