import os
from typing import List
from uuid import uuid4

from dotenv import load_dotenv
from pydantic import BaseModel
from typing_extensions import Optional

from Model.Entity.User import User


def validateNewOrganizationInfo(name, superuser_name, superuser_lastname, superuser_email, superuser_password):
    try:
        User.validateNewUserInfo(superuser_name, superuser_lastname, superuser_email)

    except ValueError as e:
        raise ValueError(e)

class Organization(BaseModel):
    id: Optional[str]
    name: str
    description: str

    def __init__(self,
                 id: Optional[str],
                 name: str,
                 description: Optional[str]):

        try:
            isOrganizationNameValid = Organization.isOrganizationNameValid(name)
            if id is None:
                id = str(uuid4())
            super().__init__(
                id=id,
                name=name,
                description=description,
            )
        except ValueError as e:
            raise ValueError(e)





    @classmethod
    def isOrganizationNameValid(cls, name: str):
        load_dotenv()
        if len(name) == 0: raise ValueError("Organization name must contain at least one character.")

        if len(name) > int(os.getenv("MAX_Organization_NAME_LENGTH")):
            raise ValueError(f"Organization name must contain at most {os.getenv("MAX_Organization_NAME_LENGTH")} characters")
        return True
