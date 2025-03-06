import telebot
from deep_translator import GoogleTranslator
import edge_tts
import os
import asyncio
import tempfile

API_TOKEN = "7604019745:AAGzwL7e43EjboFRTRS9DfwO_tDfT7sAiT8"
bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        """Assalomu alaykum! 👋\n
        Bu bot siz yuborgan so‘zni ingliz yoki o‘zbek tiliga tarjima qiladi va ovozli talaffuz faylini yuboradi.\n
        So‘z yuboring va natijani kuting! ✨"""
    )


@bot.message_handler(content_types=['text'])
def translate_text(message):
    text = message.text
    try:
        # Avtomatik tildan tarjima qilish
        translated_to_en = GoogleTranslator(source='auto', target='en').translate(text)
        translated_to_uz = GoogleTranslator(source='auto', target='uz').translate(text)

        # Tarjima natijasini chiqarish
        response = f"\n🇺🇿 ➡️ 🇬🇧 {translated_to_en}\n🇬🇧 ➡️ 🇺🇿 {translated_to_uz}"
        bot.send_message(message.chat.id, response)

        # Ovozli talaffuz yaratish
        en_voice = 'en-US-JennyNeural'
        uz_voice = 'uz-UZ-MadinaNeural'

        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as en_tmpfile, \
                tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as uz_tmpfile:

            # Ingliz tilida ovoz yaratish
            tts_en = edge_tts.Communicate(translated_to_en, en_voice)
            asyncio.run(tts_en.save(en_tmpfile.name))

            # O‘zbek tilida ovoz yaratish
            tts_uz = edge_tts.Communicate(translated_to_uz, uz_voice)
            asyncio.run(tts_uz.save(uz_tmpfile.name))

            # Fayllarni yuborish
            with open(en_tmpfile.name, "rb") as voice:
                bot.send_audio(message.chat.id, voice)

            with open(uz_tmpfile.name, "rb") as voice:
                bot.send_audio(message.chat.id, voice)

            # Fayllarni o‘chirish
            os.unlink(en_tmpfile.name)
            os.unlink(uz_tmpfile.name)
    except Exception as e:
        bot.send_message(message.chat.id, f"Xatolik yuz berdi: {e}")


bot.polling(non_stop=True)
