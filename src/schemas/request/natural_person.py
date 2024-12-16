import re
from pydantic import BaseModel, Field, field_validator


class RequestNaturalPerson(BaseModel):

    e_mail: str = Field(...)
    name: str = Field(..., min_length=3)
    surname: str = Field(...)
    password: str = Field(...)
    document: str = Field(..., min_length=11, max_length=11)
    role: str = Field(...)

    @field_validator("document", mode="before")
    def validate_ddi(cls, value):
        return re.sub(r"\D", "", value)


class RequestLogin(BaseModel):

    login: str = Field(...)
    password: str = Field(...)
