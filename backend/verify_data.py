# backend/verify_data.py

import sqlite3


def connect_to_database(db_path: str) -> sqlite3.Connection:
    """Establece conexión con la base de datos SQLite."""
    conn = sqlite3.connect(db_path)
    return conn


def show_tables(conn: sqlite3.Connection) -> None:
    """Muestra las tablas que existen en la base de datos."""
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    print("=== Tablas en la base de datos ===")
    for table in tables:
        print(f"- {table[0]}")
    print()


def count_rows(conn: sqlite3.Connection, table_name: str) -> None:
    """Muestra cuántas filas tiene una tabla."""
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]
    print(f"Tabla '{table_name}': {count} filas")


def show_columns(conn: sqlite3.Connection, table_name: str) -> None:
    """Muestra las columnas de una tabla."""
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()

    print(f"\n=== Columnas de la tabla '{table_name}' ===")
    for col in columns:
        print(f"- {col[1]} ({col[2]})")


def show_sample_data(conn: sqlite3.Connection, table_name: str, limit: int = 3) -> None:
    """Muestra algunas filas de ejemplo de una tabla."""
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name} LIMIT {limit}")
    rows = cursor.fetchall()

    print(f"\n=== Primeras {limit} filas de '{table_name}' ===")
    for row in rows:
        print(row)


def main():
    """Función principal de verificación."""
    DB_PATH = r"data\songs.db"

    conn = connect_to_database(DB_PATH)

    show_tables(conn)

    count_rows(conn, "song_features")
    count_rows(conn, "song_metadata")

    show_columns(conn, "song_features")
    show_columns(conn, "song_metadata")

    show_sample_data(conn, "song_features", limit=3)
    show_sample_data(conn, "song_metadata", limit=3)

    conn.close()
    print("\nVerificación completada.")


if __name__ == "__main__":
    main()