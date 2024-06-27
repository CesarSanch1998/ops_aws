from db.connection import session,conn
from models.client import client_db

def client_operate(data):
    action = data["action"]
    operation = "activate" if "R" in action else "deactivate"
    resulted_operation = "active" if "R" in action else "deactivated"
    result = "Reactivado" if "R" in action else "Suspendido"

    try:
        returned = session.query(client_db).filter(client_db.contract == data['contract']).first()
        if returned == None:
            return "Cliente No existe en la DB"
        else:
            print(f"Client Get Succefully {returned.contract} {returned.name_1}")
        return data
    except Exception as e:
        session.rollback()
        raise e  # o maneja la excepción de otra manera (registra el error, devuelve un mensaje, etc.)
    finally:
        session.close()
        conn.close()
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