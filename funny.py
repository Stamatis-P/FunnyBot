import asyncio

import hikari
import hikari.events.reaction_events
import lightbulb
from time import sleep
from tabulate import tabulate

table = {"Stamatis" : 1}
headers = ["Name", "Score"]
whitelist = [254832150715564033, 142104644556947457, 203741575824670720, 138504390964150273] # John, Stas, Tristan, Aron

print(tabulate(table.items(), headers=headers))


bot = lightbulb.BotApp(token="OTY2ODI3MjgxMjk1MjI4OTg4.YmHaEg.KVLrdtEOxzKDt0pkkcWIQrivzvw",
                       default_enabled_guilds=(966828214745972787, 258769394606407681), #test server, Bepis Bros
                       prefix=("+", "-"),
                       help_class=None)


@bot.command
@lightbulb.option("id", "id to add/remove to/from whitelist", type=int)
@lightbulb.command("whitelist", "Add/remove a user to/from the whitelist", aliases=["wh"])
@lightbulb.implements(lightbulb.PrefixCommand)
async def add_to_whitelist(ctx):
    if ctx.author.id == 142104644556947457:
        if ctx.options.id in whitelist:
            print("it's in there")
            if  ctx.prefix == "-":
                whitelist.remove(ctx.options.id)
                await ctx.respond("Theyre gone.")
        else:
            print("it's NOT in there")
            if ctx.prefix == "+":
                whitelist.append(ctx.options.id)
                await ctx.respond("Added.")
    elif ctx.author.id in whitelist:
        await ctx.respond("Did you make the bot? Nah.")
    else:
        await ctx.respond("Yeah ok buddy.")


@bot.command
@lightbulb.command("white", "return whitelist")
@lightbulb.implements(lightbulb.PrefixCommand)
async def return_whitelist(ctx):
    await ctx.respond(whitelist)

@bot.command
@lightbulb.option("target", "User to change funny rating", hikari.User)
@lightbulb.option("number", "how much to change funny rating by", type=int)
@lightbulb.command("funny", "Alter a users funny rating")
@lightbulb.implements(lightbulb.PrefixCommand)
async def change_funny(ctx):
    username = ctx.options.target.username  # username of target from the options

    if ctx.author == ctx.options.target:    # check the author of the message is not the target
        await ctx.respond("Bruh.")

    if ctx.author.id not in whitelist:  #check the author is in the whitelist
        if ctx.author.id == 201135827059867658:
            await ctx.respond("Nah, you fell off.")
            return
        await ctx.respond("Sorry, you're not funny.")
        return

    if username not in table:   # add target to table if they are not yet
        table[username] = 0

    await ctx.event.message.add_reaction("👍")   #react to message with :thumbsup:

    def check(reaction):    #checks that the message reacted to is correct and user is not reacting their own message
        return reaction.message_id == ctx.event.message_id and reaction.user_id != 966827281295228988 and reaction.user_id != ctx.author.id

    try:
        for i in range(2):
            reaction = await bot.wait_for(hikari.events.reaction_events.ReactionEvent, predicate=check, timeout=30) #wait for reaction on message
        if ctx.prefix == "+":
            table[username] = table[username] + ctx.options.number
            await ctx.respond(f"+{ctx.options.number} funny to {username}")
        else:
            table[username] = table[username] - ctx.options.number
            await ctx.respond(f"-{ctx.options.number} funny to {username}")
    except asyncio.TimeoutError:
        await ctx.respond("Hm, guess no one important agrees with you.")

    print(table)


@bot.command
@lightbulb.command("score", "print funny leaderboard")
@lightbulb.implements(lightbulb.PrefixCommand)
async def print_leaderboard(ctx):
    sorted_table = dict(sorted(table.items(), key=lambda item: item[1], reverse=True))
    await ctx.respond(f"``` \n {tabulate(sorted_table.items(), headers=headers)} \n ```")


HELP_MESSAGE = """
`+funny [int] [user]` \n +[int]  funny to pinged user \n
`-funny [int] [user]` \n -[int]  funny to pinged user \n
`+score` \n returns leaderboard
"""

@bot.command
@lightbulb.command("help", "Gets help for bot commands")
@lightbulb.implements(lightbulb.PrefixCommand)
async def help(ctx: lightbulb.Context) -> None:
    embed = hikari.Embed(title="Help Command", colour=0x2495bd)
    embed.add_field("Available Commands", HELP_MESSAGE)
    await ctx.respond(embed)

bot.run()