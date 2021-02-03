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
            "CREATE TABLE IF NOT EXISTS config(guild_id VARCHAR(255), prefix VARCHAR(255))") 
        conn.commit()
        
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS Playlist(user_id BIGINT, title VARCHAR(255), url VARCHAR(255), thumbnail VARCHAR(255), autor VARCHAR(255))") 
        conn.commit()
        conn.close()
