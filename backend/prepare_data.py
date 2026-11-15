# backend/prepare_data.py

import pandas as pd
import sqlite3
from pathlib import Path
import re


def clean_column_name(name: str) -> str:
    """Limpia el nombre de una columna para que sea válido en SQLite."""
    name = name.strip()
    name = re.sub(r'[^a-zA-Z0-9_]', '_', name)  # Reemplaza cualquier caracter raro por _
    name = re.sub(r'_+', '_', name)             # Evita guiones bajos seguidos
    return name


def load_csvs(csv1_path: str, csv2_path: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Lee los dos archivos CSV y los retorna como DataFrames separados."""
    print("Leyendo archivos CSV...")

    df_features = pd.read_csv(csv1_path)
    df_metadata = pd.read_csv(csv2_path)

    print(f"Archivo 1 (features): {len(df_features)} filas")
    print(f"Archivo 2 (metadata): {len(df_metadata)} filas")

    return df_features, df_metadata


def create_database(db_path: str) -> sqlite3.Connection:
    """Crea y retorna una conexión a la base de datos SQLite."""
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    print(f"Base de datos creada en: {db_path}")
    return conn


def infer_sqlite_type(dtype) -> str:
    """Convierte un tipo de pandas a un tipo compatible con SQLite."""
    if pd.api.types.is_integer_dtype(dtype):
        return "INTEGER"
    elif pd.api.types.is_float_dtype(dtype):
        return "REAL"
    else:
        return "TEXT"


def create_table_from_dataframe(conn: sqlite3.Connection, table_name: str, df: pd.DataFrame) -> None:
    """Crea una tabla en SQLite usando los nombres de columnas limpios."""
    cursor = conn.cursor()
    
    # Elimina la tabla si ya existe (para evitar errores de columnas viejas)
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    
    cleaned_columns = [clean_column_name(col) for col in df.columns]
    
    columns_sql = []
    for col, original_col in zip(cleaned_columns, df.columns):
        col_type = infer_sqlite_type(df[original_col].dtype)
        columns_sql.append(f'"{col}" {col_type}')

    create_table_sql = f'CREATE TABLE {table_name} ({", ".join(columns_sql)})'
    
    cursor.execute(create_table_sql)
    conn.commit()
    print(f"Tabla '{table_name}' creada con {len(cleaned_columns)} columnas.")


def insert_data(conn: sqlite3.Connection, table_name: str, df: pd.DataFrame) -> None:
    """Inserta los datos usando nombres de columnas limpios."""
    df_clean = df.copy()
    df_clean.columns = [clean_column_name(col) for col in df_clean.columns]

    df_clean.to_sql(table_name, conn, if_exists="append", index=False)
    print(f"Datos insertados en la tabla '{table_name}'.")


def create_indexes(conn: sqlite3.Connection) -> None:
    """Crea índices básicos."""
    cursor = conn.cursor()
    try:
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_popularity ON song_features(Popularity)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_genre ON song_metadata(Genre)")
    except sqlite3.OperationalError:
        pass
    conn.commit()
    print("Índices creados (si las columnas existían).")


def main():
    """Función principal."""
    CSV1_PATH = r"data\music_characteristics.csv"
    CSV2_PATH = r"data\music_metadata.csv"
    DB_PATH = r"data\songs.db"

    df_features, df_metadata = load_csvs(CSV1_PATH, CSV2_PATH)

    conn = create_database(DB_PATH)

    create_table_from_dataframe(conn, "song_features", df_features)
    create_table_from_dataframe(conn, "song_metadata", df_metadata)

    insert_data(conn, "song_features", df_features)
    insert_data(conn, "song_metadata", df_metadata)

    create_indexes(conn)

    conn.close()
    print("Proceso completado exitosamente.")


if __name__ == "__main__":
    main()