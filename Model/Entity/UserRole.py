from typing import Optional
from uuid import uuid4

from pydantic.v1 import BaseModel

from Model.Entity.Role import Role


class UserRole(BaseModel):
    id: Optional[str] = None
    userId: str
    projectId: str
    role: Role

    def __init__(self, userId: str, projectId: str, role: str, id: Optional[str] = None):
        if id is None:
            id = str(uuid4())

        super().__init__(
            id=id,
            userId=userId,
            projectId=projectId,
            role=role
        )