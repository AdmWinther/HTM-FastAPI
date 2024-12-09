import os
from uuid import uuid4

from Service import S00_Database


class OrganizationalRoleService:
    @classmethod
    async def resetOrganizationalRoleTable(cls):
        query = []
        query.append("DELETE FROM organizationalRoles where 1=1")
        OrganizetionalRole = os.getenv("OrganizationalRole")
        for role in organizationalRole:
            query.append(f"INSERT INTO organizationalRoles (id, role) VALUES ('{uuid4()}, {role}')")
        return Database.execute_query(query=query)