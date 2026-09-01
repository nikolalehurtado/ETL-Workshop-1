import pandas as pd


def extract_data(filepath: str) -> pd.DataFrame:
    """
    Extrae los datos crudos del archivo CSV de candidatos.

    Parameters
    ----------
    filepath : str
        Ruta al archivo candidates.csv

    Returns
    -------
    pd.DataFrame
        DataFrame con los datos crudos, sin transformar.
    """
    df = pd.read_csv(filepath, sep=';')
    print(f"Extracción completada: {df.shape[0]} filas, {df.shape[1]} columnas.")
    return df


# Bloque de prueba: solo se ejecuta si corres este archivo directamente
if __name__ == "__main__":
    df = extract_data('../data/raw/candidates.csv')
    print(df.head())