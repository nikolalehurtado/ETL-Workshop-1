from sqlalchemy import create_engine
import pandas as pd


def get_engine(password: str, host: str = 'localhost', port: int = 3306,
               database: str = 'recruitment_dw', user: str = 'root'):
    """
    Crea la conexión (engine) hacia la base de datos MySQL.

    Parameters
    ----------
    password : str
        Contraseña del usuario MySQL.
    host, port, database, user : str/int
        Parámetros de conexión (valores por defecto ya configurados
        según la instalación local).

    Returns
    -------
    sqlalchemy.Engine
    """
    connection_string = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
    engine = create_engine(connection_string)
    return engine
def clear_tables(engine):
    """
    Vacía todas las tablas del Data Warehouse, en el orden correcto
    (primero la tabla de hechos, por las llaves foráneas; luego las
    dimensiones), para permitir recargar el pipeline sin duplicar datos.
    """
    from sqlalchemy import text

    tables_in_order = [
        'FactApplications',   # primero, porque depende de las demás (FK)
        'DimDate',
        'DimTechnology',
        'DimCandidateProfile',
        'DimCountry',
        'DimCandidate'
    ]

    with engine.connect() as connection:
        for table in tables_in_order:
            connection.execute(text(f"DELETE FROM {table}"))
            connection.commit()
            print(f"Tabla '{table}' vaciada.")

def load_dimension(df: pd.DataFrame, table_name: str, engine):
    """
    Carga un DataFrame (dimensión o hecho) a su tabla correspondiente en MySQL.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame a cargar.
    table_name : str
        Nombre exacto de la tabla destino en MySQL.
    engine : sqlalchemy.Engine
        Conexión activa hacia la base de datos.
    """
    df.to_sql(table_name, con=engine, if_exists='append', index=False)
    print(f"Cargados {len(df)} registros en la tabla '{table_name}'.")