from fastapi import APIRouter, Request
from starlette.responses import JSONResponse

from Model.Entity.Project import Project
from Service.S03_ProjectService import ProjectService
from utility import JWTtoken
from uuid import uuid4

projectRouter = APIRouter()

@projectRouter.post("/new")
async def newProject(projectInfo : dict,request: Request):
    JwtToken = JWTtoken.getJwtTokenFromRequest(request)
    userRoles = JWTtoken.getUserRoleFromJwtTokenPayload(JwtToken)
    if "SUPERUSER" in userRoles:
        try:
            Project.isProjectNameValid(projectInfo["projectName"])
        except ValueError as e:
            return JSONResponse({"error": str(e)})
        projectInfoWithId = projectInfo
        projectInfoWithId["id"] = uuid4()
        try:
            await ProjectService.addProject(projectInfoWithId)
            return {"message": "Project is added."}
        except ValueError as e:
            raise ValueError(e)