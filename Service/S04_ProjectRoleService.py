import os
from .S00_Database import execute_query


class ProjectRoleService:
    @classmethod
    async def getTheRoleID(cls, roleName):
        availableProjectRoles = os.getenv("PROJECT_ROLES").split(",")
        if roleName in availableProjectRoles:
            query = f"SELECT id FROM projectRoles Where name = '{roleName}'"
            try:
                queryResult = await execute_query(query= query)
                return queryResult[0]
            except ValueError as e:
                raise ValueError(e)
        else:
            ValueError("The role is not a valid value in Project Roles list.")