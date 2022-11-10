import psycopg2


class Database:
    def __init__(self):
        self.con = psycopg2.connect(
            dbname="yobi",
            user="postgres",
            password="123",
            host="localhost",
            port=5432
        )
        self.cur = self.con.cursor()

    # def select(self, query):
    #     self.cur.execute(query)
    #     data = self.prepare_data(self.cur.fetchall())
    #
    #     return data
    #
    # def insert(self, query):
    #     self.cur.execute(query)
    #     self.con.commit()
