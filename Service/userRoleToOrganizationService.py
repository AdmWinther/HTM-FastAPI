import os
from uuid import uuid4
from Service import Database

class userRoleToOrganizationService:
    @classmethod
    async def getUserRolesAndOrganizationId(cls, userId:str):
        print("getting user organization")
        query = "SELECT * FROM userRoleToOrganization WHERE userId = " + userId
        return await Database.execute_query(query=query)

    @classmethod
    async def setUserOrganization(cls, userId:str, organizationId:str, roleId:str = "1"):
        print("setting user organization")
        query = (f"INSERT INTO userRoleToOrganization (userId, organizationId, roleId)"
                 f" VALUES ('{userId}', '{organizationId}', '{roleId}')")
        return await Database.execute_query(query=query)

    @classmethod
    def deleteAll(cls):
        query = "DELETE FROM userRoleToOrganization where 1=1"
        return Database.execute_query(query=query)