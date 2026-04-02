import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils import executor

TOKEN = "8698369347:AAHks6SPzVosV8NZo2d8q0JrGkf3p1DqBwE"
import os
TOKEN = os.getenv("8698369347:AAHks6SPzVosV8NZo2d8q0JrGkf3p1DqBwE")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

users = {}

# --- КНОПКИ ---
level_kb = ReplyKeyboardMarkup(resize_keyboard=True)
level_kb.add("🎓 Бакалавриат", "🎓 Магистратура")

bachelor_kb = ReplyKeyboardMarkup(resize_keyboard=True)
bachelor_kb.add("🟥 Atlas Core Division",
                "🟦 Atlas Retail Dynamics",
                "🟩 Atlas Supply Nexus")

master_kb = ReplyKeyboardMarkup(resize_keyboard=True)
master_kb.add("⚫ Atlas Strategic Finance Unit",
              "🟣 Atlas Global Optimization Lab")

decision_kb = ReplyKeyboardMarkup(resize_keyboard=True)
decision_kb.add("Принять", "Отклонить")

ethics_kb = ReplyKeyboardMarkup(resize_keyboard=True)
ethics_kb.add("Согласиться", "Отказаться")

# --- START ---
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    users[message.from_user.id] = {"score": 0}

    await message.answer(
        "🏢 Atlas Strategic Industries\n\n"
        "Компания на грани банкротства.\n"
        "Спасите бизнес.\n\n"
        "Выберите уровень:",
        reply_markup=level_kb
    )

# --- LEVEL ---
@dp.message_handler(lambda m: "Бакалавриат" in m.text or "Магистратура" in m.text)
async def level(message: types.Message):
    users[message.from_user.id]["level"] = message.text

    if "Бакалавриат" in message.text:
        await message.answer("Выберите филиал:", reply_markup=bachelor_kb)
    else:
        await message.answer("Выберите филиал:", reply_markup=master_kb)

# --- TEAM ---
@dp.message_handler(lambda m: "Atlas" in m.text)
async def team(message: types.Message):
    users[message.from_user.id]["team"] = message.text

    await message.answer(
        "📩 Директор:\nСрочно анализируйте затраты."
    )

    await bot.send_document(message.chat.id, types.InputFile("atlas_part1_costs_bep.xlsx"))
    await message.answer("Введите BEP:")

# --- BEP ---
@dp.message_handler(lambda m: m.text.isdigit())
async def bep(message: types.Message):
    user = users[message.from_user.id]
    answer = int(message.text)

    if abs(answer - 5000) < 500:
        user["score"] += 20
        await message.answer("✅ +20")
    else:
        user["score"] -= 5
        await message.answer("❌ -5")

    await message.answer(f"💰 {user['score']} баллов")

    await bot.send_document(message.chat.id, types.InputFile("atlas_part2_overheads.xlsx"))
    await message.answer("Введите 'готово' после анализа")

# --- OVERHEAD ---
@dp.message_handler(lambda m: m.text.lower() == "готово")
async def overhead(message: types.Message):
    users[message.from_user.id]["score"] += 20

    await message.answer("✅ +20")

    await bot.send_document(message.chat.id, types.InputFile("atlas_part4_investment.xlsx"))
    await message.answer("Инвестировать?", reply_markup=decision_kb)

# --- INVEST ---
@dp.message_handler(lambda m: m.text in ["Принять", "Отклонить"])
async def invest(message: types.Message):
    user = users[message.from_user.id]

    if message.text == "Принять":
        user["score"] += 25
    else:
        user["score"] -= 10

    await message.answer(f"💰 {user['score']}")

    await message.answer(
        "⚠️ Форс-мажор!\nПоставщик повысил цены!"
    )

    await message.answer(
        "⚖️ Скрыть часть затрат?",
        reply_markup=ethics_kb
    )

# --- ETHICS ---
@dp.message_handler(lambda m: m.text in ["Согласиться", "Отказаться"])
async def ethics(message: types.Message):
    user = users[message.from_user.id]

    if message.text == "Отказаться":
        user["score"] += 15
    else:
        user["score"] -= 15

    await message.answer(
        f"🏁 Итог: {user['score']}\n\n"
        "📩 Отправьте отчет на:\n"
        "p6484132@gmail.com"
    )

executor.start_polling(dp)
