import yfinance as yf
import discord
from datetime import datetime
from discord.ext import commands
import math

# this is from SO
millnames = ['', ' Thousand', ' Million', ' Billion', ' Trillion']
def millify(n):
    if n == "not provided":
        return n
    n = float(n)
    millidx = max(0, min(len(millnames)-1,
                        int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))
    return '{:.0f}{}'.format(n / 10 ** (3 * millidx), millnames[millidx])


def getValue(ticker, key, decimals=0):
    if key in ticker.info and ticker.info[key] is not None:
        return "{:.{decimals}f}".format(ticker.info[key], decimals=decimals)
    else:
        return "not provided"

def getText(ticker, key):
    if key in ticker.info and ticker.info[key] is not None:
        return ticker.info[key]
    else:
        return "not provided"


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
        if ticker.info["ask"] is not None and ticker.info["ask"] > 0:
            embed.add_field(name="Current price", value=getValue(ticker, "ask", 2) + currency, inline=False)
        else:
            embed.add_field(name="Market currently closed", value="last minute high will be displayed", inline=False)
            embed.add_field(name="Last minute high", value="{:.2f}".format(ticker.history(period="1d", interval="1m")["High"][-1]) + currency, inline=False)
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
        if ticker.info["ask"] is not None and ticker.info["ask"] > 0:
            embed.add_field(name="Current price", value="{:.2f}".format(ticker.info["ask"]) + currency, inline=False)
        elif "regularMarketPrice" in ticker.info and ticker.info["regularMarketPrice"] is not None:
            embed.add_field(name="Current price", value="{:.2f}".format(ticker.info["regularMarketPrice"]) + currency, inline=False)
        else:
            embed.add_field(name="Market currently closed", value="last minute high will be displayed", inline=False)
            embed.add_field(name="Last minute high", value="{:.2f}".format(ticker.history(period="1d", interval="1m")["High"][-1]) + currency, inline=False)
        embed.add_field(name="Open", value=getValue(ticker, "open", 2) + currency, inline=True)
        embed.add_field(name="High", value=getValue(ticker, "dayHigh", 2) + currency, inline=True)
        embed.add_field(name="Low", value=getValue(ticker, "dayLow", 2) + currency, inline=True)
        embed.add_field(name="52 week High", value=getValue(ticker, "fiftyTwoWeekHigh", 2) + currency, inline=True)
        embed.add_field(name="52 week Low", value=getValue(ticker, "fiftyTwoWeekLow", 2) + currency, inline=True)
        embed.add_field(name="Previous close", value=getValue(ticker, "previousClose", 2) + currency, inline=False)
        embed.add_field(name="Market cap", value=millify(getValue(ticker, "marketCap")), inline=False)
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
        embed.add_field(name="Long name", value=getText(ticker, "longName"), inline=False)
        embed.add_field(name="Industry", value=getText(ticker, "industry"), inline=False)
        if "address2" in ticker.info and ticker.info["address2"] is not None:
            embed.add_field(name="Address", value=getText(ticker, "address1")+" "+getText(ticker, "address2"), inline=False)
        else:
            embed.add_field(name="Address", value=getText(ticker, "address1"), inline=False)
        embed.add_field(name="City", value=getText(ticker, "city"), inline=True)
        embed.add_field(name="State", value=getText(ticker, "state"), inline=True)
        embed.add_field(name="Country", value=getText(ticker, "country"), inline=True)
        embed.add_field(name="Website", value=getText(ticker, "website"), inline=False)
        embed.add_field(name="Phone", value=getText(ticker, "phone"), inline=True)
    except:
        embed = discord.Embed(
            title="Ticker not found",
            color=discord.Color.red()
        )
        embed.add_field(name="Invalid ticker.", value=" Please try again.", inline=False)
        print("[ error ] "+query+" not found")
    await ctx.send(embed=embed)


# sends an embed with informations about the bot and its commands
client.remove_command("help")
@client.command(name="help")
async def help(ctx):
    embed = discord.Embed(
        title="Help",
        description="A simple and free to use discord bot for stocks.",
        color=discord.Color.green()
    )
    commands_ = """
    `$price <query> or $p <query>` sends an embed with the current price for the symbol.
    `$indepth <query>` sends an embed with current price, open, dayHigh, dayLow, prevClose and marketCap for the symbol.
    `$info <query>` sends an embed with some basic informations about the company with the symbol queried.
    `$help` sends an embed with the help message.
    `$invite` sends an invite link for itself to be added to other discord servers.
    """
    embed.set_thumbnail(url=client.user.avatar_url)
    embed.add_field(name="Commands", value=commands_, inline=False)
    embed.add_field(name="Add the bot to your server", value="https://bit.ly/39bxPcO\nBot is currently in {} servers".format(len(client.guilds)), inline=False)
    embed.add_field(name="Help", value="For more informations about the bot and the code add CaptainYEET#9943")
    await ctx.send(embed=embed)


# sends an embed with a shortened invite link for the bot
@client.command(name="invite")
async def invite(ctx):
    message = discord.Embed(
        title="Invite me to your discord server:",
        description="https://bit.ly/39bxPcO",
        color=discord.Color.green()
    )
    await ctx.send(embed=message)


# reading the bot key from a private file because things like that shouldn't be posted on the internet
# starting the client
dat = open("key.txt", "r")
key = dat.read().strip()
client.run(key)