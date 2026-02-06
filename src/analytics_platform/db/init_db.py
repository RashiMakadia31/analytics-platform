from db.connection import engine

with engine.begin() as conn:
    with open("db/schema.sql", "r") as f:
        sql = f.read()
        conn.exec_driver_sql(sql)

print("Database schema created successfully")
