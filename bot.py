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


# here you can set the prefix
client = commands.Bot(command_prefix="$")


# log stuff, you can also set the presence here
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game("buy TSLA"))
    print("[general] Bot is ready")


# sends an embed with the current price
@client.command(name="price")
async def price(ctx, query):
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


# overloading the price command with the shorter version
@client.command(name="p")
async def p(ctx, query):
    await price(ctx, query)


# sends an embed with current price, open, dayHigh, dayLow, prevClose and marketCap
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


# sends an embed with some basic informations about the company
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
    except:
        embed = discord.Embed(
            title="Ticker not found",
            color=discord.Color.red()
        )
        embed.add_field(name="Invalid ticker.", value=" Please try again.", inline=False)
        print("[ error ] "+query+" not found")
    await ctx.send(embed=embed)


# reading the bot key from a private file because things like that shouldn't be posted on the internet
# starting the client
dat = open("key.txt", "r")
key = dat.read().strip()
client.run(key)