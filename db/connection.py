# from psycopg import OperationalError
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# import os
# from dotenv import load_dotenv


# load_dotenv()

# engine = create_engine(f'postgresql+psycopg://{os.environ["DB_USER"]}:{os.environ["DB_PASSWORD"]}@{os.environ["DB_HOST"]}:5432/{os.environ["DB_NAME"]}')
# # engine.echo = True 
# try:
#     conn = engine.connect()
# except OperationalError as e:
#     print(f"Error de conexión a la base de datos: {e}")

# Session = sessionmaker(engine)
# session = Session()

import os
from typing import Generator

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session, sessionmaker

load_dotenv()

# Configuración de la base de datos desde variables de entorno
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")
DB_PORT = os.environ.get("DB_PORT", 5432)  # Puerto por defecto

# Construir la URL de la base de datos para psycopg2
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Crear el motor de SQLAlchemy con opciones de pooling y manejo de errores
try:
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,  # Verifica la conexión antes de usarla del pool
        pool_recycle=3600,  # Recicla las conexiones cada hora (ajustar según necesidad)
        pool_size=20, #Tamaño del pool de conexiones
        max_overflow=10, #Máximo de conexiones extras en caso de alta demanda
        connect_args={"connect_timeout": 5} #Tiempo máximo de espera para conectar
    )
    # Probar la conexión inmediatamente después de crear el motor
    engine.connect().close() #Cierra la conexión inmediatamente despues de probarla
    print("Conexión a la base de datos establecida correctamente (usando psycopg2).")
except OperationalError as e:
    print(f"Error al conectar a la base de datos: {e}")
    exit(1) #Sale del programa si no se puede conectar a la base de datos

# Crear la fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Función generadora para obtener una sesión
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()