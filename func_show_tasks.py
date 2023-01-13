from checkers import *
from utils import ShowTaskState


@dp.message_handler(regexp="Показать все задачи")
async def show_all(message: types.Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        all_dates = "SELECT DISTINCT `tasks`.`date` FROM `tasks` WHERE `tasks`.`user_id` = ? ORDER BY `tasks`.`date`"
        rows_dates = cursor.execute(all_dates, (user_id,)).fetchall()

    except Exception as err:
        text = f"{err}\nОЙ, какая-то ошибочка, напишите мне о ней: @Becenniytilt"
        await to_main_menu(message, text)
        await state.finish()

    else:
        if rows_dates:
            text = ''
            
            for row_date in rows_dates:
                date_db = list(row_date)[0]
                show_all_date = "SELECT * FROM `tasks` "
                show_all_date += "WHERE `tasks`.`user_id` = ? AND `tasks`.`date` = ? ORDER BY `tasks`.`task`"
                rows_tasks_date = cursor.execute(show_all_date, (user_id, date_db)).fetchall()

                date_tmp = rows_tasks_date[0][1].split("-")
                date_txt = "{}.{}.{}".format(date_tmp[2], date_tmp[1], date_tmp[0])
                text += f"{date_txt}\n"
                for task in rows_tasks_date:
                    text += f"\t{task[2]} {task[3]}\n"
                text += "\n"

            await message.answer(text)
            await state.finish()

        else:
            text = "<ошибка>\nУ вас нет никаких задач"
            await message.answer(text)
            await state.finish()


@dp.message_handler(regexp="Показать задачи на дату")
async def show_date(message: types.Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        select_all_rows_query = f"SELECT * FROM `tasks` WHERE `tasks`.`user_id` = ?"
        date_tasks = cursor.execute(select_all_rows_query, (user_id,)).fetchall()

    except Exception as err:
        text = f"{err}\nОЙ, какая-то ошибочка, напишите мне о ней: @Becenniytilt"
        await to_main_menu(message, text)
        await state.finish()

    else:
        if date_tasks:
            kb = [
                [to_main_menu_btn],
            ]
            markup = ReplyKeyboardMarkup(
                keyboard=kb,
                resize_keyboard=True
            )

            text = "Введите дату задачи\nВводить дату в формате\nДД.ММ.ГГГГ"
            await message.answer(text, reply_markup=markup)
            await ShowTaskState.date_show_user.set()

        else:
            text = "<ошибка>\nУ вас нет никаких задач"
            await to_main_menu(message, text)
            await state.finish()


@dp.message_handler(state=ShowTaskState.date_show_user)
async def process_show_date(message: types.Message, state: FSMContext):
    if not await check_main_menu(message, message.text, state):
        date_of_task = message.text.lower()
        if date_db := change_date(date_of_task):
            try:
                user_id = message.from_user.id
                show_date_tasks = "SELECT * FROM `tasks` WHERE `tasks`.`user_id` = ? AND `tasks`.`date` = ? "
                show_date_tasks += "ORDER BY `tasks`.`task`"
                rows = cursor.execute(show_date_tasks, (user_id, date_db)).fetchall()

            except Exception as err:
                text = f"{err}\nОЙ, какая-то ошибочка, напишите мне о ней: @Becenniytilt"
                await to_main_menu(message, text)
                await state.finish()

            else:
                if rows:
                    date_tmp = rows[0][1].split("-")
                    date_txt = "{}.{}.{}".format(date_tmp[2], date_tmp[1], date_tmp[0])
                    text = f"{date_txt}\n"
                    for row in rows:
                        text += f"\t{row[2]} {row[3]}\n"
                    await to_main_menu(message, text)
                    await state.finish()

                else:
                    text = "<ошибка>\nУ вас нет задач на эту дату, "
                    text += "введите другую дату ДД.ММ.ГГГГ или нажмите на \"Главное меню\""
                    await message.answer(text)

        else:
            text = "<ошибка>\nВы неправильно ввели дату, введите "
            text += "её ещё раз ДД.ММ.ГГГГ или нажмите на \"Главное меню\""
            await message.answer(text)
