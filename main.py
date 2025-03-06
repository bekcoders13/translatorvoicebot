import telebot
from googletrans import Translator
from gtts import gTTS
import edge_tts
import os
import asyncio

API_TOKEN = "7604019745:AAGzwL7e43EjboFRTRS9DfwO_tDfT7sAiT8"
bot = telebot.TeleBot(API_TOKEN)
translator = Translator()


@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Assalomu alaykum!\nBu bot so‘zlarni o‘zbekchadan inglizchaga yoki aksincha tarjima qiladi "
        "va ovozli o‘qib beradi! 🎙"
    )


@bot.message_handler(content_types=['text'])
def translate_text(message):
    text = message.text
    detected_lang = translator.detect(text).lang

    if detected_lang == 'uz':
        translated_text = translator.translate(text, dest='en').text
        tts = gTTS(translated_text, lang='en')
        audio_file = "voice.mp3"
        tts.save(audio_file)
        flag = "🇺🇿➡️🇬🇧"
    elif detected_lang == 'en':
        translated_text = translator.translate(text, dest='uz').text
        flag = "🇬🇧➡️🇺🇿"

        voice = 'uz-UZ-MadinaNeural'  # Microsoft Edge Uzbek voice
        audio_file = "voice.mp3"

        # Edge TTS orqali ovozli fayl yaratish
        asyncio.run(save_audio_edge_tts(translated_text, voice, audio_file))
    else:
        bot.send_message(message.chat.id, "Kechirasiz, faqat o‘zbek va ingliz tillari qo‘llab-quvvatlanadi.")
        return

    # Matnli tarjima yuborish
    bot.send_message(message.chat.id, f"{flag}\n{translated_text}")

    # Ovozli xabar yuborish
    with open(audio_file, "rb") as voice:
        bot.send_audio(message.chat.id, voice)
    os.remove(audio_file)


async def save_audio_edge_tts(text, voice, filename):
    """Edge-TTS orqali ovozli fayl yaratish."""
    tts = edge_tts.Communicate(text, voice)
    await tts.save(filename)


bot.polling(non_stop=True)
