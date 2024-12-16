"""Classe com a definicao do modelo de dados"""

from datetime import datetime
from sqlalchemy import TIMESTAMP, Column, Integer, String, Text
from db.model.base import DeclarativeBase


class NaturalPersonModel(DeclarativeBase):
    """Classe com a definicao do modelo de dados"""

    __tablename__ = "tb_natural_person"
    __table_args__ = {"schema": "user"}

    id_natural_person = Column(Integer, primary_key=True)
    name = Column(String(64), default=None)
    surname = Column(String(128), default=None)
    e_mail = Column(String(200), default=None)
    document = Column(String(11), default=None)
    password = Column(String(250), default=None)
    token = Column(Text)
    role = Column(Integer)
    dt_created = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    dt_updated = Column(TIMESTAMP, default=datetime.utcnow,
                        onupdate=datetime.utcnow, nullable=False)

    # pylint: disable=E1103
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
