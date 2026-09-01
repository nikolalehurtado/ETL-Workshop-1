import pandas as pd


def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepara los datos crudos: corrige tipos de datos y formatos.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame crudo, tal como sale de extract_data().

    Returns
    -------
    pd.DataFrame
        DataFrame con los tipos de datos corregidos.
    """
    df = df.copy()

    # Convertir Application Date de texto a fecha real
    df['Application Date'] = pd.to_datetime(df['Application Date'])

    print("Preparación completada.")
    print(f"Tipo de 'Application Date' ahora es: {df['Application Date'].dtype}")

    return df


def apply_business_rules(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica la regla de negocio de contratación (HIRED).

    Regla: HIRED = (Code Challenge Score >= 7) AND (Technical Interview Score >= 7)

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame ya preparado (salida de prepare_data()).

    Returns
    -------
    pd.DataFrame
        DataFrame con la nueva columna 'is_hired' (1 = contratado, 0 = no contratado).
    """
    df = df.copy()

    df['is_hired'] = (
        (df['Code Challenge Score'] >= 7) &
        (df['Technical Interview Score'] >= 7)
    ).astype(int)

    total_hired = df['is_hired'].sum()
    total_applications = len(df)
    print(f"Regla de negocio aplicada: {total_hired} de {total_applications} candidatos contratados "
          f"({total_hired / total_applications:.1%})")

    return df


if __name__ == "__main__":
    from extract import extract_data

    df_raw = extract_data('../data/raw/candidates.csv')
    df_prepared = prepare_data(df_raw)
    df_transformed = apply_business_rules(df_prepared)

    print(df_transformed[['Code Challenge Score', 'Technical Interview Score', 'is_hired']].head(10))