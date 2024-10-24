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
    # Add a user
    # Add a user to the database
    # Return the user that was added
    @classmethod
    async def addUser(cls, user: User):
        user.emailAddress = user.emailAddress.lower()
        exising = await cls.getUserByEmail(user.emailAddress)
        print("existing - UserServices")
        print(exising)
        if(len(exising) != 0): return {"error": "The email address is already registered."}
        query = (f"INSERT INTO users (id, name, lastName, emailAddress, password)"
                 f" VALUES ('{user.id}', '{user.name}' ,'{user.lastName}', '{user.emailAddress}', '{user.password}')")
        try:
            operationSuccess = await Database.insertIntoTable(query=query)
            if(operationSuccess):
                return user
            else:
                return {"error": "Operation failed_UserService"}
        except Exception as e:
            return {"error_UserService": str(e)}



    #:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # Reset the database
    # Delete all users and add a default user and an admin user
    # Return a list of all users after the reset
    @classmethod
    async def resetDatabase(cls):
        print("resetting database-UserService-haha")
        queries = ["DELETE FROM users"]

        userId = str(uuid4())
        queries.append(f"INSERT INTO users (id, name, lastName, emailAddress, password) VALUES ('{userId}', 'user', 'user', 'user@user.com' , '{User.get_password_hash("user")}')")

        adminId = str(uuid4())
        queries.append(f"INSERT INTO users (id, name, lastName, emailAddress, password) VALUES ('{adminId}', 'admin', 'admin', 'admin@admin.com' , '{User.get_password_hash("user")}')")

        await Database.execute_transaction(queries)

        return await cls.getAllUsers()



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
