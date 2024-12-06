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


@UserRouter.get("/all")
async def getAllUsers(request : Request):
    token: str = getJwtTokenFromRequestHeader(request)
    tokenPayload = JWTtoken.getTokenPayload(token)
    userRoles  = tokenPayload["role"]
    userMainRole = userRoles[0]
    if userMainRole == "SUPERUSER":
        #Superuser can only see the users of its own organization
        organizationId = await UserService.getUserOrganizationIdByUserId(tokenPayload["id"])
        return await UserService.getAllUsersSuperUser(organizationId)

    if userMainRole == "ADMIN":
        return await UserService.getAllUsersAdmin()

    return {"error": "Unauthorized"}

@UserRouter.post("")
async def postUser(userInfo : dict, request: Request):
    try:
        #First we need to validate the userInfo fields
        newUser: dict = {
            "id": str(uuid4()),
            "name": userInfo["name"],
            "lastName": userInfo["lastName"],
            "emailAddress": userInfo["emailAddress"].lower(),
            "password": User.get_password_hash(userInfo["password"])
        }
        User.validateNewUserInfo(newUser["name"], newUser["lastName"], newUser["emailAddress"])

        #control if the email is already registered for another user
        await UserService.IsThisEmailAddressAlreadyRegistered(newUser["emailAddress"])

        #now the new user data is validated and we are sure that the user email is not registered before
        #Next step is to control if the request is coming from a superuser
        JwtToken : str = getJwtTokenFromRequestHeader(request)
        tokenPayload = JWTtoken.getTokenPayload(JwtToken)
        userRoles  = tokenPayload["role"]
        if "SUPERUSER" not in userRoles:
            print(f"User roles: {userRoles}. As you can see Superuser is not in the roles.")
            # Only Superuser is allowed to add users to its own organizations
            return JSONResponse({"error": "Unauthorized"}, status = 401)

        superUserOrganizationId : str = await userRoleToOrganizationService.getOrganizationIdByUserId(tokenPayload["id"])
        try:
            newUserRegister = await UserService.addUserByDictNoValidation(newUser)
        except ValueError as e:
            raise ValueError(f"Could not register superuser.{e}")

        try:
            UserRoleId = await OrganizationalRolesService.getRoleId("USER")
            await userRoleToOrganizationService.setUserOrganization(newUser["id"],
                                                                    superUserOrganizationId,
                                                                    UserRoleId)
        except ValueError as e:
            raise ValueError(f"User is registered but could not add the userToOrganization. {e}")

        return {"message": "New user is registered successfully."}
    except ValueError as e:
        return {"error": str(e)}


@UserRouter.get("/reset")
async def resetUserTable():
    user: dict = {"id":f"{uuid4()}", "name": "user", "lastName": "user", "emailAddress": "user@user.com", "password": f"{User.get_password_hash("user")}"}
    admin: dict = {"id":f"{uuid4()}", "name": "admin", "lastName": "admin", "emailAddress": "admin@admin.com", "password": f"{User.get_password_hash("user")}"}
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
    userRolesArray = await UserService.getUserRoleByUserId(tokenPayload['id'])
    return {"roles": userRolesArray}