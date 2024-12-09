import os

from pydantic import BaseModel
from typing_extensions import Optional


class Project(BaseModel):
    id: Optional[str]
    name: str
    description: Optional[str]
    organizationId: str
    projectManagerId: str

    @classmethod
    def isProjectNameValid(cls, name: str):
        try:
            if len(name) == 0: raise ValueError("Project name must contain at least one character.")

            if len(name) > int(os.getenv("MAX_PROJECT_NAME_LENGTH")): raise ValueError("Project name too long.")

        except ValueError as e:
            raise ValueError(e)
        # Check if the last name is valid