from sqlalchemy import create_engine


class DBHelper(object):

    def __init__(self):
        engine = create_engine("mysql+pymysql://tevec:ew3wrnaKRy@6D3fyGGtvPGL6tr@172.26.3.122:3306/microservices")
        self.conn = engine.connect()

    # def query(self, query, params):
    #     return self.conn.execute(query, params)

    def __del__(self):
        self.conn.close()
