from quart import Quart, redirect, url_for, render_template, g, request
from quart_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
from discord.ext.ipc import Client
from utils.utils import *
import mysql.connector
import ast

app = Quart(__name__)
web_ipc = Client(host="127.0.0.1", secret_key="secret_key")

app.secret_key = b"random bytes representing quart secret key"

app.config["DISCORD_CLIENT_ID"] = 805082505320333383   
app.config["DISCORD_CLIENT_SECRET"] = "iQrq77S2qOakW4BR7XS7G4qKnKQ0TuDS"              
app.config["DISCORD_REDIRECT_URI"] = "http://songs-bot.tk/callback"            
app.config["DISCORD_BOT_TOKEN"] = "ODA1MDgyNTA1MzIwMzMzMzgz.YBVtgg.ie3BSi7q6z2SmEKSymLuA4mNj4Y"    

discord = DiscordOAuth2Session(app)

@app.route('/me/', methods=['POST'])
@requires_authorization
async def create_me():
    form = await request.form
    user = await discord.fetch_user()
    if user.id ==  int(form['user']):
        return redirect(url_for(".guild", guild_id=form['guild']))
    else:
        return redirect(url_for(".me"))
    
@app.route('/guild/', methods=['POST'])
@requires_authorization
async def create_guild():
    value=None
    form = await request.form

    user = await discord.fetch_user()
    try:
        write_in_database(table_name="config", data_in_name="guild_id", data_in=form['guild'],
                            data_for_write_name="prefix", data_for_write=form['prefix'])
    except:
        pass

  
    try:
        if form["head"] is not None:
            write_in_database(table_name="music_guild", data_in_name="guild_id", data_in=form['guild'],
                        data_for_write_name="rgb", data_for_write=form["head"])
    except:
        pass
    try:
        if form['channel'] is not None:
            if form['channel'] != "False":
                write_in_database(table_name="music_guild", data_in_name="guild_id", data_in=form['guild'],
                                    data_for_write_name="channel_id", data_for_write=form['channel'])
            else:
                conn = mysql.connector.connect(host=database_host(), user=database_user(),
                                       password=database_password(),
                                       database=database_name())

                cursor = conn.cursor()
                cursor.execute(f"""SELECT channel_id FROM music_guild WHERE guild_id={form['guild']}""")
                value = cursor.fetchone()
              
                if value is not None:
                    
                    write_in_database(table_name="music_guild", data_in_name="guild_id", data_in=form['guild'],
                                    data_for_write_name="channel_id", data_for_write="1")
                conn.close()
                
    except:
       pass
    try:
        if form['edit_comport'] is not None:
            conn = mysql.connector.connect(host=database_host(), user=database_user(),
                                       password=database_password(),
                                       database=database_name())

            cursor = conn.cursor()
            cursor.execute(f"""SELECT comportement_custom FROM music_guild WHERE guild_id={form['guild']}""")
            value = cursor.fetchone()
            if value is not None:
                value=value[0]
                if value == "True":
                    write_in_database(table_name="music_guild", data_in_name="guild_id", data_in=form['guild'],
                                data_for_write_name="comportement_custom", data_for_write="False")
                  
                elif value == "False":
                    write_in_database(table_name="music_guild", data_in_name="guild_id", data_in=form['guild'],
                                data_for_write_name="comportement_custom", data_for_write="True")
                else:
                    write_in_database(table_name="music_guild", data_in_name="guild_id", data_in=form['guild'],
                                data_for_write_name="comportement_custom", data_for_write="True")
                    value=True
                  
            else:
                write_in_database(table_name="music_guild", data_in_name="guild_id", data_in=form['guild'],
                                data_for_write_name="comportement_custom", data_for_write="True")
                value=True
            
            conn.close()
    except:
        pass

    return redirect(url_for(".guild", guild_id=form['guild']))
    
    
@app.route("/login/")
async def login():
    return await discord.create_session(scope=["identify", "guilds"])



@app.route("/callback/")
async def callback():
    await discord.callback()
    return redirect(url_for(".me"))

@app.route("/support")
async def support():
    return redirect("https://discord.gg/qaQtvNmdm5")

@app.route("/invite")
async def invite():
    return redirect("https://discord.com/oauth2/authorize?client_id=805082505320333383&scope=bot&permissions=70634560")


@app.errorhandler(Unauthorized)
async def redirect_unauthorized(e):
    return redirect(url_for("login"))

@app.route("/")
async def index():
     return await render_template('index.html')
    
@app.route("/commands")
async def commands():
     return await render_template('commands.html')
                
    
@app.route("/guild/")
@requires_authorization
async def guild():
    user = await discord.fetch_user()
    guilds = await discord.fetch_guilds()
    admin=False
    for i in guilds:
        if i.id == int(request.args['guild_id']):
            if i.permissions.value == 2147483647:
                admin=True

    if admin:
        conn = mysql.connector.connect(host=database_host(), user=database_user(),
                                       password=database_password(),
                                       database=database_name())
        cursor = conn.cursor()
        cursor.execute(f"""SELECT prefix FROM config WHERE  guild_id={request.args['guild_id']}""")
        prefix=cursor.fetchone()
        if prefix is not None:
            prefix = prefix[0]
        else:
            write_in_database(table_name="config", data_in_name="guild_id", data_in=request.args['guild_id'],
                                    data_for_write_name="prefix", data_for_write="s!")
            prefix="s!"  
    
     
        await web_ipc.request("get_all_channel", guild_id=request.args['guild_id'])
        with open('list.json') as f:
          guild_list = json.load(f)
     

        
        cursor.execute(f"""SELECT comportement_custom FROM music_guild WHERE guild_id={request.args['guild_id']}""")
        value = cursor.fetchone()
        conn.close()
        
        conn = mysql.connector.connect(host=database_host(), user=database_user(),
                                       password=database_password(),
                                       database=database_name())

        cursor = conn.cursor()
        cursor.execute(f"""SELECT channel_id FROM music_guild WHERE guild_id={request.args['guild_id']}""")
        id_channel = cursor.fetchone()
        cursor.execute(f"""SELECT rgb FROM music_guild WHERE guild_id={request.args['guild_id']}""")
        try:
            rgb_value = cursor.fetchone()
            
            if rgb_value[0] is None:
                rgb_value="#D45AFF"
            else:
                rgb_value=rgb_value[0]
        except:
            rgb_value="#D45AFF"
    
        try:
            if int(id_channel[0]) == 1:
                id_channel_fin=None
            else:
                guild_channel = await web_ipc.request("get_channel", channel_id=id_channel[0])
                id_channel_fin=[id_channel[0], guild_channel.replace('"',"")]
            
        except:
            id_channel_fin=None
        try:
            if value is not None:
                value=value[0]
                if value == "True" or False:              
                    if id_channel_fin is not None:
                        return await render_template('guild.html', user=user, rgb_value=rgb_value, guild_id=request.args['guild_id'], prefix=prefix, guild_list=guild_list, comport=value, id_channel_fin=id_channel_fin)
                    else:
                        return await render_template('guild.html', user=user, rgb_value=rgb_value, guild_id=request.args['guild_id'], prefix=prefix, guild_list=guild_list, comport=value)
                else:
                    if id_channel_fin is not None:
                        return await render_template('guild.html', user=user, rgb_value=rgb_value, guild_id=request.args['guild_id'], prefix=prefix, guild_list=guild_list, id_channel_fin=id_channel_fin)
                    else:
                        return await render_template('guild.html', user=user, rgb_value=rgb_value, guild_id=request.args['guild_id'], prefix=prefix, guild_list=guild_list, id_channel_fin=id_channel_fin)
            else:
                if id_channel_fin is not None:
                    return await render_template('guild.html', user=user, rgb_value=rgb_value, guild_id=request.args['guild_id'], prefix=prefix, guild_list=guild_list, id_channel_fin=id_channel_fin, comport=value)
                else:
                    write_in_database(table_name="music_guild", data_in_name="guild_id", data_in=request.args['guild_id'],
                                data_for_write_name="comportement_custom", data_for_write="False")
                    return await render_template('guild.html', user=user, rgb_value=rgb_value, guild_id=request.args['guild_id'], prefix=prefix, guild_list=guild_list, id_channel_fin=id_channel_fin, comport=value)
        except:
            if id_channel_fin is not None:
                return await render_template('guild.html', user=user, rgb_value=rgb_value, guild_id=request.args['guild_id'], prefix=prefix, guild_list=guild_list, id_channel_fin=id_channel_fin)
            else:
                return await render_template('guild.html', user=user, rgb_value=rgb_value, guild_id=request.args['guild_id'], prefix=prefix, guild_list=guild_list, id_channel_fin=id_channel_fin)
                
            
        
    else:
        return redirect(url_for(".me"))
        

@app.route("/me/")
@requires_authorization
async def me():
    common_guild = []
    no_common_guild = []
    guilds = await discord.fetch_guilds()
    guild_list = await web_ipc.request("get_guild_list")
    for i in guilds:     
        if i.permissions.value == 2147483647:   
            if (i.id in guild_list):
                common_guild.append(i)
                
            else:
                no_common_guild.append(i)

    return await render_template('me.html', user=user, guilds=common_guild, no_guild=no_common_guild)


if __name__ == "__main__":
    app.run(host="185.157.247.229", port=8081)