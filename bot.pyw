from discord.ext import commands
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from dotenv import load_dotenv
import discord, re, random, os, json

# load the .env file
load_dotenv()
# load the config
with open('config.json','r') as config_file:
    config = json.load(config_file)

BOT_TOKEN = os.getenv("BOT_TOKEN")
languages =["ABAP","AI","APL","ASM","Ada","Agda","Algorithms","Angular","Architecture","Beef","C","CMake","CSS","Clojure","Cobol","CoffeeScript","Compilers","D","Dart","Delphi","Design Patterns","Editors","Elixir","Elm","F#","FORTH","Fortran","GDScript","Go","Godot","Haskell","HoTT","HolyC","Idris","Java","Javascript","Julia","Kotlin","Linux","Lisp","Lua","Math","Memes","Mixed","MongoDB","Nim","NodeJs","OCaml","Objective-C","Orchestrator","PHP","Perl","Personification","PowerShell","Prolog","Purescript","Python","Quantum Computing","R","Racket","RayTracing","ReCT","Regex","Ruby","Rust","SICP","SQL","Scala","Shell","Smalltalk","Solidity","Swift","Systems","Typescript","UEFI","Unity","Unreal","V","VHDL","Verilog","Visual Basic","VueJS","Vulkan","WebGL"]

bot = commands.Bot(command_prefix="", intents=discord.Intents.all())

@bot.event
async def on_ready():
    channel = bot.get_channel(1136737687106236528)
    await channel.send("Reloaded")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    for language in languages:
        updatedLanguage = r"\b"+ language.lower() + r"\b"
        if re.search(updatedLanguage,message.content.lower()) != None:
            await message.channel.send(f"Picture of {message.author.display_name} incoming!")
            transport: AIOHTTPTransport = AIOHTTPTransport(url="https://graphql.senpy.club")
            
            async with Client(transport=transport, fetch_schema_from_transport=True) as client:
                query = gql(
                  """
                  query getImagesFromLanguage($language: String!){
                    language(language: $language)
                  }
                  """
                )
                image = random.choice((await client.execute(query,variable_values={"language":language}))["language"])

                await message.channel.send(image)

bot.run(BOT_TOKEN)
