#This file contains the access control for the endpoints
#The access control is based on the user role and the endpoint
#The access control is implemented in SecurityMiddleware.py


access = {
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