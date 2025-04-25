from fastapi import FastAPI

from src.apps.mms.endpoint import router as mms_router
from src.apps.root.endpoint import router as root_router

app = FastAPI(
    title="Mercado Bitcoin Challenge",
    description="API for Mercado Bitcoin Challenge",
    version="1.0",
)


app.include_router(mms_router, tags=["mms"])
app.include_router(root_router, tags=["root"])
