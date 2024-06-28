from fastapi import APIRouter, Request
import json
from scripts.OPS import *
from puresnmp_olt.accions import Get,Get_async

OPS_request = APIRouter()

@OPS_request.get("/")
async def ops_clients():
    return {"message": "Hello World"}

@OPS_request.post("/")
async def ops_clients(request: Request):
    body = await request.body()  # Obtener el cuerpo de la solicitud
    data = json.loads(body) 
    for client in data["clients"]:
        res = await client_operate(client)
        print(res)
    return data