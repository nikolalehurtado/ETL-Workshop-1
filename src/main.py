import getpass
from extract import extract_data
from transform import prepare_data, apply_business_rules
from dimensional_model import (
    create_dim_date, create_dim_technology, create_dim_candidate_profile,
    create_dim_country, create_dim_candidate, create_fact_applications
)
from load import get_engine, clear_tables, load_dimension

def run_pipeline():
    """
    Ejecuta el pipeline ETL completo:
    Extract -> Prepare -> Business Rules -> Dimensional Model -> Load
    """
    print("=" * 60)
    print("INICIANDO PIPELINE ETL - Workshop 1")
    print("=" * 60)

    # 1. EXTRACT
    print("\n--- Task 3.1: Extract ---")
    df_raw = extract_data('../data/raw/candidates.csv')

    # 2. DATA PREPARATION
    print("\n--- Task 3.2: Data Preparation ---")
    df_prepared = prepare_data(df_raw)

    # 3. BUSINESS TRANSFORMATION
    print("\n--- Task 3.3: Business Transformation ---")
    df_transformed = apply_business_rules(df_prepared)

    # 4. DIMENSIONAL TRANSFORMATION
    print("\n--- Task 4: Dimensional Transformation ---")
    dim_date = create_dim_date(df_transformed)
    dim_technology = create_dim_technology(df_transformed)
    dim_profile = create_dim_candidate_profile(df_transformed)
    dim_country = create_dim_country(df_transformed)
    dim_candidate = create_dim_candidate(df_transformed)

    fact_applications = create_fact_applications(
        df_transformed, dim_date, dim_technology, dim_profile, dim_country, dim_candidate
    )

   
    # 5. LOAD
    print("\n--- Task 5: Load ---")
    password = getpass.getpass("Contraseña de MySQL root: ")
    engine = get_engine(password)
    print("Conexión establecida correctamente.")

    print("\nVaciando tablas existentes (para evitar duplicados)...")
    clear_tables(engine)

    load_dimension(dim_date, 'DimDate', engine)
    load_dimension(dim_technology, 'DimTechnology', engine)
    load_dimension(dim_profile, 'DimCandidateProfile', engine)
    load_dimension(dim_country, 'DimCountry', engine)
    load_dimension(dim_candidate, 'DimCandidate', engine)
    load_dimension(fact_applications, 'FactApplications', engine)


if __name__ == "__main__":
    run_pipeline()