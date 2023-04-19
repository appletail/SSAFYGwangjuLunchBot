import os
import requests
import discord
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.environ.get('TOKEN')
 
today = datetime.today().strftime("%Y%m%d")
url = os.environ.get('URL') + today

 
class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        await self.change_presence(status=discord.Status.online, activity=discord.Game("대기중"))
 
    async def image(ctx):
        await ctx.send("image_link")

    async def on_message(self, message):
        if message.author == self.user:
            return
 
        if message.content == '!점심':
            today_all_meal = requests.get(url)
            for meal in today_all_meal.json()['data']['2'][:6]:
                lunch_message = ''
                thumbnailUrl = meal['thumbnailUrl'] if meal['thumbnailUrl'] else '사진이 안올라옴\n'
                lunch_message += '__**{}**__\n {}\n {}\n {}\n\n'.format(meal['corner'], meal['name'], meal['side'],thumbnailUrl)
                await message.channel.send(lunch_message)
            print('메시지 전송 완료')
 
 
intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(TOKEN)