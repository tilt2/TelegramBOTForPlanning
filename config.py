import sqlite3
import logging
import telebot
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils import *

HELP_HELLO = """Привет, {}! 
Надеюсь, что данный Telegram-бот поможет вам распланировать свое время так, чтобы вы успевали выполнять все свои дела вовремя!
Если вас есть предложения по поводу бота, пожалуйста, напишите мне в личные сообщения: @Becenniytilt"""

HELP = """Задача - переход в меню управления задачами
Заметка - переход в меню управления заметками
Удаление задач - переход в меню удаления задач

Если у вас есть предложения по поводу бота, пишите мне в ЛС: @Becenniytilt"""

FAQ = """Вопросы:

Этот раздел будет обновляться..."""

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

TOKEN = "5883689077:AAE1IqpSBxDCAjMQEXz748L3twDAu2o2Enw"
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)

db = sqlite3.connect(r'DATABASE BOT.db', check_same_thread=False)
cursor = db.cursor()

to_main_menu_btn = KeyboardButton("Главное меню")
to_del_tasks_btn = KeyboardButton("Удаление задач")
to_notes_btn = KeyboardButton("Заметка")
to_tasks_btn = KeyboardButton("Задача")
help_btn = KeyboardButton("Справка")
faq_btn = KeyboardButton("ЧаВо")


async def to_main_menu(message: types.Message, text="Вы в главном меню"):
    kb = [
        [to_tasks_btn, to_notes_btn],
        [help_btn, faq_btn],
    ]
    markup = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )
    await message.answer(text, reply_markup=markup)
    await ToMenusState.main_menu.set()


@dp.message_handler(regexp="Главное меню")
async def main_menu(message: types.Message, state: FSMContext):
    kb = [
        [to_tasks_btn, to_notes_btn],
        [help_btn, faq_btn],
    ]
    markup = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите в какое меню вы хотите перейти"
    )

    text = "Вы в главном меню, отсюда вы можете зайти в заметки или в задачи"

    await message.answer(text, reply_markup=markup)
    await state.finish()


@dp.message_handler(regexp='Заметка')
async def notes(message):
    add_note_btn = KeyboardButton("Добавить заметку")
    show_all_notes_btn = KeyboardButton("Показать все заметки")
    del_note_btn = KeyboardButton("Удалить заметку")
    del_all_notes_btn = KeyboardButton("Удалить все заметки")
    kb = [
        [add_note_btn, show_all_notes_btn],
        [del_note_btn, del_all_notes_btn],
        [to_tasks_btn],
        [help_btn, faq_btn],
    ]
    markup = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Что хотите сделать?"
    )
    text = 'Сейчас вы можете добавить/удалить/посмотреть свои заметки'
    await message.answer(text, reply_markup=markup)


@dp.message_handler(regexp='Задача')
async def tasks(message):
    add_task_btn = KeyboardButton("Добавить задачу")
    show_tasks_btn = KeyboardButton("Показать задачи на дату")
    show_all_tasks_btn = KeyboardButton("Показать все задачи")
    kb = [
        [add_task_btn, to_del_tasks_btn],
        [show_tasks_btn, show_all_tasks_btn],
        [to_notes_btn],
        [help_btn, faq_btn],
    ]
    markup = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Что хотите сделать?"
    )
    text = 'Сейчас вы можете добавить/удалить/посмотреть свои задачи'
    await message.answer(text=text, reply_markup=markup)


@dp.message_handler(regexp="Удаление задач")
async def del_tasks(message):
    del_date_btn = KeyboardButton("Удалить все задачи на дату")
    del_date_task_btn = KeyboardButton("Удалить задачу на дату")
    del_all_btn = KeyboardButton("Удалить ВСЕ задачи")
    kb = [
        [del_date_btn, del_date_task_btn],
        [del_all_btn],
        [to_tasks_btn, to_notes_btn],
        [help_btn, faq_btn],
    ]
    markup = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )
    text = "Вы можете удалить свои задачи"
    await message.answer(text, reply_markup=markup)


@dp.message_handler(regexp="Справка")
async def process_help(message):
    await message.answer(HELP)


@dp.message_handler(regexp="ЧаВо")
async def process_help(message):
    await message.answer(FAQ)
