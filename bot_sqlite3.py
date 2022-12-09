from apscheduler.schedulers.asyncio import AsyncIOScheduler

from checkers import *
from funcs_task import func_add_task, func_show_tasks, func_del_tasks
from funcs_note import func_add_note, func_show_notes, func_del_note


async def reminder_on_action(message: types.Message, user_id: int, date_db: str):
    try:
        show_date_tasks = "SELECT * FROM `tasks` WHERE `tasks`.`user_id` = ? AND `tasks`.`date` = ? "
        show_date_tasks += "ORDER BY `tasks`.`task`"
        rows = cursor.execute(show_date_tasks, (user_id, date_db)).fetchall()

    except Exception as err:
        text = f"{err}\nОЙ, какая-то ошибочка, напишите мне о ней: @Becenniytilt"
        text += "\nОшибка связана с напоминанием задач"
        await message.answer(text)

    else:
        if rows:
            text = "Ваши сегодняшние задачи:\n"
            for row in rows:
                text += f"\t{row[2]} {row[3]}\n"
            await message.answer(text)

        else:
            text = "Поздравляю!\nУ вас сегодня нет задач! :)"
            await message.answer(text)


async def reminder_creator(message: types.Message):
    date_db = change_date("сегодня")
    user_id = message.from_user.id
    await reminder_on_action(message, user_id, date_db)


async def run_daemon(message: types.Message):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(reminder_creator, "cron", args=([message]), hour=7, minute=0)
    scheduler.start()


@dp.message_handler(commands=["start"])
async def start_bot(message: types.Message):
    kb = [
        [to_tasks_btn, to_notes_btn],
        [help_btn, faq_btn],
    ]
    markup = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите в какое меню вы хотите перейти"
    )
    await message.answer(HELP_HELLO.format(message.from_user.first_name), reply_markup=markup)
    await run_daemon(message)


if __name__ == "__main__":
    executor.start_polling(
        dispatcher=dp,
        skip_updates=True
    )
