from fastapi import APIRouter, Request
from sqlalchemy import false
from starlette.responses import JSONResponse

from Model.Entity.Project import Project
from Service.S03_ProjectService import ProjectService
from utility import JWTtoken
from uuid import uuid4
from Service.S01_UserService import UserService
from utility.GetUserMainRoleFromRequest import GetUserMainRoleFromRequest
from utility.GetUserIdFromRequest import GetUserIdFromRequest

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

@projectRouter.get("/all")
async def getAllProjects(request : Request):
    userMainRole = GetUserMainRoleFromRequest(request)
    if userMainRole == "SUPERUSER":
        #Superuser can only see the users of its own organization
        organizationId = await UserService.getUserOrganizationIdByUserId(GetUserIdFromRequest(request))
        return await ProjectService.getAllProjectsSuperUser(organizationId)
    if userMainRole == "ADMIN":
        return await ProjectService.getAllProjectsAdmin()
    if userMainRole == "USER":
        userId = GetUserIdFromRequest(request)
        return await ProjectService.getAllProjectsUser(userId)

    return {"error": "Unauthorized"}

@projectRouter.get("/projectInfo/id/{projectId}")
async def getProjectInfo(projectId : str, request: Request):
    if await isUserAllowedToSeeProjectInfo(projectId, request):
        return await ProjectService.getProjectInfo(projectId)
    else:
        return JSONResponse({"error": "Unauthorized"}, status_code=401)

@projectRouter.post("/projectName")
async def getProjectName(requestData: dict, request: Request):
    projectId = requestData["projectId"]
    if await isUserAllowedToSeeProjectInfo(projectId, request):
        return await ProjectService.getProjectName(projectId)
    else:
        return JSONResponse({"error": "Unauthorized"}, status_code=401)



async def isUserAllowedToSeeProjectInfo(projectId : str, request: Request):
    #is it a valid projectId?
    isAuthorized = False
    isItValidProjectId = await ProjectService.isProjectIdValid(projectId)
    if not isItValidProjectId:
        return JSONResponse({"error": "Invalid projectId"}, status_code=404)
    userId = GetUserIdFromRequest(request)
    userMainRole= GetUserMainRoleFromRequest(request)
    userOrganizationId = await UserService.getUserOrganizationIdByUserId(userId)
    projectOrganization = await ProjectService.getOrganizationIdUsingProjectId(projectId)

    #Control if user is authorized to see the project info
    #if user is ADMIN, he can see all the projects
    if userMainRole == "ADMIN":
        isAuthorized = True
    else:
        if userOrganizationId != projectOrganization:
            return JSONResponse({"error": "The project is not in the users organization."}, status_code=401)

        #If the user is SUPERUSER, then the user is authorized to see the project info
        if userMainRole == "SUPERUSER" or userMainRole == "ADMIN":
            isAuthorized = True

        #Does user have any role towards the project?
        doesUserHasAnyRoleTowardsProject: bool= await ProjectService.doesUserHaveAccessToProject(projectId, userId)
        if doesUserHasAnyRoleTowardsProject:
            isAuthorized = True

    if isAuthorized:
        #If user has any role towards the project, the user should be able to see the project info like the project name,
        #description, project manager, editor, reviewer, approved by, etc
        return True
    else:
        return False