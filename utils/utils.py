import mysql.connector
import DiscordUtils
import json
import sys
import time
import discord
import datetime
import asyncio
from dateutil.relativedelta import relativedelta
import webcolors

requet_member = {}
list_index=[]
def requet_member():
    requet_member[id]=index
    
def convert_duration(duration):
    duration=relativedelta(seconds=round(float(duration)))
    if duration.hours != 0:
        duration=str(duration.hours)+":"+str(duration.minutes)+":"+str(duration.seconds)
    else:
        duration=str(duration.minutes)+":"+str(duration.seconds)
        
    return duration

def check_emoji():
    return "<:good:748526753634451507>"


def error_emoji():
    return "<:erreur:748526753483325530>"


def database_name():
    return "Bot"


def database_user():
    return "Jourdelune"


def database_host():
    return "localhost"


def database_password():
    return "123Nousironsaubois*"

def check_mode_pause(ctx):
    if (ctx.guild.id in pause_mode):
        return True
    else:
        return False
   
def get_channel(guild_id, channel_id):
    conn = mysql.connector.connect(host=database_host(), user=database_user(),
                                password=database_password(),
                                database=database_name())

    cursor = conn.cursor()
    cursor.execute(f"""SELECT channel_id FROM music_guild WHERE guild_id={guild_id}""")
    value = cursor.fetchone()
    try:
        if str(value[0])=="1":
            return True
        else:
            if int(value[0])==channel_id:
                return True
            else:
                return channel_id
    except:
        print("error")
            
    
pause_mode={}
final_pause={}
def mode_pause(ctx, mode=None):
    if mode=="on":
        if not (ctx.guild.id in pause_mode):
            pause_mode[ctx.guild.id]=time.time()
    if mode=="off":
        final_pause[ctx.guild.id]=time.time()-pause_mode[ctx.guild.id]
        del pause_mode[ctx.guild.id]
        
    if (ctx.guild.id in pause_mode):
        return time.time()-pause_mode[ctx.guild.id]
    
    if (ctx.guild.id in final_pause):
        return final_pause[ctx.guild.id]
    
    else:
        return 0
        
final_duration={}
def playing_duration(ctx, duration):
    try:
        final=final_duration[ctx.guild.id]-time.time()
        if final < 0:
            del final_duration[ctx.guild.id]
         
        final=final_duration[ctx.guild.id]-time.time()+mode_pause(ctx)
        return final
    except:
        final_duration[ctx.guild.id] = time.time()+duration
        final=final_duration[ctx.guild.id]-time.time()+mode_pause(ctx)
       
        return final
            
        
    
def reset_duration(ctx):
    try:
        del final_duration[ctx.guild.id]
       
    except:
        pass
   
     
def embed_color(guild_id):
    conn = mysql.connector.connect(host=database_host(), user=database_user(),
                                password=database_password(),
                                database=database_name())

    cursor = conn.cursor()
    cursor.execute(f"""SELECT rgb FROM music_guild WHERE guild_id={guild_id}""")
    value = cursor.fetchone()
    try:
        rgb=webcolors.hex_to_rgb(value[0])     
        return discord.Colour.from_rgb(rgb.red, rgb.green, rgb.blue)
    except:
        return discord.Colour(0xD45AFF)



def read_database_where(table_name, data_in, data_where, data_where_in):
    try:

        conn = mysql.connector.connect(host=database_host(), user=database_user(),
                                       password=database_password(),
                                       database=database_name())

        cursor = conn.cursor()
        cursor.execute(f"""SELECT {data_in} FROM {table_name} WHERE {data_where}={data_where_in}""")
        value = cursor.fetchone()[0]
        conn.close()
        return value

    except Exception:
        return None


def read_database(table_name, data_in, *, data=None):
    try:

        conn = mysql.connector.connect(host=database_host(), user=database_user(),
                                       password=database_password(),
                                       database=database_name())

        cursor = conn.cursor()
        cursor.execute(f"""SELECT {data_in} FROM {table_name} {data}""")
        value = cursor.fetchone()[0]
        conn.close()
        return value

    except Exception:
        return None


def drop_column(table, column, data):
    conn = mysql.connector.connect(host=database_host(), user=database_user(),
                                   password=database_password(),
                                   database=database_name())
    cursor = conn.cursor()
    cursor.execute(f"ALTER TABLE {table} DROP '{column}'='{data}'")


def write_in_database(table_name: str, data_for_write_name: str, data_in_name: str, data_in: str, data_for_write: str):
    conn = mysql.connector.connect(host=database_host(), user=database_user(),
                                   password=database_password(),
                                   database=database_name())
    cursor = conn.cursor()
    cursor.execute(f"""SELECT {data_for_write_name} FROM {table_name} WHERE {data_in_name}={data_in}""")
    if cursor.fetchone() is None:
        cursor.execute(
            f"""INSERT INTO {table_name} ({data_for_write_name}, {data_in_name}) VALUES('{data_for_write}', '{data_in}')""")

    else:
        cursor.execute(
            f"UPDATE {table_name} SET {data_for_write_name}='{data_for_write}' WHERE {data_in_name}='{data_in}'")
    conn.commit()
    conn.close()


def write_null_into_database(table_name: str, data_for_write_name: str, data_in_name: str, data_in,
                             data_for_write):
    conn = mysql.connector.connect(host=database_host(), user=database_user(),
                                   password=database_password(),
                                   database=database_name())
    cursor = conn.cursor()
    cursor.execute(f"""SELECT {data_for_write_name} FROM {table_name} WHERE {data_in_name}={data_in}""")
    if cursor.fetchone() is None:
        cursor.execute(
            f"""INSERT INTO {table_name} ({data_for_write_name}) VALUES({data_for_write})""")

    else:
        cursor.execute(
            f"UPDATE {table_name} SET {data_for_write_name}=NULL WHERE {data_in_name}='{data_in}'")
    conn.commit()
    conn.close()


def write_database_for_one_value(table_name: str, data_in: str, data: str):
    try:
        conn = mysql.connector.connect(host=database_host(), user=database_user(),
                                       password=database_password(),
                                       database=database_name())
        cursor = conn.cursor(buffered=True)
        cursor.execute(f"""SELECT {data_in} FROM {table_name}""")

        if cursor.fetchone() is None:

            cursor.execute(
                f"""INSERT INTO {table_name}({data_in}) VALUES('{data}')""")
            print("write")
        else:
            cursor.execute(
                f"UPDATE {table_name} SET {data_in}='{data}'")

        conn.commit()
        conn.close()

    except Exception as e:
        print(e)


def load_file(file: str, value):
    with open(file, 'r', encoding='utf-8') as f:
        info1 = json.load(f)
    return info1[str(value)]


def logger(type: str, action: str, author: str = None, guild: str = None):
    log = f"""[{type}] {action} at "{datetime.datetime.now()}" {'' if author and guild is None else f'by "{author}" on "{guild}"'}"""
    print(log)

    with open('./logs/logs.json', 'a+') as f:
        f.write("\n" + log)

