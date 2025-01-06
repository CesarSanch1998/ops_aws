from fastapi import APIRouter, Request
import json
from scripts.OPS import *
from puresnmp_olt.accions import Get,Get_async
from schema.ops_model import ClientList
from fastapi.responses import StreamingResponse

OPS_request = APIRouter()

@OPS_request.get("/")
async def ops_clients():
    return {"message": "Hello World"}

@OPS_request.post("/")
async def ops_clients(data: ClientList):
    # body = await request.body()  # Obtener el cuerpo de la solicitud
    # data = json.loads(body) 
    for client in data.clients:
        request = await client_operate(client)
        res = StreamingResponse(request, media_type="application/json")
        # res = await client_operate(client)
        print(res)
        print(request)
        # print(data)
    return request