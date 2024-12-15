import os
from uuid import uuid4

from Model.Entity.Organization import Organization
from Service.S00_Database import execute_query, insertIntoTable, execute_transaction

class OrganizationService:
    @classmethod
    async def getAllOrganizations(cls):
        query = (f"SELECT organizations.id, organizations.name as OrganizationName, users.name as superUserName, "
                 "users.lastName as superUserLastName, users.emailAddress as superUserEmailAddress "
                 "FROM organizations inner join userRoleToOrganization on "
                 "organizations.id = userRoleToOrganization.organizationId inner join users on "
                 "userRoleToOrganization.userId = users.id inner join organizationalRoles on "
                 "userRoleToOrganization.roleId = organizationalRoles.id WHERE organizationalRoles.name = 'SUPERUSER'")
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