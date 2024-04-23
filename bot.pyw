from discord.ext import commands
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from dotenv import load_dotenv
import discord, re, random, os, json

# load the .env file
load_dotenv()
# load the config
with open('config.json','r') as config_file: config = json.load(config_file)

# Setup bot
bot = commands.Bot(command_prefix=config["commandPrefix"], intents=discord.Intents.all())

# On ready event
@bot.event
async def on_ready():
    if config["sendOnReadyMessage"]: await bot.get_channel(config["onReadyMessageChannelId"]).send("Ready to send pics :)")

# On message event
@bot.event
async def on_message(message):
    if message.author == bot.user: return # Dont reply to my own messages

    # check if this is a command
    if message.content.startswith(config["commandPrefix"] or any(message.content[0] for prefix in config["otherPrefixesToIgnore"])):
        await bot.process_commands(message)
        return
    
    # Check if the whitelist is active and if this channel is not part of it
    if config["useWhitelist"] and message.channel.id not in config["whitelist"]:
        await bot.process_commands(message)
        return
    
    # Check if the channel is in the blacklist
    if message.channel.id in config["blacklist"]:
        await bot.process_commands(message)
        return

    # Check for each language in the message
    for language in config["languages"].keys():
        updatedLanguage = r"\b"+ language.lower() + r"\b"
        if re.search(updatedLanguage,message.content.lower()) != None:
            # Check if the language is set to True in the config
            if config["languages"][language]:
                # Get the image
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

# stop command 
@bot.command()
async def stop(ctx):
    # Check if the user has the correct permissions
    if ctx.author.name in config["adminUsers"] or (config["allowServerAdminsToStop"] and any(role.permissions.administrator for role in ctx.author.roles)):
        await ctx.send("Shutting down")
        await bot.close()
    else:
        await ctx.reply("You are not aloud to shut me off!")

bot.run(os.getenv("BOT_TOKEN"))
