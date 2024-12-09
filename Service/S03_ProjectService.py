from starlette.responses import JSONResponse

from Service.S00_Database import execute_query, insertIntoTable, execute_transaction
from Service.S04_ProjectRoleService import ProjectRoleService

class ProjectService:
    @classmethod
    async def addProject(cls, projectInfo):

        query = [(f"INSERT INTO projects (id, name, description) values ('{projectInfo["id"]}', '{projectInfo["projectName"]}','{projectInfo["description"]}')")]
        projectManagerRoleId = await ProjectRoleService.getTheRoleID("PROJECT_MANAGER")
        query.append(f"INSERT INTO userRoleToProject (userId, projectId, roleId) VALUES ('{projectInfo["projectManager"]}', '{projectInfo["id"]}', '{projectManagerRoleId}')")
        try:
            operationSuccess = await execute_transaction(queries=query)
            if operationSuccess:
                return JSONResponse("Project is added.")
            else:
                return {"error": "Adding the new project failed"}
        except Exception as e:
            return {"error": str(e)}
        
    @classmethod
    async def getAllProjects(cls):
        query = "SELECT * FROM projects"
        return await execute_query(query=query)