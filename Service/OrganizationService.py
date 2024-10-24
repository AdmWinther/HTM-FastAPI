from Service.Database import execute_query, insertIntoTable, execute_transaction

class OrganizationService:
    @classmethod
    async def getAllOrganizations(cls):
        query = "SELECT * FROM organizations"
        return await execute_query(query=query)

    @classmethod
    async def addOrganization(cls, organizationInfo):
        if "name" not in userInfo: raise ValueError("Dictionary must contain a name field")
        #     if "lastName" not in userInfo:raise ValueError("Dictionary must contain a lastName field")
        #     if "emailAddress" not in userInfo:raise ValueError("Dictionary must contain an emailAddress field")
        #     if "password" not in userInfo:raise ValueError("Dictionary must contain a password field")
        #     if "id" in userInfo: raise ValueError("Dictionary must not contain an id field")
