from pydantic import BaseModel

from schemas.response.response_base import ResponseBase


class ResponseNaturalPerson(BaseModel):
    name: str
    token: str


class ResponseNaturalPersonDict(ResponseBase):
    data: ResponseNaturalPerson | None = None
