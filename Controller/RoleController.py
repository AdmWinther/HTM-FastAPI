from fastapi import APIRouter, Response

from Service.RoleService import RoleService


roleRouter = APIRouter()


@roleRouter.get("/getAll")
async def getAllRoles():
    return await RoleService.getAllRoles()

@roleRouter.get("/reset")
async def resetRoles():
    print("initializing roles")
    return await RoleService.reset()