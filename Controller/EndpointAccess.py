#This file contains the access control for the endpoints
#The access control is based on the user role and the endpoint
#The access control is implemented in MySecurityMiddleware.py


accessRoles = {
    "GET": {
        "/api/user/all": ["ADMIN", "SUPERUSER", "SUPPORTER"],
        "/api/user/reset": ["ADMIN"],
        "/api/user/id/{userId}": ["ADMIN"],
        "/api/user/email/{emailAddress}": ["ADMIN"],
        "/api/user/userRole": ["ADMIN", "USER", "SUPERUSER", "SUPPORTER"],

        "/api/role/getAll": ["ADMIN"],
        "/api/role/reset": ["ADMIN"],

        "/api/organization/all": ["ADMIN"],

        "/api/csrf/": ["ADMIN", "USER", "SUPERUSER", "SUPPORTER"],
    },
    "POST": {
        "/api/user": ["ADMIN", "SUPERUSER"],
        "/api/organization/new": ["ADMIN"],
        "/logout": ["ADMIN", "USER", "SUPERUSER", "SUPPORTER"],
    },
}

csrfProtection = {
    "GET": {
        "version": False,

        "/api/user/all": False,
        "/api/user/reset": False,
        "/api/user/id/{userId}": False,
        "/api/user/email/{emailAddress}": False,
        "/api/user/userRole": False,

        "/api/role/getAll": False,
        "/api/role/reset": False,

        "/api/organization/all": False,

        "/api/csrf/": False
    },
    "POST": {
        "version": False,

        "/api/user": True,

        "/api/organization/new": True,

        "/login": False,
        "/logout": False,
    },
}