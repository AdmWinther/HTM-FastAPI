from enum import Enum

# Create an Enum class named Role
class Role(str, Enum):
    user = "user"
    admin = "admin"
    superuser = "superUser"
    organizationAdmin = "organizationAdmin"