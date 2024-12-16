import logging
import sys


from fastapi import FastAPI

from fastapi.responses import PlainTextResponse

from routers import admin, natural_person, user
from schemas.response.response_version_schema import ResponseVersion, VersionModel
from dotenv import load_dotenv


load_dotenv()


app = FastAPI(title='MICHAEL API')

logging.basicConfig(
    stream=sys.stdout,
    encoding="utf-8",
    format="%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] %(name)s: %(message)s",
    level=logging.DEBUG,
)


@app.get("/health", response_class=PlainTextResponse, tags=["Header"], summary="Get Health")
async def get_health():
    return "OK"


@app.get("/version", tags=["Header"], summary="Get Version")
async def get_version() -> ResponseVersion:

    return ResponseVersion(version=VersionModel(major=1, minor=0, build=0))


app.include_router(natural_person.router)
app.include_router(admin.router)
app.include_router(user.router)
