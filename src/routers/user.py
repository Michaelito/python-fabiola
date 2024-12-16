import logging

from fastapi import APIRouter, Request
from fastapi.security import HTTPBearer

from exception.global_exception import GlobalException
from enums.exception_error_enum import ExceptionErrorEnum
from schemas.request.natural_person import RequestNaturalPerson
from schemas.response.natural_person import ResponseBase
from service.natural_person import NaturalPersonService


auth_scheme = HTTPBearer()

router = APIRouter(prefix="/user", tags=["User"])

logger = logging.getLogger(__name__)


@router.get("/", summary="user")
async def user(
    request: Request, data: RequestNaturalPerson
) -> ResponseBase:

    try:
        service = NaturalPersonService()
        service.register(data)

        return ResponseBase(rc=ExceptionErrorEnum.OK.value)

    except Exception as e:
        if isinstance(e, GlobalException):
            return ResponseBase(rc=e.code)
        else:
            return ResponseBase(rc=ExceptionErrorEnum.UNKNOWN_ERROR.value)
