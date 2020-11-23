import yfinance as yf
import discord
from datetime import datetime
from discord.ext import commands
import math

# this is from SO
millnames = ['', ' Thousand', ' Million', ' Billion', ' Trillion']
def millify(n):
    n = float(n)
    millidx = max(0, min(len(millnames)-1,
                        int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))
    return '{:.0f}{}'.format(n / 10 ** (3 * millidx), millnames[millidx])


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
    try:
        ticker = yf.Ticker(query)
        currency = " " + ticker.info["currency"]
        embed = discord.Embed(
            title=ticker.info["shortName"],
            color=discord.Color.green()
        )
        embed.set_thumbnail(url=ticker.info["logo_url"])
        embed.add_field(name="Current price", value="{:.2f}".format(ticker.info["ask"]) + currency, inline=False)
    except:
        embed = discord.Embed(
            title="Ticker not found",
            color=discord.Color.red()
        )
        embed.add_field(name="Invalid ticker.", value=" Please try again.", inline=False)
        print("[ error ] "+query+" not found")
    await ctx.send(embed=embed)


@client.command(name="indepth")
async def indepth(ctx, *, query):
    try:
        ticker = yf.Ticker(query)
        currency = " " + ticker.info["currency"]
        embed = discord.Embed(
            title=ticker.info["shortName"],
            color=discord.Color.green()
        )
        embed.set_thumbnail(url=ticker.info["logo_url"])
        embed.add_field(name="Current price", value="{:.2f}".format(ticker.info["ask"]) + currency, inline=False)
        embed.add_field(name="Open", value="{:.2f}".format(ticker.info["open"]) + currency, inline=True)
        embed.add_field(name="High", value="{:.2f}".format(ticker.info["dayHigh"]) + currency, inline=True)
        embed.add_field(name="Low", value="{:.2f}".format(ticker.info["dayLow"]) + currency, inline=True)
        embed.add_field(name="Previous close", value="{:.2f}".format(ticker.info["previousClose"]) + currency, inline=False)
        embed.add_field(name="Market cap", value=millify(ticker.info["marketCap"]), inline=False)
    except:
        embed = discord.Embed(
            title="Ticker not found",
            color=discord.Color.red()
        )
        embed.add_field(name="Invalid ticker.", value=" Please try again.", inline=False)
        print("[ error ] "+query+" not found")
    await ctx.send(embed=embed)


@client.command(name="info")
async def info(ctx, *, query):
    try:
        ticker = yf.Ticker(query)
        currency = " " + ticker.info["currency"]
        embed = discord.Embed(
            title=ticker.info["shortName"],
            color=discord.Color.green()
        )
        embed.set_thumbnail(url=ticker.info["logo_url"])
        embed.add_field(name="Long name", value=ticker.info["longName"], inline=False)
        embed.add_field(name="Industry", value=ticker.info["industry"], inline=False)
        embed.add_field(name="Address", value=ticker.info["address1"], inline=False)
        embed.add_field(name="City", value=ticker.info["city"], inline=True)
        embed.add_field(name="State", value=ticker.info["state"], inline=True)
        embed.add_field(name="Country", value=ticker.info["country"], inline=True)
        embed.add_field(name="Website", value=ticker.info["website"], inline=False)
        embed.add_field(name="Phone", value=ticker.info["phone"], inline=True)
        #embed.add_field(name="Summary", value=ticker.info["longBusinessSummary"], inline=False)
    except:
        embed = discord.Embed(
            title="Ticker not found",
            color=discord.Color.red()
        )
        embed.add_field(name="Invalid ticker.", value=" Please try again.", inline=False)
        print("[ error ] "+query+" not found")
    await ctx.send(embed=embed)


# branje ključa za bot iz zasebne datoteke, ker se takšne stvari ne objavljajo na internetu
# reading the bot key from a private file because things like that shouldn't be posted on the internet
dat = open("key.txt", "r")
key = dat.read().strip()
client.run(key)