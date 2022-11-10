import os
import requests
import json
import random
import discord
import spotipy
import text2emotion as te
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
from discord.ext import commands

# accessing env keys from .env file
# load_dotenv()
# TOKEN = os.getenv("DISCORD_TOKEN")
# SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
# SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

# acessing env keys from heroku
print("Accessing env keys....")
try:
    TOKEN = os.environ["DISCORD_TOKEN"]
    SPOTIFY_CLIENT_ID = os.environ["SPOTIFY_CLIENT_ID"]
    SPOTIFY_CLIENT_SECRET = os.environ["SPOTIFY_CLIENT_SECRET"]
    print("env keys Accessed")
except Exception as e:
    print(Exception)

# Spotify Authentication
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))
print("Connected to spotify")

# values to help with category mapping for spotify api
category_id_mapping = {
    "workout": "0JQ5DAqbMKFAXlCG6QvYQ4",
    "Dance/Electronic": "0JQ5DAqbMKFHOzuVTgTizF",
    "sleep": "0JQ5DAqbMKFCuoRTxhYWow",
    "chill": "0JQ5DAqbMKFFzDl7qN9Apr",
    "wellness": "0JQ5DAqbMKFLb2EqgLtpjC",
    "mood": "0JQ5DAqbMKFzHmL4tf05da",
    "rock": "0JQ5DAqbMKFDXXwE9BDJAr",
    "country": "0JQ5DAqbMKFKLfwjuJMoNC",
    "pop": "0JQ5DAqbMKFEC4WFtoNRpw",
    "party": "0JQ5DAqbMKFA6SOHvT3gck",
    "romance": "0JQ5DAqbMKFAUsdyVjCQuL",
    "sports":
    "0JQ5DAqbMKFLhhtGqqgAsz",
    "car": "in_the_car",
    "soul": "0JQ5DAqbMKFIpEuaCnimBj",
    "metal": "0JQ5DAqbMKFDkd668ypn6O"
}

happy_generes = ["party", "pop", "happy", "chill", "romance", "Dance/Electronic", "country", "mood", "car"]
sad_generes = ["mood", "sad", "sleep", "wellness", "soul"]
anger_generes = ["workout", "wellness", "rock", "sports", "metal"]

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

def detect_emotion(text: str) -> str:
    """
    Finds the most probable emotion of the user from the given text
    Attributes:
        text (str): Text from which emotion is to be detected
    Returns:
        detected_emotion (str): Angry or Happy or Sad"""
    # print(text)
    emotion = te.get_emotion(text)  # geting emotions_dict from te
    # print(emotion)
    max = -1
    detected_emotion = None
    # Finding the emotion with highest probability from emotion
    for k, v in emotion.items():
        if v > max:
            max = v
            detected_emotion = k

    # Consider Fear as sad and Surprised as Happy
    if detected_emotion == "Fear":
        detected_emotion = "Sad"
    elif detected_emotion == "Suprised":
        detected_emotion = "Happy"

    return detected_emotion

def fetch_playlist(category_id: str):
    # category = "workout"
    # print(f"Category: {category}")
    # category_id = category_id_mapping.get(category)
    # print(f"Category_ID: {category_id}")
    response = spotify.category_playlists(category_id=category_id, country="US")
    playlists = response["playlists"]["items"] # list of playlists, each playlist is a dict
    playlist = random.choice(playlists)
    playlist_name = playlist["name"]
    playlist_uri = playlist["external_urls"]["spotify"]
    print(f"Playlist Name: {playlist_name}")
    print(f"Playlist_uri: {playlist_uri}")
    return playlist_name, playlist_uri


@client.command(
    name="recommend", 
    help="Recommends a music by analysing the emotion in the corresponding text. Please put the corresponding text in quotes"
    )
async def recommend(ctx, text: str):
    print("Detecting emotion.....")
    detected_emotion = detect_emotion(text)
    print(f"Emotion detected: {detected_emotion}")
    match detected_emotion:
        case "Angry":
            category = random.choice(anger_generes)
            category_id = category_id_mapping.get(category)
            try:
                name, uri = fetch_playlist(category_id=category_id)
                # await ctx.send("I sense you are angry\nCalm out with this playlist")
                # await ctx.send(f"[{name}]({uri})")
                embed = discord.Embed(title=name, url=uri, description="I sense you are angry\nCalm out with this playlist", color=0xFF5733)
                await ctx.send(embed=embed)
            except Exception as e:
                print("Error occured when fetch playlist")
                with open("err.log", "w") as log:
                    log.writelines(str(e.__class__) + "\n")
                await ctx.send("I am having some internal issues, please try again or contact Abhinav")

        # case "Fear":
        #     await ctx.send("I sense you are afraid of something")
        case "Happy":
            category = random.choice(happy_generes)
            category_id = category_id_mapping.get(category)
            try:
                name, uri = fetch_playlist(category_id=category_id)
                await ctx.send("You seems to be happy\nChill out with this playlist")
                embed = discord.Embed(title=name, url=uri, description="You seems to be happy\nChill out with this playlist", color=0xFF5733)
                await ctx.send(embed=embed)
            except Exception as e:
                print("Error occured when fetch playlist")
                with open("err.log", "w") as log:
                    log.writelines(str(e.__class__) + "\n")
                await ctx.send("I am having some internal issues, please try again or contact Abhinav")
        case "Sad":
            category = random.choice(sad_generes)
            category_id = category_id_mapping.get(category)
            try:
                name, uri = fetch_playlist(category_id=category_id)
                embed = discord.Embed(title=name, url=uri, description="I feel like you are worried\nRelax with this playlist\nDon't hide your emotions, talk with a real person, please", color=0xFF5733)
                await ctx.send(embed=embed)
            except Exception as e:
                print("Error occured when fetch playlist")
                with open("err.log", "w") as log:
                    log.writelines(str(e.__class__) + "\n")
                await ctx.send("I am having some internal issues, please try again or contact Abhinav")
        # case default:
        #     await ctx.send("I sense you are Surprised")

@client.command(name="inspire", help="Provide an inspiring qoute")
async def inspire(ctx):
    json_res = requests.get("https://zenquotes.io/api/quotes").json()
    quote = json_res[0]['q']
    author = json_res[0]['a']
    await ctx.channel.send(f"{quote} - _**{author}**_")
# Handle error by writting error msgs to an log file

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f"""
        Hi {member.name}, welcome to my Discord server!

        I'm VirtualElle, a discord bot created to help you.
        Things I can do:

        Command: !inspire
        Description: Provide an inspiring qoute
        Usage: !inspire

        Command: !recommend "[text]"
        Description: Recommends a music by analysing the emotion in the corresponding text. Please put the corresponding text in QUOTES
        Usage: !recommend "text-to-be-analyzed"

        Command: !ping
        Decription: A test command to see if the bot is online, if online returns pong else nothing
        Usage: !ping
        """
    )


client.run(TOKEN)