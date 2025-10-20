"""

"""
import discord
# from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
load_dotenv()
# import supabase
import time
# Import nonce manager
import nonce.nonce_manager as nonce_manager
#client = commands.Bot(command_prefix='!', intents=discord.Intents.all())
import secrets

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents = discord.Intents.default())
        self.synced = False
        self.tree = app_commands.CommandTree(self)  # attach the tree to this client
    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            # guild = discord.Object(id=GUILD_ID)
            await self.tree.sync()  # sync all commands
            self.synced = True
        print(f"We have logged in as {self.user}.")


import os, jsonDatabase, pathlib
DB_CODE_TO_USER = os.path.join(pathlib.Path(__file__).parent,"google_auth", "code_to_user.json")
databaseCodeToUser = jsonDatabase.createDatabase(DB_CODE_TO_USER)
databaseCodeToUser(jsonDatabase.write, {})

DB_USER = os.path.join(pathlib.Path(__file__).parent, "users.json")
databaseUsers = jsonDatabase.createDatabase(DB_USER)
# databaseUsers(jsonDatabase.write, {})

client = aclient()
tree = client.tree
#@client.event
async def on_ready():
    print("bot is ready")

# @tree.command
# async def on_message(message):
#     if message.author == client.user:
#         return

#     if message.content.startswith('$hello'):
#         await message.channel.send('Hello!')

@tree.command(name="open_website", description="open the website")
async def self(interaction : discord.Interaction):
    await interaction.response.send_message(f'Here is the [website](legitminh.github.io)', ephemeral=True)

@tree.command(name="pang", description="reply pong")
async def self(interaction : discord.Interaction):
    await interaction.response.send_message(f'pong', ephemeral=True)

@tree.command(name="do_addition", description="add(a,b)")
async def self(interaction : discord.Interaction, number1 : int, number2 : int):
    await interaction.response.send_message(f'{number1 + number2}', ephemeral=True)


@tree.command(name="sign_in_bonus", description="Round two of signing in")
async def self(interaction: discord.Interaction, code : str):
    dict = databaseCodeToUser(jsonDatabase.read)[code]
    messagerId = interaction.user.id
    verifyingId = dict["id"]
    googleId = dict["googleId"]
    if messagerId == verifyingId:
        databaseUsers(jsonDatabase.set, verifyingId, {"signedIn": True, "googleId": googleId})
        await interaction.response.send_message(
            f"You are signed in!", ephemeral=True
        )
    else:
        await interaction.response.send_message(
            f"Wrong code", ephemeral=True
        )

# New sign_in command
@tree.command(name="sign_in", description="Generate a sign-in link")
async def self(interaction: discord.Interaction):
    nonce = nonce_manager.generate_nonce_linked(interaction.user.id, time.time())
    # You should replace the URL below with your actual sign-in endpoint
    sign_in_url = f"localhost:5000/login?nonce={nonce}"
    await interaction.response.send_message(
        f"Click here to sign in: {sign_in_url}", ephemeral=True
    )


















#last line
client.run(os.getenv("DISCORD_TOKEN"))