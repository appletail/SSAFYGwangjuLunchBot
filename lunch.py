import os
import requests
import discord
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.environ.get('TOKEN')

today = datetime.today().strftime("%Y%m%d")
today_url = os.environ.get('TODAY_URL') + today
week_url = os.environ.get('WEEK_URL')
week_all_meal = requests.get(week_url).json()
next_week_url = os.environ.get('NEXT_WEEK_URL')
next_week_all_meal = requests.get(next_week_url).json()

week = {
    '!월': 'mo',
    '!화': 'tu',
    '!수': 'we',
    '!목': 'th',
    '!금': 'fr',
}

next_week = {
    '!월월': 'mo',
    '!화화': 'tu',
    '!수수': 'we',
    '!목목': 'th',
    '!금금': 'fr',
}


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        await self.change_presence(status=discord.Status.online, activity=discord.Game("!도움 | 점심메뉴 고르기"))

    async def on_message(self, message):
        if message.author == self.user:
            return
        # 오늘 점심
        if message.content == '!점심':
            today_all_meal = requests.get(
                today_url).json().get('data').get('2')
            lunch_message = ''
            is_thumbnail_true = today_all_meal[1]['thumbnailUrl']

            for idx in range(6):
                meal = today_all_meal[idx]

                if is_thumbnail_true:
                    embed = discord.Embed(title=meal['corner'])
                    embed.add_field(name=meal['name'],
                                    value=meal['side'], inline=False)
                    if idx < 5:
                        embed.set_image(url=meal['thumbnailUrl'])
                        embed.set_footer(
                            text=f'kcal: {meal.get("kcal")}')
                    else:
                        cat_url = requests.get(
                            'https://api.thecatapi.com/v1/images/search').json()[0].get('url')
                        embed.set_image(url=cat_url)
                        embed.set_footer(text='!야옹')
                    await message.channel.send(embed=embed)
                else:
                    lunch_message += '__**{}**__\n {}\n {}\n kcal: {}\n\n'.format(
                        meal['corner'], meal['name'], meal['side'], meal.get('kcal'))
                    if idx == 5:
                        lunch_message += '\n**이제 이번주와 다음주 점심을 모두 알 수 있습니다.\n<!월> 혹은 <!월월>을 채팅창에 입력해보세요!'

            if not is_thumbnail_true:
                await message.channel.send(lunch_message)
            now = datetime.today().strftime("%Y/%m/%d %H:%M:%S")
            print(now, '\033[94m' + 'TODAY' + '\033[0m' + '    메시지 전송 완료')
        # 이번주 점심들
        elif week.get(message.content):
            day = week.get(message.content)
            lunch_message = ''
            for meal in week_all_meal.get('data').get(day).get('2')[:6]:
                lunch_message += '__**{}**__\n {}\n {}\n kcal: {}\n\n'.format(
                    meal['corner'], meal['name'], meal['side'], meal.get('kcal'))
            await message.channel.send(lunch_message)
            now = datetime.today().strftime("%Y/%m/%d %H:%M:%S")
            print(now, '\033[94m' + day.upper() +
                  '\033[0m' + '       메시지 전송 완료')
        # 다음주 점심들
        elif next_week.get(message.content):
            day = next_week.get(message.content)
            lunch_message = ''
            now = datetime.today().strftime("%Y/%m/%d %H:%M:%S")
            try:
                for meal in next_week_all_meal.get('data').get(day).get('2')[:6]:
                    lunch_message += '__**{}**__\n {}\n {}\n kcal: {}\n\n'.format(
                        meal['corner'], meal['name'], meal['side'], meal.get('kcal'))
                await message.channel.send(lunch_message)
                print(now, '\033[94m' + day.upper() +
                      '\033[0m' + '       메시지 전송 완료')
            except:
                await message.channel.send('**점심이 없어요**')
                print(now, '\033[94m' + day.upper() +
                      '\033[0m' + '       점심없음 전송 완료')

        # 고양이 사진
        elif message.content == '!야옹':
            embed = discord.Embed(color=0x7cbbfe)
            cat_url = requests.get(
                'https://api.thecatapi.com/v1/images/search').json()[0].get('url')
            embed.set_image(url=cat_url)
            await message.channel.send(embed=embed)
            now = datetime.today().strftime("%Y/%m/%d %H:%M:%S")
            print(now, '\033[94m' + 'MEW' + '\033[0m' + '      메시지 전송 완료')

        # 개 사진
        elif message.content == '!멍멍':
            embed = discord.Embed(color=0x7cbbfe)
            dog_url = requests.get(
                'https://api.thedogapi.com/v1/images/search').json()[0].get('url')
            embed.set_image(url=dog_url)
            await message.channel.send(embed=embed)
            now = datetime.today().strftime("%Y/%m/%d %H:%M:%S")
            print(now, '\033[94m' + 'DOG' + '\033[0m' + '      메시지 전송 완료')

        elif message.content == '!도움':
            text = '''
                - 명령어\n
                !점심 : 오늘 점심\n
                !월   : 이번주 월요일 점심\n
                !월월 : 다음주 월요일 점심\n
                !야옹 : 랜덤 고양이 사진\n
                !멍멍   : 랜던 개 사진\n
            - 런치봇은 6번 메시지를 보내며 이는 각 메시지 마지막에 사진을 포함시키기 위함입니다.
                '''
            await message.channel.send(text)


intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(TOKEN)
