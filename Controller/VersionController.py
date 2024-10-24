import os

from fastapi import APIRouter


VersionRouter = APIRouter()

@VersionRouter.get("")
async def getAllUsers():
    return os.getenv("VERSION")