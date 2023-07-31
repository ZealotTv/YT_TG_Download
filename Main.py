import os
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
from Download import download_audio


load_dotenv()

API_KEY = os.getenv("API_KEY")
bot = Bot(token=API_KEY)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply(f"Привет, {message.from_user.full_name}!\nЯ бот, который был создан для загрузки музыки с ютуба!\n Отправь мне ссылку на ролик, я скачаю из него аудиодорожки и скину её тебе)")
    
@dp.message_handler(commands=['search'])
async def send_audio(message: types.Message):
    arg = message.get_args()
    if not arg:
        await message.reply(f'ДАЙ ССЫЛКУ!!!')
    else:
        msg = await message.reply(f'Подождите, пожалуйста! Скачиваю!')
        try:
            audio_info = download_audio(arg)
            with open(audio_info[0], 'rb') as f:
                await msg.delete()
                msg = await message.reply(f'Подождите, пожалуйста! Отправляю!')
                await bot.send_audio(chat_id=message.chat.id, audio=f,  performer = audio_info[1], title = audio_info[2])
                await msg.delete()
                os.unlink(audio_info[0])
        except Exception as e:
            await message.reply('ошибка((')


if __name__ == '__main__':
    executor.start_polling(dp)