import os
from enum import Enum
from symtable import Class
from uuid import uuid4
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from passlib.context import CryptContext
from typing_extensions import Optional

# Create a new instance of CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(BaseModel):
    # field id is optional
    id:Optional[str] = None
    name: str
    lastName: str
    emailAddress: str
    password: str
    # todo: define roles class
    # role: str = "user"



    # Create the constructor
    def __init__(self, name: str, lastName: str, emailAddress: str, password: str, id: Optional[str] = None):
        load_dotenv()
        # check if the id is None, if it is, then generate a new id
        if id is None:
            id = str(uuid4())

        # check if the email address is valid
        self.validateNewUserInfo(name, lastName, emailAddress)

        super().__init__(
            name=name,
            lastName=lastName,
            emailAddress=emailAddress,
            password=password,
            id=id)

    @classmethod
    def isFirstNameValid(cls, name: str):
        load_dotenv()
        if len(name) == 0: raise ValueError("Name must contain at least one character")
        if not name.isalpha():
            raise ValueError("Name must contain only alphabetic characters")
        if len(name) > int(os.getenv("MAX_USER_NAME_LENGTH")):
            raise ValueError(f"Name must contain at most {os.getenv("MAX_USER_NAME_LENGTH")} characters")
        return True

    @classmethod
    def isLastNameValid(cls, name: str):
        load_dotenv()
        if len(name) == 0: raise ValueError("Last name must contain at least one character")
        if not name.isalpha(): raise ValueError("Last name must contain only alphabetic characters")
        if len(name) > int(os.getenv("MAX_USER_NAME_LENGTH")):
            raise ValueError(f"Last name must contain at most {os.getenv("MAX_USER_NAME_LENGTH")} characters")
        return True

    # @classmethod
    # def userFromDict(cls, userInfo: dict):
    #     # Control if the dictionary has the required fields
    #     if "name" not in userInfo:raise ValueError("Dictionary must contain a name field")
    #     if "lastName" not in userInfo:raise ValueError("Dictionary must contain a lastName field")
    #     if "emailAddress" not in userInfo:raise ValueError("Dictionary must contain an emailAddress field")
    #     if "password" not in userInfo:raise ValueError("Dictionary must contain a password field")
    #     if "id" in userInfo: raise ValueError("Dictionary must not contain an id field")
    #     userInfo["id"] = str(uuid4())
    #     return User(
    #         name=userInfo["name"],
    #         lastName=userInfo["lastName"],
    #         emailAddress=userInfo["emailAddress"],
    #         password=userInfo["password"],
    #         id=userInfo["id"]
    #     )

    @classmethod
    def get_password_hash(cls, password: str) -> str:
        return pwd_context.hash(password)

    @classmethod
    # Validate if the user information is valid and a new user object can be created from the information
    def validateNewUserInfo(cls, name, lastName, emailAddress):
        from Model.Entity.Email import Email
        try:
            isEmailValid = Email.isValidEmailAddress(emailAddress)
            if os.getenv("VERBOSE") == "True": print(f"Email address validation returned {isEmailValid}")
        except ValueError as e:
            raise ValueError(e)
        # Check if the name is valid
        try:
            isNameValid = User.isFirstNameValid(name)
            if os.getenv("VERBOSE") == "True": print(f"First name validation returned {isNameValid}")
        except ValueError as e:
            raise ValueError(e)
        # Check if the last name is valid
        try:
            isLastNameValid = User.isLastNameValid(lastName)
            if os.getenv("VERBOSE") == "True": print(f"Last name validation returned {isLastNameValid}")
        except ValueError as e:
            raise ValueError(e)