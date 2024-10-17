from fastapi import APIRouter

router = APIRouter()

@router.get("/item")
async def get_user():
    return "This is the route in User Controller."

