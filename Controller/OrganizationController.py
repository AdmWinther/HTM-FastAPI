from fastapi import APIRouter

from Service.OrganizationService import OrganizationService

router = APIRouter()

@router.get("")
async def getAllOrganizations():
    return await OrganizationService.getAllOrganizations()

@router.post("")
async def post_organization(organizationInfo : dict):
    return await OrganizationService.addOrganization(organizationInfo)