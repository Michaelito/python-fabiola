from datetime import datetime
import logging
from argon2 import PasswordHasher


from db.model.natural_person import NaturalPersonModel
from enums.exception_error_enum import ExceptionErrorEnum
from exception.global_exception import GlobalException
from schemas.request.natural_person import RequestLogin, RequestNaturalPerson

ph = PasswordHasher()


class NauralPersonRepository():

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self.ph = PasswordHasher()

    def register(self, db_session, data: RequestNaturalPerson):
        self._logger.debug("starting repository register")

        hashed_password = ph.hash(data.password)

        dt_created = datetime.utcnow()

        obj = NaturalPersonModel(
            e_mail=data.e_mail,
            name=data.name,
            surname=data.surname,
            password=hashed_password,
            document=data.document,
            role=data.role,
            dt_created=dt_created,
            dt_updated=dt_created,
        )

        db_session.add(obj)
        db_session.commit()
        db_session.refresh(obj)

        return obj

    def auth_natural_person(self, db_session, data: RequestLogin) -> NaturalPersonModel:
        self._logger.debug("starting repository auth_natural_person")

        # Buscar a pessoa natural pelo email
        natural_person = db_session.query(NaturalPersonModel).filter(
            NaturalPersonModel.e_mail == data.login
        ).first()

        if natural_person is None:
            raise GlobalException(ExceptionErrorEnum.DATA_NOT_FOUND.value)

        # Verificar a senha fornecida contra a senha hash armazenada
        try:
            self.ph.verify(natural_person.password, data.password)
        except Exception as e:
            self._logger.debug(f"error: {e}")
            raise GlobalException(ExceptionErrorEnum.INVALID_PASSWORD.value)

        return natural_person
