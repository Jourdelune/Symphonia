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
            "CREATE TABLE IF NOT EXISTS music_guild(guild_id BIGINT, rgb VARCHAR(255), channel_id BIGINT, comportement_custom VARCHAR(255))") 
        conn.commit()
        conn.close()