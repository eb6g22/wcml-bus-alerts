import discord
import requests
import os
from discord.ext import tasks

TOKEN =  # Replace with your bot's token
GUILD_ID = ''  # Replace with your server's ID
ROLE_NAME = 'Bus Replacement Alerts'  # Replace with the role name you want to alert

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

def get_bus_replacement_info():
    # Example API call (replace with actual API)
    url = 'https://api.openrailway.com/v1/alerts'  # Replace with actual API URL
    response = requests.get(url)
    data = response.json()
    return data

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    check_for_alerts.start()  # Start the task loop

@tasks.loop(minutes=5)  # Check every 5 minutes
async def check_for_alerts():
    alerts = get_bus_replacement_info()
    
    if alerts.get('bus_replacement'):  # Adjust depending on the data structure
        guild = client.get_guild(int(GUILD_ID))
        role = discord.utils.get(guild.roles, name=ROLE_NAME)
        
        if role:
            await guild.text_channels[0].send(f"@{role.name} Bus replacement services are active! Check updates!")
        else:
            print("Role not found")

client.run(TOKEN)
