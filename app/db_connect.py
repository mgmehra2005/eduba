import pymysql

class DBConnection:

    def __init__(self, config):
        if (pymysql.__version__):
            self.connect = pymysql.connect(
                                host=config.get("DB_HOST", "localhost"),
                                user=config.get("DB_USER", "root"),
                                password=config.get("DB_PASSWORD", ""),
                                db=config.get("DB_NAME", "eduba"),
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor
                                )
        else:
            raise ImportError("pymysql library is not installed or not found")
        

    def get_db_cursor(self, query):
        cursor = self.connect.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        return data
    
    def push_db_cursor(self, query):
        cursor = self.connect.cursor()
        cursor.execute(query)
        self.connect.commit()
        cursor.close()

    def close(self):
        self.connect.close()

    
# if __name__ == "__main__":
#     from app import app
#     db = DBConnection(app.config)
#     import time
#     problem = db.get_db_cursor("select problem_text from exercise where concept_id = 1 and exercise_id = 1;")
#     hints = db.get_db_cursor("select * from hints")
#     print(problem[0]['problem_text'].center(50, '-'))    
#     for row in hints:
#         if row['exercise_id'] == 1:
#             time.sleep(1)
#             print(row['hint_text'])


    