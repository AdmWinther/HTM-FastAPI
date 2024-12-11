from starlette.responses import JSONResponse

from Service.S00_Database import execute_query, insertIntoTable, execute_transaction
from Service.S04_ProjectRoleService import ProjectRoleService

class ProjectService:
    @classmethod
    async def addProject(cls, projectInfo):

        query = [(f"INSERT INTO projects (id, name, description) values ('{projectInfo["id"]}', '{projectInfo["projectName"]}','{projectInfo["description"]}')")]
        projectManagerRoleIdDatabaseResult = await ProjectRoleService.getTheRoleID("PROJECT_MANAGER")
        projectManagerRoleId =  projectManagerRoleIdDatabaseResult["id"]
        query.append(f"INSERT INTO userRoleToProject (userId, projectId, roleId) VALUES ('{projectInfo["projectManager"]}', '{projectInfo["id"]}', '{projectManagerRoleId}')")
        try:
            operationSuccess = await execute_transaction(queries=query)
            if operationSuccess:
                return JSONResponse("Project is added.")
            else:
                return {"error": "Adding the new project failed"}
        except ValueError as e:
            return ValueError(e)
        
    @classmethod
    async def getAllProjectsAdmin(cls):
        # users.name, users.lastName, users.emailAddress, organizations.name
        query = (
            "SELECT projects.name as ProjectName, users.name, users.lastName, users.emailAddress, organizations.name as organizationName "
            "FROM projects join userRoleToProject join users join organizations join userRoleToOrganization on "
            "projects.id = userRoleToProject.projectId and "
            "users.id = userRoleToProject.userId and "
            "users.id = userRoleToOrganization.userId and "
            "userRoleToOrganization.organizationId = organizations.id")

        result = await execute_query(query=query)
        return result

    @classmethod
    async def getAllProjectsSuperUser(cls, organizationId: str):
        # users.name, users.lastName, users.emailAddress, organizations.name
        query = (
            "SELECT projects.name as ProjectName, users.name, users.lastName, users.emailAddress, organizations.name as organizationName "
            "FROM projects join userRoleToProject join users join organizations join userRoleToOrganization on "
            "projects.id = userRoleToProject.projectId and "
            "users.id = userRoleToProject.userId and "
            "users.id = userRoleToOrganization.userId and "
            "userRoleToOrganization.organizationId = organizations.id"
            f" WHERE organizations.id = '{organizationId}'")

        result = await execute_query(query=query)
        return result