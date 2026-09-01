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

    bins = [-1, 5, 10, 15, 20, 25, 30]
    labels = ['0-5', '6-10', '11-15', '16-20', '21-25', '26-30']
    df['yoe_range'] = pd.cut(df['YOE'], bins=bins, labels=labels)

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


def create_fact_applications(df: pd.DataFrame, dim_date: pd.DataFrame,
                               dim_technology: pd.DataFrame, dim_profile: pd.DataFrame,
                               dim_country: pd.DataFrame, dim_candidate: pd.DataFrame) -> pd.DataFrame:
    """
    Crea la Tabla de Hechos FactApplications, mapeando cada aplicación
    a las llaves subrogadas de sus 5 dimensiones correspondientes.
    """
    df = df.copy()

    bins = [-1, 5, 10, 15, 20, 25, 30]
    labels = ['0-5', '6-10', '11-15', '16-20', '21-25', '26-30']
    df['yoe_range'] = pd.cut(df['YOE'], bins=bins, labels=labels)

    fact = df.merge(
        dim_date[['date_key', 'full_date']],
        left_on='Application Date', right_on='full_date', how='left'
    )

    fact = fact.merge(
        dim_technology[['technology_key', 'technology_name']],
        left_on='Technology', right_on='technology_name', how='left'
    )

    fact = fact.merge(
        dim_profile[['profile_key', 'seniority', 'yoe_range']],
        left_on=['Seniority', 'yoe_range'], right_on=['seniority', 'yoe_range'], how='left'
    )

    fact = fact.merge(
        dim_country[['country_key', 'country_name']],
        left_on='Country', right_on='country_name', how='left'
    )

    fact = fact.merge(
        dim_candidate[['candidate_key', 'email']],
        left_on='Email', right_on='email', how='left'
    )

    fact_applications = fact[[
        'date_key', 'technology_key', 'profile_key', 'country_key', 'candidate_key',
        'Code Challenge Score', 'Technical Interview Score', 'is_hired'
    ]].copy()

    fact_applications = fact_applications.rename(columns={
        'Code Challenge Score': 'code_challenge_score',
        'Technical Interview Score': 'technical_interview_score'
    })

    fact_applications['application_count'] = 1
    fact_applications.insert(0, 'application_key', range(1, len(fact_applications) + 1))

    print(f"FactApplications creada: {len(fact_applications)} aplicaciones.")

    nulls = fact_applications[['date_key', 'technology_key', 'profile_key',
                                 'country_key', 'candidate_key']].isnull().sum()
    print("Verificación de referencias inválidas (deben ser todas 0):")
    print(nulls)

    return fact_applications