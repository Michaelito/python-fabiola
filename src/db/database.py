import os
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine

engine = None
engine_repl = None
firstTimeDb = True
last = 1


def db_url():
    return "postgresql+psycopg2://{}:{}@{}:{}/{}?sslmode=disable".format(
        os.getenv("DB_USER"),
        os.getenv("DB_PASSWORD"),
        os.getenv("DB_HOST"),
        os.getenv("DB_PORT"),
        os.getenv("DB_NAME"),
    )


def db_url_repl():
    return "postgresql+psycopg2://{}:{}@{}:{}/{}?sslmode=disable".format(
        os.getenv("DB_USER"),
        os.getenv("DB_PASSWORD"),
        os.getenv("DB_HOST_RPL"),
        os.getenv("DB_PORT_RPL"),
        os.getenv("DB_NAME"),
    )


def database_session(write=False):
    global firstTimeDb, engine, engine_repl, last
    if firstTimeDb is True:
        engine = create_engine(
            db_url(),
            pool_size=250,
            max_overflow=50,
            pool_use_lifo=True,
            pool_pre_ping=True,
            pool_recycle=300,
        )

        engine_repl = create_engine(
            db_url_repl(),
            pool_size=250,
            max_overflow=50,
            pool_use_lifo=True,
            pool_pre_ping=True,
            pool_recycle=300,
        )
        firstTimeDb = False

    if write is False:
        if last == 1:
            last = 2
            return scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
        else:
            last = 1
            return scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine_repl))

    return scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
