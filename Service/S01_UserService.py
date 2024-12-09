from uuid import uuid4

from Model.Entity.User import User
from Service.S00_Database import execute_query, insertIntoTable, execute_transaction
import aiosqlite


class UserService:
    #:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # Get all users
    # Return a list of all users
    @classmethod
    async def getAllUsersAdmin(cls):
        #users.name, users.lastName, users.emailAddress, organizations.name
        query = ("SELECT users.name, users.lastName, users.emailAddress, organizationalRoles.name as Role, organizations.name as organizationName "
                 "FROM organizations join userRoleToOrganization join users join organizationalRoles on "
                 "organizations.id = userRoleToOrganization.organizationId and "
                 "userRoleToOrganization.userId = users.id and organizationalRoles.id = userRoleToOrganization.roleId")

        result = await execute_query(query=query)
        return result

    @classmethod
    async def getAllUsersSuperUser(cls, organizationId: str):
        # users.name, users.lastName, users.emailAddress, organizations.name
        query = (
            "SELECT users.name, users.lastName, users.emailAddress, organizationalRoles.name as Role, organizations.name as organizationName "
            "FROM organizations join userRoleToOrganization join users join organizationalRoles on "
            "organizations.id = userRoleToOrganization.organizationId and "
            "userRoleToOrganization.userId = users.id and organizationalRoles.id = userRoleToOrganization.roleId"
            f" WHERE organizations.id = '{organizationId}'")

        result = await execute_query(query=query)
        return result

    @classmethod
    async def getOrganizationUsers_OnlyIdAndNameAndLastName(cls, organizationId: str):
        # users.name, users.lastName, users.emailAddress, organizations.name
        query = (
            "SELECT users.id, users.name, users.lastName "
            "FROM organizations join userRoleToOrganization join users join organizationalRoles on "
            "organizations.id = userRoleToOrganization.organizationId and "
            "userRoleToOrganization.userId = users.id and organizationalRoles.id = userRoleToOrganization.roleId"
            f" WHERE organizations.id = '{organizationId}'")

        result = await execute_query(query=query)
        return result

    #:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # Reset the database
    # Delete all users and add a default user and an admin user
    # Return a list of all users after the reset
    @classmethod
    async def deleteAll(cls):
        print("deleting all users")
        try:
            query = ["DELETE FROM users where 0=0"]
            await execute_transaction(queries=query)
            return {"message": "Deleted all users successfully"}
        except Exception as e:
            print(f"userService-deleteAll: {e}")
            return {"error": str(e)}



    #:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # Get a user by id
    # Return the user with the given id
    @classmethod
    async def getUserById(cls, userId: str):
        query = f"SELECT * FROM users WHERE id ='{userId}'"
        return await execute_query(query=query)


    #:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # Get a user by email address
    # Return the user with the given email address
    @classmethod
    async def getUserByEmail(cls, emailAddress: str):
        emailAddress = emailAddress.lower()
        # print("getting user by email-haha-UserService")
        query = f"SELECT * FROM users WHERE emailAddress ='{emailAddress}'"
        return await execute_query(query=query)


    #:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # Add a user by dictionary WITHOUT validating the fields
    @classmethod
    async def addUserByDictNoValidation(cls, user: dict):
        query = [(f"INSERT INTO users (id, name, lastName, emailAddress, password)"
                 f" VALUES ('{user['id']}', '{user['name']}','{user['lastName']}', '{user['emailAddress']}', '{user['password']}')")]
        try:
            operationSuccess = await execute_transaction(queries=query)
            if operationSuccess:
                return user
            else:
                raise ValueError(f"Error. Operation failed_UserService: {operationSuccess}")
        except Exception as e:
            raise ValueError(e)

    @classmethod
    async def getUserOrganizationIdByUserId(cls, userId):
        databaseResult  = await execute_query(f"SELECT organizationId FROM userRoleToOrganization WHERE userId = '{userId}'")
        return databaseResult[0]["organizationId"]

    @classmethod
    async def getUserRoleByUserId(cls, id):
        # Control if the user is a super user
        query = f"SELECT name FROM userRoleToOrganization inner join organizationalRoles on userRoleToOrganization.roleId = organizationalRoles.id where userId = '{id}'"
        try:
            userRoles = await execute_query(query=query)
            userRolesArray = []
            for role in userRoles:
                userRolesArray.append(role["name"])
            return userRolesArray
        except Exception as e:
            return {"error": str(e)}

    @classmethod
    async def IsThisEmailAddressAlreadyRegistered(cls, emailAddress: str):
        try:
            result  = await cls.getUserByEmail(emailAddress)
            if len(result) > 0:
                raise ValueError("Email is already registered.")
            else:
                return False
        except Exception as e:
            raise ValueError(e)