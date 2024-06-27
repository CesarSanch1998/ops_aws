from fastapi import FastAPI
from routers.ops_path import OPS_request

app = FastAPI()

app.include_router(OPS_request)