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
            "SELECT projects.id, projects.name as ProjectName, users.name, users.lastName, users.emailAddress, organizations.name as organizationName "
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
            "SELECT projects.id, projects.name as ProjectName, users.name, users.lastName, users.emailAddress, organizations.name as organizationName "
            "FROM projects join userRoleToProject join users join organizations join userRoleToOrganization on "
            "projects.id = userRoleToProject.projectId and "
            "users.id = userRoleToProject.userId and "
            "users.id = userRoleToOrganization.userId and "
            "userRoleToOrganization.organizationId = organizations.id"
            f" WHERE organizations.id = '{organizationId}'")

        result = await execute_query(query=query)
        return result

    @classmethod
    async def getAllProjectsUser(cls, userId: str):
        # users.name, users.lastName, users.emailAddress, organizations.name
        query = (
            "SELECT projects.id, projects.name as ProjectName, users.name, users.lastName, users.emailAddress, organizations.name as organizationName "
            "FROM projects join userRoleToProject join users join organizations join userRoleToOrganization on "
            "projects.id = userRoleToProject.projectId and "
            "users.id = userRoleToProject.userId and "
            "users.id = userRoleToOrganization.userId and "
            "userRoleToOrganization.organizationId = organizations.id"
            f" WHERE userRoleToProject.userId = '{userId}'")

        result = await execute_query(query=query)
        return result

    @classmethod
    async def getOrganizationIdUsingProjectId(cls, projectId):
        query = (
            "SELECT organizations.name , organizations.id "
            "FROM projects join userRoleToProject join users join organizations join userRoleToOrganization on "
            "projects.id = userRoleToProject.projectId and "
            "users.id = userRoleToProject.userId and "
            "users.id = userRoleToOrganization.userId and "
            "userRoleToOrganization.organizationId = organizations.id"
            f" WHERE projects.id = '{projectId}'")
        result = await execute_query(query=query)
        return result[0]["id"]

    @classmethod
    async def getUserRoleToProject(cls, userId, projectId):
        query = (
            "SELECT projectRoles.name "
            "FROM userRoleToProject inner join projectRoles on userRoleToProject.roleId = projectRoles.id "
            f" WHERE userRoleToProject.userId = '{userId}' and userRoleToProject.projectId = '{projectId}'")
        result = await execute_query(query=query)
        return result

    @classmethod
    async def isProjectIdValid(cls, projectId):
        query = f"SELECT id FROM projects WHERE id = '{projectId}'"
        result = await execute_query(query=query)
        if len(result) == 0:
            return False
        else:
            return True

    @classmethod
    async def doesUserHaveAccessToProject(cls, projectId, userId):
        query = (
            "SELECT * "
            "FROM userRoleToProject"
            f" WHERE userRoleToProject.userId = '{userId}' and userRoleToProject.projectId = '{projectId}'")
        result = await execute_query(query=query)
        if len(result) == 0:
            return False
        else:
            return True

    @classmethod
    async def getProjectInfo(cls, projectId):
        query = (
                "SELECT "
                "projects.name as projectsName, "
                "projects.id as id, "
                "users.name as usersName, "
                "users.lastName as usersLastName, "
                "users.emailAddress as usersEmailAddress, "
                "users.id as usersId, "
                "projectRoles.name as usersRole "
                "FROM "
                "projects inner join userRoleToProject on projects.id=userRoleToProject.projectId "
                "inner Join users on users.id=userRoleToProject.userId "
                "inner join projectRoles on projectRoles.id=userRoleToProject.roleId "
                f"WHERE projects.id = '{projectId}'")
        print(query)
        result = await execute_query(query=query)
        print(result)
        return result