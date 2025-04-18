import os
import logging
import asyncio
import requests
import instaloader
from aiogram import Bot, Dispatcher, types,F
from aiogram.filters import Command
from aiogram.types import FSInputFile

BOT_TOKEN = "7759284109:AAFQST6M2iSiT3gV32q4nOTgVYjcNKhjL2Q"
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
L = instaloader.Instaloader()

async def download_instagram_video(url: str):
    try:
        shortcode = url.split("/")[-2]
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        
        if post.is_video:
            video_url = post.video_url
            response = requests.get(video_url)
            
            filename = f"temp_video_{post.owner_username}.mp4"
            with open(filename, 'wb') as f:
                f.write(response.content)
            
            return filename
        return None
    except Exception as e:
        print(f"Xatolik: {str(e)}")
        return None

@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("Instagram video yuklovchi botga xush kelibsiz!\nVideo yuklash uchun post havolasini yuboring.")

@dp.message(F.text.contains("instagram.com"))
async def handle_instagram_link(message: types.Message):
    url = message.text
    await message.answer("Video yuklanmoqda...")
    
    video_path = await download_instagram_video(url)
    if video_path:
        video = FSInputFile(video_path)
        await message.answer_video(video=video)
        os.remove(video_path)
    else:
        await message.answer("❌ Video yuklab olinmadi. \nHavolani tekshiring yoki post ochiq emas.")



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(dp.start_polling(bot))
