import yfinance as yf
import discord
from datetime import datetime
from discord.ext import commands


### ZAGON BOTA
# tukaj se lahko spremeni predpona, za katero bot posluša
# here the prefix used to command the bot can be changed
client = commands.Bot(command_prefix="$")


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game("buy TSLA"))
    # za lažji nadzor nad botom, ker ob zagonu potrebuje nekaj časa, da dobi ponudbo vseh ponudnikov
    # here for easier overview over the bot, as the initialization takes some time at the beginning
    print("[general] Bot is ready")


@client.command(name="price")
async def price(ctx, *, query):
    ticker = yf.Ticker(query)
    embed = discord.Embed(
        title=ticker.info["shortName"],
        color=discord.Color.green()
    )
    embed.set_thumbnail(url=ticker.info["logo_url"])
    embed.add_field(name="Trenutna cena", value=str(ticker.info["ask"])+"$", inline=False)
    await ctx.send(embed=embed)



# branje ključa za bot iz zasebne datoteke, ker se takšne stvari ne objavljajo na internetu
# reading the bot key from a private file because things like that shouldn't be posted on the internet
dat = open("key.txt", "r")
key = dat.read().strip()
client.run(key)