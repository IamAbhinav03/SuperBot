import os
import discord
import text2emotion as te
from dotenv import load_dotenv
from discord.ext import commands


load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = commands.Bot(command_prefix="!", intents=intents)

@client.event
async def on_ready():
    print(f"{client.user.name} has connected to Discord!")

@client.event
async def on_member_join(member):
    await member.create_dm()
    # Send more customized msg explaning functionalities
    await member.dm_chaneel.send(
        f"Hi {member.name}, welcome to my Discord Server"
    )

# Test command to check if bot is online or not
@client.command(
    name="ping", 
    help="A test function to check if the bot is online or not"
    )
async def ping(ctx):
    await ctx.send("pong")

@client.command(
    name="recommend", 
    help="Recomends a music by analysing the emotion in the corresponding text"
    )
async def recommend(ctx, text: str):
    emotion = te.get_emotion(text)
    max = -1
    detected_emotion = None
    for k, v in emotion.items():
        if v > max:
            max = v
            detected_emotion = k
    match detected_emotion:
        case "Angry":
            pass
        case "Fear":
            pass
        case "Happy":
            pass
        case "Sad":
            pass
        case "Surprise":
            pass
        case default:
            pass
    pass


# Handle error by writting error msgs to an log file

client.run(TOKEN)