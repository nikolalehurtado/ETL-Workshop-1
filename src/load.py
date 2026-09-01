from sqlalchemy import create_engine
import pandas as pd


def get_engine(password: str, host: str = 'localhost', port: int = 3306,
               database: str = 'recruitment_dw', user: str = 'root'):
    """
    Crea la conexión (engine) hacia la base de datos MySQL.
    """
    connection_string = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
    engine = create_engine(connection_string)
    return engine


def load_dimension(df: pd.DataFrame, table_name: str, engine):
    """
    Carga un DataFrame de dimensión (o hecho) a su tabla correspondiente en MySQL.
    """
    df.to_sql(table_name, con=engine, if_exists='append', index=False)
    print(f"Cargados {len(df)} registros en la tabla '{table_name}'.")


if __name__ == "__main__":
    import getpass
    from extract import extract_data
    from transform import prepare_data, apply_business_rules
    from dimensional_model import (
        create_dim_date, create_dim_technology, create_dim_candidate_profile,
        create_dim_country, create_dim_candidate, create_fact_applications
    )

    # 1. Pipeline completo (Extract -> Transform -> Dimensional Model)
    df_raw = extract_data('../data/raw/candidates.csv')
    df_prepared = prepare_data(df_raw)
    df_transformed = apply_business_rules(df_prepared)

    dim_date = create_dim_date(df_transformed)
    dim_technology = create_dim_technology(df_transformed)
    dim_profile = create_dim_candidate_profile(df_transformed)
    dim_country = create_dim_country(df_transformed)
    dim_candidate = create_dim_candidate(df_transformed)

    fact_applications = create_fact_applications(
        df_transformed, dim_date, dim_technology, dim_profile, dim_country, dim_candidate
    )

    # 2. Conexión a MySQL
    password = getpass.getpass("Contraseña de MySQL root: ")
    engine = get_engine(password)
    print("Conexión establecida correctamente.")

    # 3. Cargar en el orden correcto: Dimensiones -> Hechos
    load_dimension(dim_date, 'DimDate', engine)
    load_dimension(dim_technology, 'DimTechnology', engine)
    load_dimension(dim_profile, 'DimCandidateProfile', engine)
    load_dimension(dim_country, 'DimCountry', engine)
    load_dimension(dim_candidate, 'DimCandidate', engine)
    load_dimension(fact_applications, 'FactApplications', engine)

    print("\n¡Carga completa del Data Warehouse finalizada!")


    