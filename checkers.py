from config import *
from datetime import *


def change_date(user_date: str):
    if user_date == "сегодня":
        user_date = datetime.now().strftime("%d.%m.%Y")
    elif user_date == "завтра":
        user_date = (datetime.now() + timedelta(days=1)).strftime("%d.%m.%Y")
    elif user_date == "послезавтра":
        user_date = (datetime.now() + timedelta(days=2)).strftime("%d.%m.%Y")
    try:
        checked_date = datetime.strptime(user_date, "%d.%m.%Y").strftime("%Y-%m-%d")
        return checked_date
    except ValueError:
        return False


async def check_main_menu(message: types.Message, message_from_user: str, state: FSMContext):
    if message_from_user.lower() == "главное меню":
        kb = [
            [to_tasks_btn, to_notes_btn],
            [help_btn, faq_btn],
        ]
        markup = ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True
        )
        text = "Вы в главном меню, отсюда вы можете зайти в заметки или в задачи"
        await message.answer(text, reply_markup=markup)
        await state.finish()
        return 1
    else:
        return 0


async def to_main_menu(message: types.Message, text: str, state: FSMContext):
    kb = [
        [to_tasks_btn, to_notes_btn],
        [help_btn, faq_btn],
    ]
    markup = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )

    await message.answer(text, reply_markup=markup)
    await state.finish()


async def to_del_tasks_menu(message: types.Message, text: str, state: FSMContext):
    del_date_btn = KeyboardButton("Удалить все задачи на дату")
    del_date_task_btn = KeyboardButton("Удалить задачу на дату")
    del_all_btn = KeyboardButton("Удалить ВСЕ задачи")

    kb = [
        [del_date_btn, del_date_task_btn],
        [del_all_btn],
        [to_tasks_btn, to_notes_btn],
        [help_btn, faq_btn],
    ]
    markup = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )

    await message.answer(text, reply_markup=markup)
    await state.finish()
