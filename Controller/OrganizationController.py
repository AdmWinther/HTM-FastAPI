from fastapi import APIRouter

from Controller import UserController
from Model.Entity.Organization import Organization
from Service.OrganizationService import OrganizationService
from Model.Entity.User import User
from Service.UserService import UserService

organizationRouter = APIRouter()

@organizationRouter.get("/all")
async def getAllOrganizations():
    return await OrganizationService.getAllOrganizations()

@organizationRouter.post("/new")
async def post_organization(organizationInfo : dict):
    print("New organization endpoint is called.")
    try:
        justOrganization = {
            "name": organizationInfo["organization_name"],
            "description": organizationInfo["description"]
        }
        Organization.isOrganizationNameValid(justOrganization["name"])

        justSuperUser = {
            "name": organizationInfo["superuser_name"],
            "lastName": organizationInfo["superuser_lastname"],
            "emailAddress": organizationInfo["superuser_email"],
            "password": organizationInfo["superuser_password"]
        }
        User.validateNewUserInfo(justSuperUser["name"], justSuperUser["lastName"], justSuperUser["emailAddress"])

        isSuperUserEmailRegistered = await UserService.getUserByEmail(justSuperUser["emailAddress"])
        if len(isSuperUserEmailRegistered) > 0:
            raise ValueError("Email is already registered.")

        try:
            superUserRegister = await UserService.addUserByDictWithValidation(justSuperUser)
        except ValueError as e:
            raise ValueError(f"Could not register superuser.{e}")

        try:
            organizationRegister =  await OrganizationService.addOrganization(organizationInfo)
        except ValueError as e:
            raise ValueError(f"Superuser is registered but could not register organization.{e}")

        try:
            await UserController.addSuperUser(superUserRegister["id"], organizationRegister["id"])
        except ValueError as e:
            raise ValueError(f"Organization and superuser are both registered but Could not add the user as superuser of the organization.{e}")

        return {"message": f"Organization and superuser are registered successfully."}

    except ValueError as e:
        return {"message": f"Registering the new organization failed. {e}"}