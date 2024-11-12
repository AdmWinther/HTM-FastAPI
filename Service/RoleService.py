import os
from uuid import uuid4
from Service import Database

class RoleService:
    @classmethod
    async def reset(cls):
        allRoles = os.getenv("ROLES").split(",")
        print("allRoles")
        print(allRoles)

        print("resetting database-Roles")
        queries = ["DELETE FROM roles where 1=1"]

        for role in allRoles:
            queries.append(f"INSERT INTO roles (id, name, description) VALUES ('{uuid4()}', '{role}', 'no description is available.')")

        await Database.execute_transaction(queries)

        return await cls.getAllRoles()

    @classmethod
    async def getAllRoles(cls):
        print("getting all roles")
        query = "SELECT * FROM roles"
        return await Database.execute_query(query=query)
