from quart import Quart, redirect, url_for, render_template, g, request
from quart_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
from discord.ext.ipc import Client

app = Quart(__name__)
web_ipc = Client(host="localhost", port=8765, secret_key="secret_key")

app.secret_key = b"random bytes representing quart secret key"

app.config["DISCORD_CLIENT_ID"] = 805082505320333383   
app.config["DISCORD_CLIENT_SECRET"] = "iQrq77S2qOakW4BR7XS7G4qKnKQ0TuDS"              
app.config["DISCORD_REDIRECT_URI"] = "http://127.0.0.1:5000/callback"                
app.config["DISCORD_BOT_TOKEN"] = "ODA1MDgyNTA1MzIwMzMzMzgz.YBVtgg.ie3BSi7q6z2SmEKSymLuA4mNj4Y"    

discord = DiscordOAuth2Session(app)

@app.route('/me/', methods=['POST'])
@requires_authorization
async def create():
    form = await request.form
    user = await discord.fetch_user()
    if (str(user.id) in form['user']):
        return redirect(url_for(".guild", guild=form['guild']))
    else:
        return redirect(url_for(".me"))
    
    
    
@app.route("/login/")
async def login():
    return await discord.create_session(scope=["identify", "guilds"])



@app.route("/callback/")
async def callback():
    await discord.callback()
    return redirect(url_for(".me"))


@app.errorhandler(Unauthorized)
async def redirect_unauthorized(e):
    return redirect(url_for("login"))

@app.route("/guild")
@requires_authorization
async def guild():
    user = await discord.fetch_user()
    guild_list = await web_ipc.request("get_owner_with_id", guild_id=request.args['guild'])
    if guild_list == user.id:
        return await render_template('guild.html', user=user)
    else:
        return redirect(url_for(".me"))
        

@app.route("/me/")
@requires_authorization
async def me():
    user = await discord.fetch_user()
    common_guild = []
    no_common_guild = []
    guilds = await discord.fetch_guilds()
    guild_list = await web_ipc.request("get_guild_list")
    for i in guilds:
        if i.is_owner:   
            if (str(i.id) in guild_list):
                common_guild.append(i)
            else:
                no_common_guild.append(i)

    return await render_template('index.html', user=user, guilds=common_guild, no_guild=no_common_guild)


if __name__ == "__main__":
    app.run()