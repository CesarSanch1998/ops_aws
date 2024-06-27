from db.connection import session,conn
from models.client import client_db
from puresnmp_olt.accions import Set,Get
from puresnmp_olt.tools import ascii_to_hex
from config.definitions import olt_devices,map_ports
import os
from dotenv import load_dotenv

load_dotenv()

def client_operate(data):
    action = data["action"]
    operation = 1 if "R" in action else 2   #1 is active and 2 is deactivate
    resulted_operation = "active" if "R" in action else "deactivated"
    result = "Reactivado" if "R" in action else "Suspendido"

    try:
        returned = session.query(client_db).filter(client_db.contract == data['contract']).first()
        if returned == None:
            return {
            "message": "The required OLT & ONT does not exists",
            "contract": data["contract"],
        }
        else:
            print(f"Client Get Succefully {returned.contract} {returned.name_1}")
            resp = accion(returned)
        return resp
    except Exception as e:
        session.rollback()
        raise e  # o maneja la excepción de otra manera (registra el error, devuelve un mensaje, etc.)
    finally:
        session.close()
        conn.close()

def accion(db_data):
    fsp_buscado = f"{str(db_data.fsp)}"
    for oid_puerto, fsp_puerto in map_ports.items():
        if fsp_puerto == fsp_buscado:
            get_serial = Get(olt_devices[str(db_data.olt)],os.environ['SNMP_READ'],f"1.3.6.1.4.1.2011.6.128.1.1.2.43.1.3.{oid_puerto}.{db_data.onu_id}")
            print(get_serial)
            print(f"1.3.6.1.4.1.2011.6.128.1.1.2.43.1.3.{oid_puerto}.{db_data.onu_id}")
    return "Succefully"
    # value = Set(olt_devices[str(returned.olt)],os.environ['SNMP_READ'],"1.3.6.1.4.1.2011.6.128.1.1.2.46.1.1.4194312960.19",operation)
    # print(value)
    # payload["lookup_type"] = "C"
    # payload["lookup_value"] = {"contract":data["contract"], "olt": data.get("olt") or "*"}
    # req = db_request(endpoints["get_client"], payload)

    # if req["data"] is None:
    #     return {
    #         "message": "The required OLT & ONT does not exists",
    #         "contract": data["contract"],
    #     }

    # client = req["data"]
    # (command, quit_ssh) = ssh(olt_devices[str(client["olt"])])
    # command(f'interface gpon {client["frame"]}/{client["slot"]}')
    # command(f'ont {operation} {client["port"]} {client["onu_id"]}')

    # payload["change_field"] = "OX"
    # payload["new_values"] = {"state": resulted_operation}
    # req = db_request(endpoints["update_client"], payload)
    # message = f'Cliente {client["name_1"]} {client["name_2"]} {client["contract"]} ha sido {result}'
    # quit_ssh()

    # return {
    #     "message": message,
    #     "name": f'{client["name_1"]} {client["name_2"]} {client["contract"]}',
    #     "fspi": client["fspi"],
    #     "olt": client["olt"],
    #     "frame": client["frame"],
    #     "slot": client["slot"],
    #     "port": client["port"],
    #     "onu_id": client["onu_id"],
    #     "state": resulted_operation,
    # }