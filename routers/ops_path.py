from fastapi import APIRouter, Request
import json

OPS_request = APIRouter()

@OPS_request.get("/")
async def ops_clients():
    return {"message": "Hello World"}

@OPS_request.post("/")
async def ops_clients(request: Request):
    body = await request.body()  # Obtener el cuerpo de la solicitud
    data = json.loads(body) 
    # with open(f"datosdelodoo.json", "a") as archivo_json:
    #     json.dump(data, archivo_json, indent=4)
    print(data)
    return data