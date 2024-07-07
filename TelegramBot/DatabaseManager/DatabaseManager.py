import pyodbc

CONNECTION_STRING = (
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=DESKTOP-FTBUDIT\SQLEXPRESS;"
    "Database=DB_AI_assistent;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

class DatabaseManager:
    def __init__(self, connection_string):
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

def main():
    with DatabaseManager(CONNECTION_STRING) as db:
        # Первый запрос
        json_query = """
        DECLARE @JsonResult NVARCHAR(MAX);
        SET @JsonResult = (SELECT number, query FROM TS_request FOR JSON AUTO);
        SELECT @JsonResult;
        """
        result_one = db.execute_query(json_query)
        
        if result_one:
            print("Первый запрос успешно выполнен.")
            print("Результат в формате JSON:", result_one[0])
        else:
            print("Не удалось получить данные для первого запроса.")

        print()
        # Второй запрос с параметром
        number_param = 1  # Замените 1 на нужный номер
        result_two = db.execute_query("SELECT number, query, answer FROM TS_request WHERE number = ? FOR JSON AUTO;", (number_param,))
        
        if result_two:
            print("Второй запрос успешно выполнен.")
            print("Результат в формате JSON:", result_two[0])
        else:
            print("Не удалось получить данные для второго запроса.")

if __name__ == "__main__":
    main()
