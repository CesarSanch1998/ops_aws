import os
from typing import Generator

from dotenv import load_dotenv
from sqlalchemy import create_engine, orm
from models.client import client_db
from puresnmp_olt.accions import Set,Set_async,Get ,Get_async
from puresnmp_olt.tools import ascii_to_hex
from config.definitions import olt_devices
import os
import json
from datetime import datetime
from dotenv import load_dotenv
from utils.fsp import calcular
import json
from datetime import datetime

# Integrate the previous code for database connection
from db.connection import get_db # Assuming this points to the SessionLocal function


load_dotenv()

async def client_operate(data):
    action = data.action
    operation = 1 if "R" in action.upper() else 2  # 1 is active and 2 is deactivate

    try:
        # Use the session obtained from the session_local function
        session: orm.Session = next(get_db())

        returned = session.query(client_db).filter(client_db.contract == data.contract).first()
        if returned is None:
            resp = {
                "message": "The required OLT & ONT does not exists in DB",
                "contract": data.contract,
            }
            try:
                filename = "registro_corte_" + datetime.now().strftime("%Y-%m-%d") + ".json"
                with open(filename, mode="a") as f:
                    json_string = json.dumps(resp, indent=4)
                    f.write(json_string)
            except PermissionError:
                print(f"Error: No tienes permiso para escribir en el archivo {filename}")
            return resp
        else:
            print(f"Client Get Succefully {returned.contract} {returned.name_1}")
            resp = await comparer(returned, operation,session)
            try:
                filename = "registro_corte_" + datetime.now().strftime("%Y-%m-%d") + ".json"
                with open(filename, mode="a") as f:
                    json_string = json.dumps(resp, indent=4)
                    f.write(json_string)
            except PermissionError:
                print(f"Error: No tienes permiso para escribir en el archivo {filename}")

        return resp
    except Exception as e:
        # Use the rollback method on the session object
        session.rollback()
        raise e  # Or handle the exception differently
    finally:
        # Close the session automatically with the 'with' statement
        session.close()  # No need to call conn.close() anymore

async def comparer(db_data,operation, session: orm.Session):

    # fsp_buscado = f"{str(db_data.fsp)}"

    oid_puerto = calcular(str(db_data.fsp))
    oid,get_serial = await Get_async(olt_devices[str(db_data.olt)],os.environ['SNMP_READ'],f"1.3.6.1.4.1.2011.6.128.1.1.2.43.1.3.{oid_puerto}.{db_data.onu_id}")
    print(oid)
    serial_up = ascii_to_hex(get_serial).upper()
    if serial_up == db_data.sn:
        print(f"Client SN similar {db_data.contract} {db_data.name_1}")
        resp = await action(db_data,oid_puerto,operation,session)
        return resp
    else:
        print("Client SN not similar")
        resp = {
        "message": f"Sn not similar SN-OLT:{serial_up} SN-DB:{db_data.sn}",
        "contract": db_data.contract,
    }
        return resp
            
    return resp

async def action(db_data,oid_puerto,operation, session: orm.Session):
    resulted_operation = "active" if  operation == 1 else "deactivated"
    result = "Reactivado" if operation == 1 else "Suspendido"
    try:
        change_status = await Set_async(olt_devices[str(db_data.olt)],os.environ['SNMP_READ'],f"1.3.6.1.4.1.2011.6.128.1.1.2.46.1.1.{oid_puerto}.{db_data.onu_id}",operation,'int')
        # print(change_status)
        if change_status['Cod'] == 404:
            # print("Error")
            return {
                "message": "No such name/oid",
                "contract": db_data.contract,
            }
        elif change_status['Cod'] == 200:
            # print(f"Client Changed State {db_data.contract} {db_data.name_1} to {resulted_operation}")
            db_data.state = resulted_operation
            session.add(db_data)
            session.commit()
            resp = {
                "message": f"Client Changed State {db_data.name_1} {db_data.name_2} to {resulted_operation}",
                "contract": db_data.contract,
            }
            return resp 
        return resp
    except Exception as e:
        session.rollback()
        raise e  # o maneja la excepción de otra manera (registra el error, devuelve un mensaje, etc.)
    finally:
        session.close()

