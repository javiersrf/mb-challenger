from fastapi import APIRouter


router = APIRouter(
    prefix="/",
    tags=["mms"],
)


@router.get("/healthcheck", status_code=200)
async def healthcheck():
    return {"message": "All systems operational"}