import os
from uuid import uuid4

from Model.Entity.Organization import Organization
from Service.Database import execute_query, insertIntoTable, execute_transaction

class OrganizationService:
    @classmethod
    async def getAllOrganizations(cls):
        query = "SELECT * FROM organizations"
        return await execute_query(query=query)

    @classmethod
    async def addOrganization(cls, organizationInfo):
        query = [(f"INSERT INTO organizations (id, name, description)"
                 f" VALUES ('{organizationInfo['id']}', '{organizationInfo['name']}' ,'{organizationInfo['description']}')")]
        try:
            operationSuccess = await execute_transaction(queries=query)
            if operationSuccess:
                organizationObject: Organization = Organization(
                    organizationInfo["id"],
                    organizationInfo["name"],
                    organizationInfo["description"]
                )
                # return {"id": id, "name": organizationInfo["organization_name"], "description": organizationInfo["description"]}
                return organizationObject
            else:
                return {"error": "Operation failed"}
        except Exception as e:
            return {"error": str(e)}

    @classmethod
    def deleteAll(cls):
        query = "DELETE FROM organizations where 7=7"
        if os.getenv("VERBOSE"): print(query)
        return execute_query(query=query)