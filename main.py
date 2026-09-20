import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import discord
from discord.ext import commands, tasks

# --- Dummy HTTP Server for Render Health Check ---
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"OK")

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    server.serve_forever()

# Start the web server in a background thread
threading.Thread(target=run_web_server, daemon=True).start()

# --- Discord Bot Setup ---
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Replace 123456789012345678 with your actual target channel ID
TARGET_CHANNEL_ID = 123456789012345678

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

# Run bot using Environment Variable token
bot.run(os.environ['DISCORD_TOKEN'])
