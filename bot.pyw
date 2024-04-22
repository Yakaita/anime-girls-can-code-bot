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

bot = commands.Bot(command_prefix=config["commandPrefix"], intents=discord.Intents.all())

@bot.event
async def on_ready():
    if config["sendOnReadyMessage"]:
      await bot.get_channel(config["onReadyMessageChannelId"]).send("Ready to send pics :)")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    for language in config["languages"].keys():
        updatedLanguage = r"\b"+ language.lower() + r"\b"
        if re.search(updatedLanguage,message.content.lower()) != None:
            if config["languages"][language]:
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

@bot.command
async def stop(ctx):
    if ctx.author.name in config["adminUsers"] or (config["allowServerAdminsToStop"] and any(role.permissions.administrator for role in ctx.author.roles)):
        await ctx.send("Shutting down")
        await bot.close()
    else:
        await ctx.reply("You are not aloud to shut me off!")

bot.run(BOT_TOKEN)
