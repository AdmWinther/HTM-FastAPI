from uuid import uuid4

from Model.Entity.User import User
from Service import Database
import aiosqlite


class UserService:
    #:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # Get all users
    # Return a list of all users
    @classmethod
    async def getAllUsers(cls):
        query = "SELECT * FROM users"
        return await Database.execute_query(query=query)

    #:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # Reset the database
    # Delete all users and add a default user and an admin user
    # Return a list of all users after the reset
    @classmethod
    async def deleteAll(cls):
        print("resetting database-UserService")
        try:
            queries = ["DELETE FROM users"]
            await Database.execute_transaction(queries=queries)
            return {"message": "Database reset"}
        except Exception as e:
            return {"error": str(e)}



    #:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # Get a user by id
    # Return the user with the given id
    @classmethod
    async def getUserById(cls, userId: str):
        query = f"SELECT * FROM users WHERE id ='{userId}'"
        return await Database.execute_query(query=query)


    #:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # Get a user by email address
    # Return the user with the given email address
    @classmethod
    async def getUserByEmail(cls, emailAddress: str):
        emailAddress = emailAddress.lower()
        # print("getting user by email-haha-UserService")
        query = f"SELECT * FROM users WHERE emailAddress ='{emailAddress}'"
        return await Database.execute_query(query=query)


    #:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # Add a user by dictionary and validate the dictionary before adding the user
    @classmethod
    async def addUserByDictWithValidation(cls, userInfo: dict):
        #control if the dictionary has the required fields and the format is correct
        try:
            User.validateNewUserInfo(userInfo["name"], userInfo["lastName"], userInfo["emailAddress"])
        except ValueError as e:
            raise ValueError(e)

        userInfo["emailAddress"] = userInfo["emailAddress"].lower()
        userInfo["password"] = User.get_password_hash(userInfo["password"])

        #control if the email address is already registered
        exising = await cls.getUserByEmail(userInfo["emailAddress"])
        print("existing - UserServices")
        print(exising)
        if len(exising) != 0:
            e ="Error. The email address is already registered."
            raise ValueError(e)

        user: User = User(**userInfo)

        query = (f"INSERT INTO users (id, name, lastName, emailAddress, password)"
                 f" VALUES ('{user.id}', '{user.name}' ,'{user.lastName}', '{user.emailAddress}', '{user.password}')")
        try:
            operationSuccess = await Database.insertIntoTable(query=query)
            if operationSuccess:
                return dict(user)
            else:
                raise ValueError("Error. Operation failed_UserService")
        except Exception as e:
            raise ValueError(e)

    @classmethod
    def addSuperUser(cls, userId, organizationId):
        query = (f"INSERT INTO superUser (userId, organizationId)"
                 f" VALUES ('{userId}', '{organizationId}')")
        return Database.insertIntoTable(query=query)