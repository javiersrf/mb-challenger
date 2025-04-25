from fastapi import APIRouter


router = APIRouter(
    tags=["mms"],
)


@router.get("/healthcheck", status_code=200)
async def healthcheck():
    return {"status": "ok"}
