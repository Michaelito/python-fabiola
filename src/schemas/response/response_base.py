from pydantic import BaseModel


class ResponseBase(BaseModel):
    rc: int
    data: dict | None = None
