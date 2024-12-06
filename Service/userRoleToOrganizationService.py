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
        query = [(f"INSERT INTO userRoleToOrganization (userId, organizationId, roleId)"
                 f" VALUES ('{userId}', '{organizationId}', '{roleId}')")]
        print("query is : " + query[0])
        return await Database.execute_transaction(queries=query)

    @classmethod
    def deleteAll(cls):
        query = "DELETE FROM userRoleToOrganization where 1=1"
        return Database.execute_query(query=query)

    @classmethod
    async def getOrganizationIdByUserId(cls, userId: str):
        query = f"SELECT organizationId FROM userRoleToOrganization WHERE userId = '{userId}'"
        organizationIdArray = await Database.execute_query(query=query)
        print(organizationIdArray)
        organizationId : str = organizationIdArray[0]["organizationId"]
        print(organizationId)
        return organizationId