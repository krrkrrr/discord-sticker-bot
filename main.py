import os
import discord
from discord.ext import commands, tasks

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Target Channel ID (Replace with your channel's ID)
TARGET_CHANNEL_ID = 1551304309227004144

# Official Discord Wumpus Wave Sticker ID
STICKER_ID = 749054660769218631

@tasks.loop(minutes=30)
def send_sticker_task():
    channel = bot.get_channel(TARGET_CHANNEL_ID)
    if channel:
        try:
            sticker = bot.get_sticker(STICKER_ID)
            if sticker:
                bot.loop.create_task(channel.send(stickers=[sticker]))
                print("Wumpus wave sticker sent!")
            else:
                # Fallback if bot.get_sticker returns None for default stickers
                sticker_obj = discord.Object(id=STICKER_ID)
                bot.loop.create_task(channel.send(stickers=[sticker_obj]))
                print("Wumpus wave sticker sent via object!")
        except Exception as e:
            print(f"Error sending sticker: {e}")

@send_sticker_task.before_loop
async def before_send_sticker_task():
    await bot.wait_until_ready()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    if not send_sticker_task.is_running():
        send_sticker_task.start()

bot.run(os.environ['DISCORD_TOKEN'])
