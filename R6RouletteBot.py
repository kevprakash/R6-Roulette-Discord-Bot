import asyncio
import os
from dotenv import load_dotenv

import discord
from discord import Option, Member
from DiscordUtil import PageView

from Siege import opNames, getTeam

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

intents = discord.Intents.default()
intents.messages = True
intents.reactions = True
client = discord.Client(intents=intents)

bot = discord.Bot()

operatorNames = opNames


@bot.command(description="Test")
async def roulette(ctx, side: Option(str, choices=["Attack", "Defense"], required=True), rounds_per_half: Option(int, required=True),
                      player1: Option(Member, required=True), player2: Option(Member, required=False),
                      player3: Option(Member, required=False), player4: Option(Member, required=False),
                      player5: Option(Member, required=False),
                      ban1: Option(str, required=False), ban2: Option(str, required=False),
                      ban3: Option(str, required=False), ban4: Option(str, required=False),
                      silly: Option(bool, required=False)):

    print("Received command")

    ctx.timeout = None

    players = [player1.display_name]
    for p in [player2, player3, player4, player5]:
        if p is not None:
            players.append(p.display_name)

    bans = []
    for b in [ban1, ban2, ban3, ban4]:
        if b is not None:
            bans.append(str(b))

    pages = []

    for r in range(rounds_per_half * 2 + 4):
        if r < rounds_per_half:
            t = "Round " + str(r + 1)
            s = side == "Attack"
        elif r < rounds_per_half * 2:
            t = "Round " + str(r + 1)
            s = side == "Defense"
        else:
            t = "OT " + ("Attack " if (r - rounds_per_half * 2 < 2) else "Defense ") + str((r % 2) + 1)
            s = r % 2 == 0

        silly = silly if silly is not None else False
        loadouts = getTeam(s, players, bans, seriousMode=not silly)

        loadoutStrings = []

        for lo in loadouts:
            op, role, primary, secondary, gadget = lo
            response = op + (" [" + role + "]" if len(role) > 0 else "") + "\n"
            response += "Primary: " + primary + "\n"
            response += "Secondary: " + secondary + "\n"
            response += "Gadget: " + gadget
            loadoutStrings.append(response)

        embedVar = discord.Embed(title=t, color=0x00ff00)
        for p_i in range(len(players)):
            player = players[p_i]
            loadoutString = loadoutStrings[p_i]
            embedVar.add_field(name=player, value=loadoutString, inline=False)

        pages.append(embedVar)

    await ctx.respond(embed=pages[0])
    message = await ctx.interaction.original_response()

    view = PageView(pages, message)
    await message.edit(view=view)


bot.run(TOKEN)