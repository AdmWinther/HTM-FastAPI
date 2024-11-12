from uuid import uuid4

from Service.Database import execute_query, insertIntoTable, execute_transaction

class OrganizationService:
    @classmethod
    async def getAllOrganizations(cls):
        query = "SELECT * FROM organizations"
        return await execute_query(query=query)

    @classmethod
    async def addOrganization(cls, organizationInfo):
        if "organization_name" not in organizationInfo: raise ValueError("Dictionary must contain a name field")
        if "description" not in organizationInfo: organizationInfo["description"] = ""
        id = str(uuid4())
        query = (f"INSERT INTO organizations (id, name, description)"
                 f" VALUES ('{id}', '{organizationInfo['organization_name']}' ,'{organizationInfo['description']}')")
        try:
            operationSuccess = await insertIntoTable(query=query)
            if operationSuccess:
                return {"id": id, "name": organizationInfo["organization_name"], "description": organizationInfo["description"]}
            else:
                return {"error": "Operation failed"}
        except Exception as e:
            return {"error": str(e)}