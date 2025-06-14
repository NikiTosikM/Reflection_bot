import os
import logging

import uvicorn


from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI , Request
from aiogram.types import Update
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .start_bot import bot, dp
from .handlers.file_operations import YaDisk
from .handlers.handler import word_doc_obj


logging.basicConfig()

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    url_webhook = os.getenv('BASE_URL')
    await bot.set_webhook(url=url_webhook, 
                        allowed_updates=dp.resolve_used_update_types(), 
                        drop_pending_updates=True)
    info =  await bot.get_webhook_info()
    print(info)
    scheduler.start()
    yield
    await bot.delete_webhook()
    scheduler.shutdown()
    

app = FastAPI(lifespan=lifespan)
scheduler = AsyncIOScheduler(timezone = 'Europe/Samara')
ya_disk = YaDisk(
    token=os.getenv('YA_DISK'),
    doc_obj=word_doc_obj
    )

scheduler.add_job(
        ya_disk.send_docx_document, 
        'interval', 
        seconds = 30
    )

@app.post("/")
async def webhook(request: Request):
    update = Update(**await request.json())
    await dp._process_update(update=update, bot=bot)


if __name__ == '__main__':
    uvicorn.run('src.main:app', port=8080, host=os.getenv('HOST'))