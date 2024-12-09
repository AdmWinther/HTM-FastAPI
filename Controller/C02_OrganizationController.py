from uuid import uuid4

from fastapi import APIRouter
from starlette.responses import JSONResponse

from Controller import C01_UserController
from Model.Entity.Organization import Organization
from Service.S02_OrganizationService import OrganizationService
from Model.Entity.User import User
from Service.OrganizationalRolesService import OrganizationalRolesService
from Service.S01_UserService import UserService
from Service.userRoleToOrganizationService import userRoleToOrganizationService

organizationRouter = APIRouter()

@organizationRouter.get("/all")
async def getAllOrganizations():
    return await OrganizationService.getAllOrganizations()

@organizationRouter.post("/new")
async def post_organization(organizationInfo : dict):
    print("New organization endpoint is called.")
    try:
        justOrganization = {
            "id": str(uuid4()),
            "name": organizationInfo["organization_name"],
            "description": organizationInfo["description"]
        }
        Organization.isOrganizationNameValid(justOrganization["name"])

        justSuperUser = {
            "id": str(uuid4()),
            "name": organizationInfo["superuser_name"],
            "lastName": organizationInfo["superuser_lastname"],
            "emailAddress": organizationInfo["superuser_email"].lower(),
            "password": User.get_password_hash(organizationInfo["superuser_password"])
        }
        User.validateNewUserInfo(justSuperUser["name"], justSuperUser["lastName"], justSuperUser["emailAddress"])

        # control if the email is already registered for another user
        await UserService.IsThisEmailAddressAlreadyRegistered(justSuperUser["emailAddress"])

        #isSuperUserEmailRegistered = await UserService.getUserByEmail(justSuperUser["emailAddress"])
        #if len(isSuperUserEmailRegistered) > 0:
        #    raise ValueError("Email is already registered.")

        try:
            await UserService.addUserByDictNoValidation(justSuperUser)
        except ValueError as e:
            raise ValueError(f"Could not register superuser.{e}")

        try:
            # print(f"org_Contro: L48: justOrganization: {justOrganization}")
            await OrganizationService.addOrganization(justOrganization)
        except ValueError as e:
            raise ValueError(f"Superuser is registered but could not register organization.{e}")

        try:
            superUserRoleId = await OrganizationalRolesService.getRoleId("SUPERUSER")
            await userRoleToOrganizationService.setUserOrganization(justSuperUser["id"], justOrganization["id"], superUserRoleId)
        except ValueError as e:
            raise ValueError(f"Organization and superuser are both registered but Could not add the userToOrganization. {e}")

        return {"message": "Organization and superuser are registered successfully."}


    except ValueError as e:
        return {"error": str(e)}