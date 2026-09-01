import pandas as pd


def create_dim_date(df: pd.DataFrame) -> pd.DataFrame:
    """
    Crea la dimensión DimDate a partir de las fechas únicas de aplicación.
    """
    unique_dates = df['Application Date'].drop_duplicates().sort_values().reset_index(drop=True)

    dim_date = pd.DataFrame({'full_date': unique_dates})
    dim_date['date_key'] = dim_date.index + 1
    dim_date['year'] = dim_date['full_date'].dt.year
    dim_date['month'] = dim_date['full_date'].dt.month
    dim_date['quarter'] = dim_date['full_date'].dt.quarter
    dim_date = dim_date[['date_key', 'full_date', 'year', 'month', 'quarter']]

    print(f"DimDate creada: {len(dim_date)} fechas únicas.")
    return dim_date


def create_dim_technology(df: pd.DataFrame) -> pd.DataFrame:
    """
    Crea la dimensión DimTechnology a partir de las tecnologías únicas.
    """
    unique_tech = df['Technology'].drop_duplicates().sort_values().reset_index(drop=True)

    dim_technology = pd.DataFrame({'technology_name': unique_tech})
    dim_technology['technology_key'] = dim_technology.index + 1
    dim_technology = dim_technology[['technology_key', 'technology_name']]

    print(f"DimTechnology creada: {len(dim_technology)} tecnologías únicas.")
    return dim_technology


def create_dim_candidate_profile(df: pd.DataFrame) -> pd.DataFrame:
    """
    Crea la dimensión DimCandidateProfile combinando Seniority y rangos de YOE.
    """
    df = df.copy()

    # Crear rangos de YOE (0-5, 6-10, 11-15, 16-20, 21-25, 26-30)
    bins = [-1, 5, 10, 15, 20, 25, 30]
    labels = ['0-5', '6-10', '11-15', '16-20', '21-25', '26-30']
    df['yoe_range'] = pd.cut(df['YOE'], bins=bins, labels=labels)

    # Combinaciones únicas de Seniority + yoe_range
    unique_profiles = df[['Seniority', 'yoe_range']].drop_duplicates().sort_values(
        ['Seniority', 'yoe_range']
    ).reset_index(drop=True)

    dim_profile = unique_profiles.rename(columns={'Seniority': 'seniority'})
    dim_profile['profile_key'] = dim_profile.index + 1
    dim_profile = dim_profile[['profile_key', 'seniority', 'yoe_range']]

    print(f"DimCandidateProfile creada: {len(dim_profile)} perfiles únicos (seniority + rango YOE).")
    return dim_profile

def create_dim_candidate_profile(df: pd.DataFrame) -> pd.DataFrame:
    """
    Crea la dimensión DimCandidateProfile combinando Seniority y rangos de YOE.
    """
    df = df.copy()

    # Crear rangos de YOE (0-5, 6-10, 11-15, 16-20, 21-25, 26-30)
    bins = [-1, 5, 10, 15, 20, 25, 30]
    labels = ['0-5', '6-10', '11-15', '16-20', '21-25', '26-30']
    df['yoe_range'] = pd.cut(df['YOE'], bins=bins, labels=labels)

    # Combinaciones únicas de Seniority + yoe_range
    unique_profiles = df[['Seniority', 'yoe_range']].drop_duplicates().sort_values(
        ['Seniority', 'yoe_range']
    ).reset_index(drop=True)

    dim_profile = unique_profiles.rename(columns={'Seniority': 'seniority'})
    dim_profile['profile_key'] = dim_profile.index + 1
    dim_profile = dim_profile[['profile_key', 'seniority', 'yoe_range']]

    print(f"DimCandidateProfile creada: {len(dim_profile)} perfiles únicos (seniority + rango YOE).")
    return dim_profile

def create_dim_country(df: pd.DataFrame) -> pd.DataFrame:
    """
    Crea la dimensión DimCountry a partir de los países únicos.
    """
    unique_countries = df['Country'].drop_duplicates().sort_values().reset_index(drop=True)

    dim_country = pd.DataFrame({'country_name': unique_countries})
    dim_country['country_key'] = dim_country.index + 1
    dim_country = dim_country[['country_key', 'country_name']]

    print(f"DimCountry creada: {len(dim_country)} países únicos.")
    return dim_country

def create_dim_candidate(df: pd.DataFrame) -> pd.DataFrame:
    """
    Crea la dimensión DimCandidate a partir de los candidatos únicos (por email).
    """
    unique_candidates = df[['First Name', 'Last Name', 'Email']].drop_duplicates(
        subset=['Email']
    ).sort_values('Email').reset_index(drop=True)

    dim_candidate = unique_candidates.rename(columns={
        'First Name': 'first_name',
        'Last Name': 'last_name',
        'Email': 'email'
    })
    dim_candidate['candidate_key'] = dim_candidate.index + 1
    dim_candidate = dim_candidate[['candidate_key', 'first_name', 'last_name', 'email']]

    print(f"DimCandidate creada: {len(dim_candidate)} candidatos únicos (por email).")
    return dim_candidate



if __name__ == "__main__":
    from extract import extract_data
    from transform import prepare_data, apply_business_rules

    df_raw = extract_data('../data/raw/candidates.csv')
    df_prepared = prepare_data(df_raw)
    df_transformed = apply_business_rules(df_prepared)

    dim_date = create_dim_date(df_transformed)
    print(dim_date.head())

    dim_technology = create_dim_technology(df_transformed)
    print(dim_technology.head())

    dim_profile = create_dim_candidate_profile(df_transformed)
    print(dim_profile.head(10))

    dim_profile = create_dim_candidate_profile(df_transformed)
    print(dim_profile.head(10))

    dim_country = create_dim_country(df_transformed)
    print(dim_country.head())

    dim_candidate = create_dim_candidate(df_transformed)
    print(dim_candidate.head())