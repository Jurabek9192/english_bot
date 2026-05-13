import asyncio
import logging
import sys
from os import getenv

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
import os
import logging
from word_take import get_word
from googletrans import Translator

# .env faylini yuklaymiz
load_dotenv()

# TOKEN ni to'g'ri string kalit bilan olamiz
BOT_TOKEN = getenv("TOKEN")

dp = Dispatcher()
# Translator obyekti (ba'zi versiyalarda asinxronlik uchun qo'shimcha sozlamalar kerak bo'lishi mumkin)
translator = Translator()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Salom, {html.bold(message.from_user.full_name)}! \nSo'z yuboring yoki matn yozing.")


@dp.message(Command('help'))
async def help_handler(message: Message) -> None:
    text = f"{html.bold(message.from_user.full_name)}, bu bot so'zlar ma'nosini topadi va matnlarni tarjima qiladi."
    await message.answer(text)



# Loglarni terminalda aniq ko'rish uchun
logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    logging.error("XATOLIK: TOKEN muhit o'zgaruvchisi topilmadi!")
    exit(1) # Botni xato bilan to'xtatish
else:
    logging.info("TOKEN muvaffaqiyatli yuklandi.")


@dp.message()
async def message_handler(message: Message) -> None:
    # Faqat matnli xabarlarni tekshiramiz
    if not message.text:
        return

    try:
        text = message.text
        # Kiruvchi matn tilini aniqlash
        # DIQQAT: googletrans asinxron ishlashi uchun event_loop bilan muammo bo'lsa,
        # bu qismni oddiyroq qilish kerak bo'ladi.
        detection = translator.detect(text)
        lang = detection.lang

        # Agar matn 2 tadan ko'p so'z bo'lsa - TARJIMA QILAMIZ
        if len(text.split()) >= 2:
            dest_lang = 'uz' if lang == 'en' else 'en'
            translation = translator.translate(text, dest=dest_lang)
            await message.reply(f"🔄 Tarjima ({dest_lang}):\n{translation.text}")

        # Agar bitta so'z bo'lsa - LUG'ATDAN QIDIRAMIZ
        else:
            meaning = get_word(text)
            if meaning:
                response = f"🔍 So'z: {html.code(text)}\n\n📖 Ma'nosi:\n{meaning['definitions']}"
                await message.reply(response)

                if meaning.get('audio'):
                    await message.reply_voice(voice=meaning['audio'], caption="Talaffuz")
            else:
                await message.reply(f"Kechirasiz, '{text}' so'zi bo'yicha ma'lumot topilmadi.")

    except Exception as e:
        logging.error(f"Xatolik yuz berdi: {e}")
        await message.answer("Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")


async def main() -> None:
    # Bot obyektini main ichida yaratish tavsiya etiladi
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # Botni ishga tushirishdan oldin eski navbatda turgan xabarlarni o'chirib tashlaymiz
    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot to'xtatildi")
