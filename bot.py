import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils import executor

TOKEN = "8698369347:AAHks6SPzVosV8NZo2d8q0JrGkf3p1DqBwE"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

users = {}

