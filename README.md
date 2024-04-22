# This bot just sends pictures of anime girls holding programming books

<center><strong><em>Written in Python</em></strong> </center>  

![Picture of anime girl holding a python book](https://raw.githubusercontent.com/cat-milk/Anime-Girls-Holding-Programming-Books/master/Python/Tomoe_Takasago_With_Python_Books.jpg)

## Things this bot does

* Watches chats for the names of programming languages
* When it detects a programming language it will send an image (if available) of an anime girl holding a book about that language.  

Images are sourced from the [Anime-Girls-Holding-Programming-Books](https://github.com/cat-milk/Anime-Girls-Holding-Programming-Books "Probably the worlds most important repo") repo so if you want to see an image you made then fork that repo and make a pull request to add the image.

### Setup

1. Download this repo
2. [Create a Discord bot](https://discordpy.readthedocs.io/en/stable/discord.html "A tutorial by discordpy")
3. Set the **Privileged Gateway Intents** in the **Bot** tab all to on
4. Get the invite link from the **OAuth2 URL Generator** in the **OAuth2** tab
    * Give it the scope **bot**
    * Give it the following permissions:
        * Send Messages
        * Read Message History
        * Embed Links
            > :memo: **Note:** Im not certain it needs anything other than *Send Messages* but tbh its easier to just give it the extra perms just in case :)
    * Copy the URL into your browser and invite it to the server you want it on
5. Create a .env file in the folder with the python script and copy the contents of the .env.example file into it
6. Reset the token for the bot and paste the token in the .env file.
7. Check over the config.json file and make the desired changes. I have set a few specific languages to false by default because they will cause spam.
8. Either host the bot on a server or host it from your own computer and thats it. I have my bot run on my pc startup

### FAQ (or things I think you will ask)

* ***Why are C# and C++ set to false by defaut?***
    > Because the code looks for words using word characters and *#* and *+* arent included. So when it sees **C#** or **C++** it sees it as **C** and then sends an image from all 3 languages. This can be fixed I'm just lazy.