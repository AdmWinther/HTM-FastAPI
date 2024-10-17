from pydantic import BaseModel
from typing_extensions import Optional


class Project(BaseModel):
    id: Optional[str]
    name: str
    description: Optional[str]
    organizationId: str
    projectManagerId: str