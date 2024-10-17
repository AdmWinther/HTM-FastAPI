from typing import List

from pydantic import BaseModel
from typing_extensions import Optional

from Model.Entity.User import User


class Organization(BaseModel):
    id: Optional[str]
    name: str
    description: str
    adminId: str

    def __init__(self,
                 id: str,
                 name: str,
                 adminName,
                 adminLastName,
                 adminEmailAddress,
                 adminPassword: Optional[str],
                 description: Optional[str]):

        try:
            organizationAdmin = User(
                name=adminName,
                lastName=adminLastName,
                emailAddress=adminEmailAddress,
                password=adminPassword
            )
        except ValueError as e:
            raise ValueError(e)

        super().__init__(
            id=id,
            name=name,
            description=description,
            adminId=organizationAdmin.id
        )