from datetime import datetime, timedelta
import logging
import os

import jwt


from db.database import database_session
from db.repository.natural_person import NauralPersonRepository
from enums.exception_error_enum import ExceptionErrorEnum
from exception.global_exception import GlobalException
from schemas.request.natural_person import RequestLogin, RequestNaturalPerson
from schemas.response.response_base import ResponseBase


class NaturalPersonService:

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._natural_person_repository = NauralPersonRepository()

    def register(self, data: RequestNaturalPerson) -> ResponseBase:
        self._logger.debug("starting repository register")

        try:
            # session db
            db_session = database_session(write=False)

            # validate
            self._natural_person_repository.register(
                db_session=db_session, data=data)

            return ResponseBase(rc=ExceptionErrorEnum.OK.value)

        except Exception as e:
            if not isinstance(e, GlobalException):
                self._logger.error("{}".format(e))

            raise e
        finally:
            try:
                db_session.close()
            except:
                pass

    def create_jwt_token(self, paylod: dict) -> str:
        expire = datetime.utcnow() + timedelta(minutes=int(os.getenv("JWT_EXPIRED", 30)))
        paylod.update({"exp": expire})
        encoded_jwt = jwt.encode(paylod, os.getenv(
            "JWT_SECRET_KEY", "mysecretkey"), algorithm=os.getenv("JWT_ALGORITHM", "HS256"))
        return encoded_jwt

    def token(self, data: RequestLogin) -> ResponseBase:
        self._logger.debug("starting service token")

        try:
            # session db
            db_session = database_session(write=False)

            # validate
            natural_person = self._natural_person_repository.auth_natural_person(
                db_session=db_session, data=data)

            response = {
                "name": natural_person.name,
                "surname": natural_person.surname,
                "document": natural_person.document,
                "login": natural_person.e_mail,
                "role": natural_person.role
            }

            # Create JWT token
            token = self.create_jwt_token(response)
            response["token"] = token

            return response

        except Exception as e:
            if not isinstance(e, GlobalException):
                self._logger.error("{}".format(e))

            raise e
        finally:
            try:
                db_session.close()
            except:
                pass
