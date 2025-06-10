import os
import oracledb
from dotenv import load_dotenv

load_dotenv()

TABLES = os.getenv("TABLES", "").split(",")
TABLES = [table.strip().upper() for table in TABLES if table.strip()]
ORACLE_USER = os.getenv("ORACLE_USER")
ORACLE_PASSWORD = os.getenv("ORACLE_PASSWORD")
ORACLE_DSN = os.getenv("ORACLE_DSN")

def get_db_schema():
    conn = oracledb.connect(user=ORACLE_USER, password=ORACLE_PASSWORD, dsn=ORACLE_DSN)
    cursor = conn.cursor()
    schema_docs = {}

    for table in TABLES:
        cursor.execute(f"""
            SELECT column_name 
            FROM user_tab_columns 
            WHERE table_name = '{table}'
        """)
        columns = cursor.fetchall()
        if columns:
            column_names = [col[0] for col in columns]
            schema_docs[table] = column_names

    conn.close()
    return schema_docs

def retrieve_schema(schema_docs):
    schema_text = ""
    for table, columns in schema_docs.items():
        schema_text += f"Table: {table}\n  - " + "\n  - ".join(columns) + "\n"
    return schema_text

def execute_sql_query(sql_query: str):
    try:
        conn = oracledb.connect(user=ORACLE
