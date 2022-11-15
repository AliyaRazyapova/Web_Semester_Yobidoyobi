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

    def select(self, query):
        self.cur.execute(query)
        data = self.prepare_data(self.cur.fetchall())

        return data

    def insert(self, query):
        self.cur.execute(query)
        self.con.commit()

    def get_category_page(self, table, category, parametr):
        self.cur.execute(f"SELECT * FROM {table} WHERE {parametr} = '{category}';")
        data = self.prepare_data(self.cur.fetchall())
        if len(data) == 1:
            data = data[0]
        return data

    def prepare_data(self, data):
        products = []
        if len(data):
            column_names = [desc[0] for desc in self.cur.description]
            for row in data:
                products += [{c_name: row[key] for key, c_name in enumerate(column_names)}]

        return products
