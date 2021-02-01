import mysql.connector
from utils.utils import *


class CreateTable(object):
    def __init__(self):
        self.create_table()

    @staticmethod
    def create_table():
        conn = mysql.connector.connect(host=database_host(), user=database_user(),
                                       password=database_password(),
                                       database=database_name())
        cursor = conn.cursor(buffered=True)

        cursor.execute(
            "CREATE TABLE IF NOT EXISTS Queue(server VARCHAR(255), liste VARCHAR(255))") 
        conn.commit()
        conn.close()
