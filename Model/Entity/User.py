import os
from enum import Enum
from symtable import Class
from uuid import uuid4
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from pydantic.v1 import UUID4
from typing_extensions import Optional

# create a class named user with fields name, email, password
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
            if os.getenv("VERBOSE") == "True": print(f"Last name validation returned {isNameValid}")
        except ValueError as e:
            raise ValueError(e)

        super().__init__(
            name=name,
            lastName=lastName,
            emailAddress=emailAddress,
            password=password,
            id=id)

    def isFirstNameValid(name: str):
        load_dotenv()
        if(len(name) == 0): raise ValueError("Name must contain at least one character")
        if not name.isalpha():
            raise ValueError("Name must contain only alphabetic characters")
        if(len(name) > int(os.getenv("MAX_USER_NAME_LENGTH"))):
            raise ValueError(f"Name must contain at most {os.getenv("MAX_USER_NAME_LENGTH")} characters")
        return True

    def isLastNameValid(name: str):
        load_dotenv()
        if(len(name) == 0): raise ValueError("Last name must contain at least one character")
        if not name.isalpha(): raise ValueError("Last name must contain only alphabetic characters")
        if(len(name) > int(os.getenv("MAX_USER_NAME_LENGTH"))):
            raise ValueError(f"Last name must contain at most {os.getenv("MAX_USER_NAME_LENGTH")} characters")
        return True