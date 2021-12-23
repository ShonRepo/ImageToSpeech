from PIL import Image
import pytesseract
# import pyttsx3
import gtts
from playsound import playsound
import time

from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram import Bot

from pydub import AudioSegment

bot = Bot('5079044432:AAEzSuphtSBX8R0Fto-JKXADeMbvz9BvZzE')
dp = Dispatcher(bot)
# engine = pyttsx3.init()

@dp.message_handler(content_types=["photo"])
async def get_photo(message):

    file_info = await bot.get_file(message.photo[-1].file_id)
    print('get photo')

    await bot.send_message(message.from_user.id, 'Ожидайте...')

    await message.photo[-1].download('info.' + file_info.file_path.split('.')[-1]) # ++
    text = read_image('info.' + file_info.file_path.split('.')[-1])

    say(text)

    file = open('text_to_speech.mp3', 'rb')
    await bot.send_audio(message.from_user.id, file, reply_to_message_id=message.message_id)
    file.close()
    print('message sended')

def read_image(file):
  image = Image.open(file)
  
  text = pytesseract.image_to_string(image, lang='rus')

  print('final read image')

  return text

def say(text):
  tts = gtts.gTTS(text, lang='ru')
  tts.save('text_to_speech.mp3')
  time.sleep(5)
  print('audio saved!')


if __name__ == '__main__':
    print('bot started')
    executor.start_polling(dp)