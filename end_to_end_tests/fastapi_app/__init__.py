""" A FastAPI app used to create an OpenAPI document for end-to-end testing """
import json
from datetime import date, datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Union

from fastapi import APIRouter, Body, FastAPI, File, Header, Query, UploadFile
from pydantic import BaseModel

app = FastAPI(title="My Test API", description="An API for testing openapi-python-client",)


@app.get("/ping", response_model=bool)
async def ping():
    """ A quick check to see if the system is running """
    return True


test_router = APIRouter()


class AnEnum(Enum):
    """ For testing Enums in all the ways they can be used """

    FIRST_VALUE = "FIRST_VALUE"
    SECOND_VALUE = "SECOND_VALUE"


class DifferentEnum(Enum):
    FIRST_VALUE = "DIFFERENT"
    SECOND_VALUE = "OTHER"


class OtherModel(BaseModel):
    """ A different model for calling from TestModel """

    a_value: str


class AModel(BaseModel):
    """ A Model for testing all the ways custom objects can be used """

    an_enum_value: AnEnum
    nested_list_of_enums: List[List[DifferentEnum]] = []
    some_dict: Dict[str, str]
    aCamelDateTime: Union[datetime, date]
    a_date: date


@test_router.get("/", response_model=List[AModel], operation_id="getUserList")
def get_list(
    an_enum_value: List[AnEnum] = Query(...), some_date: Union[date, datetime] = Query(...),
):
    """ Get a list of things """
    return


@test_router.post("/upload")
async def upload_file(some_file: UploadFile = File(...), keep_alive: bool = Header(None)):
    """ Upload a file """
    data = await some_file.read()
    return (some_file.filename, some_file.content_type, data)


@test_router.post("/json_body")
def json_body(body: AModel):
    """ Try sending a JSON body """
    return


@test_router.post("/test_defaults")
def test_defaults(
    string_prop: str = Query(default="the default string"),
    datetime_prop: datetime = Query(default=datetime(1010, 10, 10)),
    date_prop: date = Query(default=date(1010, 10, 10)),
    float_prop: float = Query(default=3.14),
    int_prop: int = Query(default=7),
    boolean_prop: bool = Query(default=False),
    list_prop: List[AnEnum] = Query(default=[AnEnum.FIRST_VALUE, AnEnum.SECOND_VALUE]),
    union_prop: Union[float, str] = Query(default="not a float"),
    enum_prop: AnEnum = Query(default=AnEnum.FIRST_VALUE),
    dict_prop: Dict[str, str] = Body(default={"key": "val"}),
):
    return


app.include_router(test_router, prefix="/tests", tags=["tests"])


def generate_openapi_json():
    path = Path(__file__).parent / "openapi.json"
    path.write_text(json.dumps(app.openapi(), indent=4))


if __name__ == "__main__":
    generate_openapi_json()
