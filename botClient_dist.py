# Python SuperTitan Bot Client
# Author: lauren brown
# Date: 2/14/19
# Built with Python 3.6

import asyncio
import aiohttp
import json
import signal
import sys
import os
import time
from discord import Game
from discord.ext.commands import Bot
import discord

# Bot Configuration
TOKEN = ""  # Get a token at discordapp.com/developers

CHANNEL = ""  # The Channel ID where the bot should report invasions

USER_ID = ""  # The user ID of where the bot should report to

BOT_PREFIX = ("?", "!")
description = '''Hello, I am SixthTitan's assistant: \n
I can provide information regarding titan's current software projects and novels regarding the Destiny Zero Origins book series. \n
I can also provide other useful information.'''

client = Bot(command_prefix=BOT_PREFIX, description=description)


def signal_handler(sig, frame):
    print('\n Quitting')
    client.close()  # Disconnect
    if client.is_closed:
        os.system('clear')
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)


# Available Bot Commands
@client.command(brief="Allows you to be notified when certain cogs are invading Toontown")
async def cogTracker(cogTrack):
    await client.wait_until_ready()
    while not client.is_closed:
        url = 'https://www.toontownrewritten.com/api/invasions'
        async with aiohttp.ClientSession() as session:  # Async HTTP request
            raw_response = await session.get(url)
            response = await raw_response.text()
            response = json.loads(response)

            invData = response['invasions']
            currentInv = []
            districtList = []
            progression = []

            for inv in response["invasions"]:
                cog = invData[inv]['type']
                progress = invData[inv]['progress']
                asOf = time.ctime(invData[inv]['asOf'])
                cog = cog.replace('\x03', '')  # Replace Panda3d's text seperater
                currentInv.append(cog)
                districtList.append(inv)
                progression.append(progress)

                invasionReport = (
                        "------- COG INVASION ------- \n" +
                        "District: " + inv + "\n"
                        "Type: " + cog + "\n"
                        "Progress: " + progress + "\n"
                        "Incident Reported: " + asOf
                )

                if cogTrack == cog:
                    await client.say("Alert:" + str(cog) + " in " + "District: " + inv + "\n")


@client.event
async def on_ready():
    await client.change_presence(game=Game(name="Toontown Rewritten"))
    # user = await client.get_user_info(USER_ID)
    # await client.send_message(user, "Logged on")


@client.command(brief="Gets current cog invasions in Toontown Rewritten")
async def invasions():
    url = 'https://www.toontownrewritten.com/api/invasions'
    async with aiohttp.ClientSession() as session:  # Async HTTP request
        raw_response = await session.get(url)
        response = await raw_response.text()
        response = json.loads(response)

        invData = response['invasions']
        currentInv = []
        districtList = []
        progression = []
        lastUpdated = time.ctime(response["lastUpdated"])

        for inv in response["invasions"]:
            print("\n")
            # print("COG INVASION: \n" + "District: " + inv)
            cog = invData[inv]['type']
            progress = invData[inv]['progress']
            asOf = time.ctime(invData[inv]['asOf'])
            cog = cog.replace('\x03', '')  # Replace Panda3d's text seperater
            currentInv.append(cog)
            districtList.append(inv)
            progression.append(progress)

            await client.say(
                "------- COG INVASION ------- \n" +
                "District: " + inv + "\n"
                "Type: " + cog + "\n"
                "Progress: " + progress + "\n"
                "Incident Reported: " + asOf
            )


@client.event
async def post_invasions():
    await client.wait_until_ready()
    while not client.is_closed:
        url = 'https://www.toontownrewritten.com/api/invasions'
        async with aiohttp.ClientSession() as session:  # Async HTTP request
            raw_response = await session.get(url)
            response = await raw_response.text()
            response = json.loads(response)

            invData = response['invasions']
            currentInv = []
            districtList = []
            progression = []
            lastUpdated = time.ctime(response["lastUpdated"])
            invasionreported = False

            for inv in response["invasions"]:
                cog = invData[inv]['type']
                progress = invData[inv]['progress']
                asOf = time.ctime(invData[inv]['asOf'])
                cog = cog.replace('\x03', '')  # Replace Panda3d's text seperater
                currentInv.append(cog)
                districtList.append(inv)
                progression.append(progress)

                invasionReport = (
                    "------- COG INVASION ------- \n" +
                    "District: " + inv + "\n"
                    "Type: " + cog + "\n"
                    "Progress: " + progress + "\n"
                    "Incident Reported: " + asOf
                )

                await client.send_message(discord.Object(id=CHANNEL), content=invasionReport, tts=True)
            await asyncio.sleep(930)


async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        # print("Current servers:")
        for server in client.servers:
            os.system('clear')

            print("******************************************************")
            print("* Toontown Rewritten Invasion Tracker,               *")
            print("* Version 1.0 Written by Sixth Titan                 *")
            print("* Invasions are reported every 15 minutes on the     *")
            print("* Discord Server through the Super Titan Bot Account *")
            print("******************************************************")

            print("Account Username: " + client.user.name + "\n"
                  + "Account Server: " + server.name + "\n")
            print('Press Ctrl+C to quit')

        await asyncio.sleep(600)


client.loop.create_task(list_servers())
client.loop.create_task(post_invasions())
client.run(TOKEN)
