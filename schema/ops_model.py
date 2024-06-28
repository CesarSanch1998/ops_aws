from pydantic import BaseModel
from typing import Optional
from typing import ClassVar


class Client(BaseModel):
    contract: str 
    olt: int 
    action: str 

class ClientList(BaseModel):
    clients: list[Client]