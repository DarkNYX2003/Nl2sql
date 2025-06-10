from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from .model import generate_sql
from .db_utils import get_db_schema, retrieve_schema, execute_sql_query

router = APIRouter()
schema_docs = get_db_schema()

@router.get("/query")
def handle_query(question: str = Query(...)):
    try:
        schema = retrieve_schema(schema_docs)
        prompt = f"""### Instruction:
Convert the following question to a SQL query.

### Schema:
{schema}

### Relationships:
- CUSTOMERS.CUSTOMER_ID → ORDERS.CUSTOMER_ID
- ORDERS.ORDER_ID → ORDER_PAYMENTS.ORDER_ID

### Question:
{question}

### SQL Query:
"""
        prompt = prompt[:4096]
        sql = generate_sql(prompt)
        result = execute_sql_query(sql)

        if "error" in result:
            return JSONResponse(status_code=500, content={"sql": sql, "error": result["error"]})
        return {"sql": sql, "result": result}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
