from pydantic import BaseModel


class VersionModel(BaseModel):
    major: int
    minor: int
    build: int


class ResponseVersion(BaseModel):
    version: VersionModel
