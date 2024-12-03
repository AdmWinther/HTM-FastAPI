import uuid

from fastapi import Request

from Controller import JWTtoken

from Service import Database

class CSRFService:
    @classmethod
    async def getCsrfToken(self, userId: str):
        try:
            CsrfToken = self.generateCSRFToken()

            query = [
                    # delete the old CSRF token
                    f"DELETE FROM CSRFToken WHERE userId = '{userId}'",
                     # insert the new CSRF token
                     f"INSERT INTO CSRFToken (userId, token) VALUES ('{userId}', '{CsrfToken}')"]
            await Database.execute_transaction(query)
            return CsrfToken
        except Exception as e:
            return f"Error: {e}"

    @classmethod
    async def validateCSRFToken(self, request: Request, csrfToken: str):
        try:
            userId = JWTtoken.getUserIdFromRequest(request)
            query = f"SELECT * FROM csrf_tokens WHERE userId = '{userId}'"
            result = await Database.execute_query(query)
            if len(result) == 0:
                return False
            if len(result) > 1:
                return f"Error: More than one CSRF token found for user {userId}"
            else:
                if(result[0]["token"] != csrfToken):
                    return False
                return True
        except Exception as e:
            return f"Error: {e}"

    @classmethod
    async def deleteCSRFToken(self, request: Request):
        try:
            userId = JWTtoken.getUserIdFromRequest(request)
            query = f"DELETE * FROM csrf_tokens WHERE userId = '{userId}'"
            await Database.execute_query(query)
            return True
        except Exception as e:
            return f"Error: {e}"


    @classmethod
    def generateCSRFToken(self):
        return str(uuid.uuid4())