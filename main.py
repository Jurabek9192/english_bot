import asyncio
import logging
import sys
import os
from aiohttp import web  # Render porti uchun kerak
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from word_take import get_word
from googletrans import Translator

load_dotenv()


TOKEN = os.getenv("TOKEN")
if not TOKEN:
    print("XATOLIK: TOKEN muhit o'zgaruvchisi (Environment Variable) topilmadi!")
    sys.exit(1)

dp = Dispatcher()
translator = Translator()

try:
    from word_take import get_word
except ImportError:
    logging.error("XATOLIK: word_take.py fayli topilmadi!")
    get_word = None

from googletrans import Translator




async def handle(request):
    return web.Response(text="Bot is live!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    logging.info(f"Web server {port}-portda ishga tushdi.")


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Salom, {html.bold(message.from_user.full_name)}!")

@dp.message()
async def changer(message: Message) -> None:
    if not message.text:
        return
    try:
       
        if len(message.text.split()) >= 2:
            translation = translator.translate(message.text, dest='uz')
            await message.reply(translation.text)
        else:
            if get_word:
                meaning = get_word(message.text)
                if meaning:
                    await message.reply(f"So'z: {message.text}\nMa'nosi: {meaning['definitions']}")

                    if meaning.get('audio'):
                    await message.reply_voice(voice=meaning['audio'], caption="Talaffuz")
                else:
                    await message.reply("Topilmadi.")
    except Exception as e:
        logging.error(f"Xabar ishlashida xato: {e}")

async def main() -> None:

    await start_web_server()
    

    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await bot.delete_webhook(drop_pending_updates=True)
    
    logging.info("Polling boshlandi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot to'xtatildi.")
