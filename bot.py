import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command, CommandObject
from aiogram.enums.dice_emoji import DiceEmoji
from config_reader import config
from aiogram.enums import ParseMode
from aiogram.utils.formatting import Text, Bold
from aiogram import F, html
from datetime import datetime



logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()



@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer(f"Hello, <b>{message.from_user.full_name}</b>", parse_mode = ParseMode.HTML)
    
async def main():
    await dp.start_polling(bot)



@dp.message(Command("hello"))
async def cmd_hello(message: types.Message):
    content = Text("Hello, ",Bold(message.from_user.full_name))
    await message.answer(**content.as_kwargs())



@dp.message(Command("dice"))
async def cmd_dice(message: types.Message):
    await message.answer_dice(emoji=DiceEmoji.BOWLING)



@dp.message(Command("settimer"))
async def cmd_settimer(message: types.Message, command: CommandObject):
    if command.args is None:
        await message.reply("Необходимо передать аргументы!")
        return
    try:
        delay_time, text_to_send = command.args.split(" ", maxsplit=1)
    except ValueError:
        await message.reply("Неправильный формат данных\nПример: /settimer <time> <message> ")
        return
    await message.answer(f"Таймер добавлен:\nВремя: {delay_time}\nСообщение: {text_to_send}")



# @dp.message(F.text)
# async def echo_with_time(message: types.Message):
#     time_now = datetime.now().strftime('%H:%M')
#     added_text = html.underline(f'Создано в {time_now}')
#     await message.answer(f'{message.html_text}\n\n{added_text}',parse_mode="HTML")



@dp.message(F.text)
async def extract_data(message: types.Message):
    data = {"url" : "", "email" : "", "code" : ""}
    entities = message.entities or []
    for item in entities:
        if item.type in data.keys():
            data[item.type] = item.extract_from(message.text)
    await message.reply(f"Данные добавлены:\nUrl: {html.quote(data['url'])}\nEmail: {html.quote(data['email'])}\nPassword: {html.quote(data['code'])}")





if __name__ == "__main__":
    asyncio.run(main())