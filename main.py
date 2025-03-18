# Dependencies
import os
import sys
import requests
import asyncio
import json
from discord.ext import commands
from colorama import Fore

# Config
debug = True # Set to False to disable debug output
imageSize = 512 # 128, 256, 512, 1024, 2048, 4096
profileChannels = {
    # example:
    # channel_id: ["channel_name", "webhook"]
    # 0000000000000000000: ["main", "https://discord.com/api/webhooks/000000000000000000/]
}

# Variables
webhookQueue = asyncio.Queue()

# Functions

def debugPrint(message,status,force=False):
    if debug or force:
        if status:
            print(f"{Fore.GREEN}[+]{Fore.RESET} {message}")
        else:
            print(f"{Fore.RED}[-]{Fore.RESET} {message}")

def getToken():
    if os.path.exists("token.txt"):
        with open("token.txt", "r") as f:
            token = f.read().strip()
            if not token:
                debugPrint("Token is required to proceed.", False)
                sys.exit(1)
            return token
    else:
        token = input("Enter your Discord token (will not echo): ")
        if not token:
            debugPrint("Token is required to proceed.", False)
            sys.exit(1)
        with open("token.txt", "w") as f:
            f.write(token)
        return token
    
def checkWebhook(webhook):
    status = False
    if webhook.startswith("https://discord.com/api/webhooks/"):
        response = requests.get(webhook)
        if response.status_code != 200:
            status = True
    else:
        status = True
    
    if status:
        for channel in profileChannels:
            if profileChannels[channel][1] == webhook:
                debugPrint(f"Webhook for {profileChannels[channel][0]} channel is invalid and will not function.", False, True)
                break

async def downloadAvatar(message):
    for embed in message.embeds:
        imageUrl = embed.image.url.replace("?size=4096", f"?size={imageSize}")
        channelType = message.channel.id

        debugPrint(f"Downloading image from {profileChannels[channelType][0]} channel.", True)
        fileName = imageUrl.split("/")[-1].split("?")[0]
        filePath = f"pfps/{profileChannels[channelType][0]}/{fileName}"

        response = requests.get(imageUrl)
        if response.status_code == 200:
            with open(filePath, "wb") as f:
                f.write(response.content)
            await webhookQueue.put((profileChannels[channelType][1], filePath))
            debugPrint(f"Image downloaded.", True)
        else:
            debugPrint(f"Failed to download {fileName}.", False)

async def processQueue():
    while True:
        imageWebhook, filePath = await webhookQueue.get()
        try:
            with open(filePath, "rb") as file:
                files = {"file": file}
                payload = {
                    "embeds": [
                        {
                            "color": 0x000000,
                            "footer": {
                                "text": "Authenticating"
                            },
                            "image": {"url": f"attachment://{filePath.split('/')[-1]}"}
                        }
                    ],
                    "username": "Authenticating",
                    "avatar_url": "https://cdn.discordapp.com/avatars/1340045863401033800/6a9c3c0aba65383034bca92339083cfd.webp?size=128"
                }
                response = requests.post(imageWebhook,files=files,data={"payload_json": json.dumps(payload)})
                if response.status_code == 200:
                    debugPrint(f"Image sent to webhook.", True)
                else:
                    debugPrint(f"Failed to send image to webhook.", False)
        except Exception as error:
            debugPrint(f"Error processing webhook queue: {error}", False)
        finally:
            webhookQueue.task_done()

async def main():
    TOKEN = getToken()
    bot = commands.Bot(command_prefix="!")

    @bot.event
    async def on_ready():
        debugPrint(f"Debug mode is currently {'enabled' if debug else 'disabled'}.", True, True)
        debugPrint(f"Logged in as {bot.user.name}.", True, True)
        for channel in profileChannels:
            checkWebhook(profileChannels[channel][1])
            if not os.path.exists(f"pfps/{profileChannels[channel][0]}"):
                os.makedirs(f"pfps/{profileChannels[channel][0]}")

    @bot.event
    async def on_message(message):
        if message.channel.id not in profileChannels:
            return
        await downloadAvatar(message)

    asyncio.create_task(processQueue())

    try:
        await bot.start(TOKEN)
    except Exception as error:
        debugPrint(f"Error running bot: {error}", False)

asyncio.run(main())