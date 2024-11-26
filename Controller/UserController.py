import os
from typing import List
from uuid import uuid4

from Service.Database import execute_transaction
from fastapi import APIRouter, Request
from starlette.responses import JSONResponse
from urllib3 import request

from Controller import JWTtoken
from Controller.JWTtoken import getJwtTokenFromRequestHeader
from Model.Entity.Organization import Organization
from Service.OrganizationService import OrganizationService
from Service.OrganizationalRolesService import OrganizationalRolesService
from Service.UserService import UserService
from Service.userRoleToOrganizationService import userRoleToOrganizationService
from Model.Entity.User import User

UserRouter = APIRouter()


@UserRouter.get("")
async def getAllUsers():
    return await UserService.getAllUsers()

@UserRouter.post("")
async def postUser(userInfo : dict):
    try:
        return await UserService.addUserByDictWithValidation(userInfo)
        # return db
    except ValueError as e:
        return {"error": str(e)}

@UserRouter.get("/reset")
async def resetUserTable():
    user: dict = {"id":f"{uuid4()}", "name": "user", "lastName": "user", "emailAddress": "user@user.com", "password": "user"}
    admin: dict = {"id":f"{uuid4()}", "name": "admin", "lastName": "admin", "emailAddress": "admin@admin.com", "password": "user"}
    htmDict: dict = {"name": "HTM", "description": "HTM organization"}
    HtmOrganization: dict = {"id":"0","name": "HTM", "description": "HTM organization"}
    print("resetting database")

    try:
        #Delete all  users
        queries = ["DELETE FROM users where 0=0"]

        # Delete all organizational roles and add the default ones from the environment variable
        allOrganizationalRoles = os.getenv("ORGANIZATIONAL_ROLES").split(",")
        queries.append("DELETE FROM organizationalRoles where 1=1")
        for role in allOrganizationalRoles:
            queries.append(f"INSERT INTO organizationalRoles (id, name, description)"
                           f" VALUES ('{uuid4()}', '{role}', 'no description is available.')")

        #Delete all project related roles and add the default ones from the environment variable
        allProjectRoles = os.getenv("PROJECT_ROLES").split(",")
        queries.append("DELETE FROM projectRoles where 1=1")
        for projectRole in allProjectRoles:
            queries.append(f"INSERT INTO projectRoles (id, name, description)"
                           f" VALUES ('{uuid4()}', '{projectRole}', 'no description is available.')")

        # Delete all organizations
        queries.append("DELETE FROM organizations where 7=7")

        # Delete all user roles related to organizations
        queries.append("DELETE FROM userRoleToOrganization where 1=1")

        # Add the default user "USER" to the user table
        queries.append(f"INSERT INTO users (id, name, lastName, emailAddress, password)"
                       f" VALUES ('{user['id']}', '{user['name']}', '{user['lastName']}'"
                       f", '{user['emailAddress']}', '{user['password']}')")

        # Add the default user "ADMIN" to the user table
        queries.append(f"INSERT INTO users (id, name, lastName, emailAddress, password)"
                       f" VALUES ('{admin['id']}', '{admin['name']}', '{admin['lastName']}'"
                       f", '{admin['emailAddress']}', '{admin['password']}')")

        # Add the default organization "HTM" to the organizations table
        queries.append(f"INSERT INTO organizations (id, name, description)"
                       f" VALUES ('{HtmOrganization['id']}', '{HtmOrganization['name']}' ,'{HtmOrganization['description']}')")

        await execute_transaction(queries)
        # Get the role ids for the default roles ADMIN and USER
        adminRoleId = await OrganizationalRolesService.getRoleId("ADMIN")
        userRoleId = await OrganizationalRolesService.getRoleId("USER")

        # Add the
        queries = [f"insert into userRoleToOrganization (userId, organizationId, roleId) values ('{user['id']}', '0', '{userRoleId}')"]
        # await userRoleToOrganizationService.setUserOrganization(admin["id"], "0", adminRoleId[0]["id"])
        queries.append(f"insert into userRoleToOrganization (userId, organizationId, roleId) values ('{admin['id']}', '0', '{adminRoleId}')")
        await execute_transaction(queries)
        return {"message": "Database reset"}
    except ValueError as e:
        return {"error": str(e)}

@UserRouter.get("/id/{userId}")
async def getUserById(userId: str):
    print(f"userid in controller: {userId}")
    return await UserService.getUserById(userId)


@UserRouter.get("/email/{emailAddress}")
async def getUserByEmail(emailAddress: str):
    return await UserService.getUserByEmail(emailAddress)

@UserRouter.get("/userRole")
async def getUserRoleEndpoint(request: Request):
    token: str = getJwtTokenFromRequestHeader(request)
    tokenPayload = JWTtoken.getTokenPayload(token)
    print(f"FETCH usrRoles for {tokenPayload['sub']}")
    return await getUserRoleByUserName(tokenPayload['sub'])


async def getUserRoleByUserName(username: str):
    # print("UserType-get in controller")
    data: dict = {"roles": ["ADMIN"]}
    # response = await call_next(request)
    # response.set_body(data)
    return UserService.getUserRoleByUserName(username)

def addSuperUser(userId, organizationId):
    return (userId, organizationId)