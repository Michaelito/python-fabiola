import logging
import os

from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from exception.global_exception import GlobalException
from enums.exception_error_enum import ExceptionErrorEnum
from schemas.request.natural_person import RequestLogin, RequestNaturalPerson
from schemas.response.natural_person import ResponseBase
from service.natural_person import NaturalPersonService
from util.security.security import verify_token
# from util.security.security import verify_token


auth_scheme = HTTPBearer()

router = APIRouter(prefix="/natural_person", tags=["Natural Person"])

_logger = logging.getLogger(__name__)


@router.post("/", tags=["Natural Person"], summary="Natural Person Register")
async def register(data: RequestNaturalPerson, token: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> ResponseBase:

    cd_auth = verify_token(token.credentials, os.getenv(
        "JWT_SECRET_KEY"), os.getenv("JWT_ALGORITHMS"))

    _logger.debug(f"---------------------: {cd_auth}")

    try:
        service = NaturalPersonService()

        service.register(data=data)

        return ResponseBase(rc=ExceptionErrorEnum.OK.value)

    except Exception as e:
        if isinstance(e, GlobalException):
            return ResponseBase(rc=e.code)
        else:
            return ResponseBase(rc=ExceptionErrorEnum.UNKNOWN_ERROR.value)


@router.post("/token", tags=["Natural Person"], summary="Login")
async def token(
    request: Request, data: RequestLogin
) -> ResponseBase:

    try:
        service = NaturalPersonService()
        response = service.token(data)

        return ResponseBase(rc=ExceptionErrorEnum.OK.value, data=response)

    except Exception as e:
        if isinstance(e, GlobalException):
            return ResponseBase(rc=e.code)
        else:
            return ResponseBase(rc=ExceptionErrorEnum.UNKNOWN_ERROR.value)
