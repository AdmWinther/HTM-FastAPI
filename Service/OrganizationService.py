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
        if "name" not in organizationInfo: raise ValueError("organizationInfo Dictionary must contain a name field")
        if "description" not in organizationInfo: organizationInfo["description"] = ""
        if("id" not in organizationInfo):
            id = str(uuid4())
        else:
            id = organizationInfo["id"]
        query = (f"INSERT INTO organizations (id, name, description)"
                 f" VALUES ('{id}', '{organizationInfo['name']}' ,'{organizationInfo['description']}')")
        try:
            operationSuccess = await insertIntoTable(query=query)
            if operationSuccess:
                organizationObject: Organization = Organization(
                    id,
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
        print(query)
        return execute_query(query=query)