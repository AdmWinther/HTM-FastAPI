#This file contains the access control for the endpoints
#The access control is based on the user role and the endpoint
#The access control is implemented in MySecurityMiddleware.py


accessRoles = {
    "GET": {
        "/api/user": ["ADMIN", "USER", "SUPERUSER","READ-ONLY", "READ-WRITE", "APPROVE", "REVIEW"],
        "/api/user/reset": ["ADMIN"],
        "/api/user/id/{userId}": ["ADMIN"],
        "/api/user/email/{emailAddress}": ["ADMIN"],
        "/api/user/userRole": ["ADMIN"],

        "/api/role/getAll": ["ADMIN"],
        "/api/role/reset": ["ADMIN"],

        "/api/organization/all": ["ADMIN"],
    },
    "POST": {
        "/api/user": ["ADMIN"],
        "/api/organization/new": ["ADMIN"],
    },
}

CSRFProtection = {
    "GET": {
        "version": False,

        "/api/user": False,
        "/api/user/reset": True,
        "/api/user/id/{userId}": True,
        "/api/user/email/{emailAddress}": False,
        "/api/user/userRole": False,

        "/api/role/getAll": False,
        "/api/role/reset": False,

        "/api/organization/all": False,
    },
    "POST": {
        "version": False,

        "/api/user": True,

        "/api/organization/new": False,

        "/login": False
    },
}