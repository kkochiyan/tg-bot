from aiogram import Bot, Dispatcher
from app.hendlers import router
import asyncio
from app.database.models import async_main
from dotenv import load_dotenv
import os

async def main():
    await async_main()
    load_dotenv()
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher()
    dp.include_router(router=router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')


