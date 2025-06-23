
from fastapi import FastAPI
from app.routers import ci

app = FastAPI(
    title="CMDB API",
    version="1.0.0"
)
## include the router for the CMDB
# (Configuration Management Database)

app.include_router(ci.router)

