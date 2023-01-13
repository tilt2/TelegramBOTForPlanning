from apscheduler.schedulers.asyncio import AsyncIOScheduler
import func_add_task, func_show_tasks, func_del_tasks
import func_add_note, func_show_notes, func_del_note
from checkers import *


async def task_reminder_on_action(message: types.Message, user_id: int, date_db: str):
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


async def task_reminder_creator(message: types.Message):
    date_db = change_date("сегодня")
    user_id = message.from_user.id
    await task_reminder_on_action(message, user_id, date_db)


async def ny_reminder_on_action(message: types.Message):
    text = "С Новым годом, роднулечка! " \
           "Надеюсь, что в этом году тебе помог данный телеграм-бот для выполнения и планирования своих целей! " \
           "Удачи тебе в этом году и желаю тебе всего самого наилучшего!"
    await message.answer(text)


async def ny_reminder_creator(message: types.Message):
    await ny_reminder_on_action(message)

async def test(message: types.Message):
    text = "Не забудьте позавтракать, ведь это самый главный прием пищи!"
    await message.answer(text)


async def run_daemon(message: types.Message):
    scheduler = AsyncIOScheduler()

    scheduler.add_job(
        task_reminder_creator, "cron", args=([message]),
        hour=7, minute=0, misfire_grace_time=90
    )

    scheduler.add_job(
        test, "date", args=([message]),
        run_date=datetime(2023, 1, 14, 7, 15, 0)
    )

    # scheduler.add_job(
    #     ny_reminder_creator, "date", args=([message]),
    #     date=f"01.01.{datetime.now().year}", hour=0, minute=0
    # )

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
