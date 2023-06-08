import logging
import aiogram

import functions

logging.basicConfig(level=logging.INFO, filename="../logs.log", filemode="w", format="%(asctime)s %(levelname)s %(message)s")

with open("../BOT_TOKEN.txt", "r") as file:
    BOT_TOKEN = file.read().strip()

bot = aiogram.Bot(token=BOT_TOKEN)
dp = aiogram.Dispatcher(bot)


async def setup_bot_commands(dispatcher):
    bot_commands = [
        aiogram.types.BotCommand(command="/start", description="Show start menu"),
        aiogram.types.BotCommand(command="/help", description="Show start menu"),
        aiogram.types.BotCommand(command="/info", description="Show player info"),
        aiogram.types.BotCommand(command="/inventory", description="Show player inventory"),
        aiogram.types.BotCommand(command="/change_lang", description="Changes language")
        ]
    await bot.set_my_commands(bot_commands)


@dp.message_handler(commands=["start", "help"])
async def start(message: aiogram.types.Message):
    logging.info(f" | Text: {message.text} | ID: {message.from_user.id} | User: {message.from_user.username}"
                 f" | Name: {message.from_user.first_name}")
    functions.except_new_account(message.from_user.id, message.from_user.username, message.from_user.first_name)
    keyboard = aiogram.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*functions.get_action_buttons(message.from_user.id))
    await message.answer(f"Select a language, you can also choose it using command /change_lang", reply_markup=keyboard)


@dp.message_handler(commands="info")
async def info(message: aiogram.types.Message):
    logging.info(f"Text: {message.text} | ID: {message.from_user.id} | User: {message.from_user.username}")
    answer = functions.get_player_info(message.from_user.id, message.from_user.username, message.from_user.first_name)
    keyboard = aiogram.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*functions.get_action_buttons(message.from_user.id))
    await message.answer(answer, reply_markup=keyboard)


@dp.message_handler(commands="inventory")
async def info(message: aiogram.types.Message):
    logging.info(f"Text: {message.text} | ID: {message.from_user.id} | User: {message.from_user.username}")
    answer = functions.get_player_inventory_info(message.from_user.id, message.from_user.username,
                                                 message.from_user.first_name)
    keyboard = aiogram.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*functions.get_action_buttons(message.from_user.id))
    await message.answer(answer, reply_markup=keyboard)


@dp.message_handler(commands="change_lang")
async def change_lang(message: aiogram.types.Message):
    logging.info(f"Text: {message.text} | ID: {message.from_user.id} | User: {message.from_user.username}")
    answer = "Choose game language"
    keyboard = aiogram.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*["en", "ru"])
    await message.answer(answer, reply_markup=keyboard)


@dp.message_handler()
async def start(message: aiogram.types.Message):
    logging.info(f" | Text: {message.text} | ID: {message.from_user.id} | User: {message.from_user.username}"
                 f" | Name: {message.from_user.first_name}")
    answer = functions.execute_action(message.text, message.from_user.id, message.from_user.username,
                                      message.from_user.first_name)
    keyboard = aiogram.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*functions.get_action_buttons(message.from_user.id))
    await message.answer(answer, reply_markup=keyboard)


if __name__ == "__main__":
    aiogram.executor.start_polling(dp, skip_updates=True, on_startup=setup_bot_commands)
