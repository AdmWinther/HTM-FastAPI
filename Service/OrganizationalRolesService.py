import os
from uuid import uuid4
from Service import Database

class OrganizationalRolesService:
    @classmethod
    async def reset(cls):
        allOrganizationalRoles = os.getenv("ORGANIZATIONAL_ROLES").split(",")
        print("all organizationalRoles from env")
        print(allOrganizationalRoles)

        print("resetting database-organizationalRoles")
        queries = ["DELETE FROM organizationalRoles where 1=1"]

        for role in allOrganizationalRoles:
            queries.append(f"INSERT INTO organizationalRoles (id, name, description)"
                           f" VALUES ('{uuid4()}', '{role}', 'no description is available.')")

        await Database.execute_transaction(queries)

        return await cls.getAllRoles()

    @classmethod
    async def getAllRoles(cls):
        print("getting all organizationalRoles")
        query = "SELECT * FROM organizationalRoles"
        return await Database.execute_query(query=query)

    @classmethod
    async def getRoleId(cls, roleName: str):
        query = f"SELECT id FROM organizationalRoles WHERE name = '{roleName}'"
        queryResult = await Database.execute_query(query=query)
        return queryResult[0]["id"]

    @classmethod
    async def getRoleName(cls, roleId: str):
        query = f"SELECT name FROM organizationalRoles WHERE id = '{roleId}'"
        queryResult = await Database.execute_query(query=query)
        return queryResult[0]["name"]