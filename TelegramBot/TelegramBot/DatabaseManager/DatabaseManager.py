import pyodbc
import json

CONNECTION_STRING = (
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=<Server>"
    "Database=DB_AI_assistent;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

class DatabaseManager:
    def __init__(self, connection_string=CONNECTION_STRING):
        self.connection_string = connection_string
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = pyodbc.connect(self.connection_string)
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()

    def execute_query(self, query, params=None):
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchone()
        except Exception as e:
            print("Ошибка выполнения запроса:", e)
            return None

    def execute_non_query(self, query, params=None):
        try:
            self.cursor.execute(query, params or ())
            self.conn.commit()
        except Exception as e:
            print("Ошибка выполнения запроса:", e)

        
    def get_incomplete_context(self):
        with DatabaseManager(CONNECTION_STRING) as db:
            json_query = """
            DECLARE @JsonResult NVARCHAR(MAX);
            SET @JsonResult = (SELECT ts_request_number, ts_query FROM TS_request FOR JSON AUTO);
            SELECT @JsonResult;
            """
            result = db.execute_query(json_query)
            
            return result[0]
    
    def get_full_context(self, number_query):
        with DatabaseManager(CONNECTION_STRING) as db:
            query = "SELECT ts_request_number, ts_query, ts_answer FROM TS_request WHERE ts_request_number = ?;"
            result = db.execute_query(query, (number_query,))

            result_dict = {"ts_request_number": result[0], "ts_query": result[1], "ts_answer": result[2]}

            return result_dict
    
    def save_record_on_log_table(self, record):
        try:
            with DatabaseManager(CONNECTION_STRING) as db:
                query = "INSERT INTO Log_Table (username, user_query, log_request_number, LLM_answer) VALUES (?, ?, ?, ?);"
                result = db.execute_non_query(query, record)
                
            return True
        
        except Exception as e:
            print(f"Произошла ошибка при выполнении запроса: {e}")
            
            return False