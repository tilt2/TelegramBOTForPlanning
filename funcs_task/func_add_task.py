from TelegramBOTSQLite3.checkers import *
from TelegramBOTSQLite3.utils import AddTaskState


@dp.message_handler(regexp="Добавить задачу")
async def add_task(message: types.Message):
    kb = [
        [to_main_menu_btn],
    ]
    markup = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )

    text = "Вводить дату в формате\nДД.ММ.ГГГГ"
    await message.answer(text, reply_markup=markup)
    await AddTaskState.date_user.set()


@dp.message_handler(state=AddTaskState.date_user)
async def process_add_date(message: types.Message, state: FSMContext):
    if not await check_main_menu(message, message.text, state):
        date_user = message.text.lower()
        if change_date(date_user):
            text = "Теперь введите задачу"

            await state.update_data(date_user=date_user)
            await message.answer(text)
            await AddTaskState.task.set()

        else:
            text = "<ошибка>\nВы неправильно ввели дату, введите её ещё раз ДД.ММ.ГГГГ или нажмите на \"Главное меню\""
            await message.answer(text)


@dp.message_handler(state=AddTaskState.task)
async def process_add_task(message: types.Message, state: FSMContext):
    task = message.text

    if not await check_main_menu(message, message.text, state):
        if 3 <= len(task) <= 50:
            text = "Теперь введите категорию\nНапишите минус, чтобы не добавлять категорию"

            await state.update_data(task=task)
            await message.answer(text)
            await AddTaskState.category.set()

        elif len(task) > 50:
            text = "<ошибка>\nЗадача слишком большая для добавления, введите задачу ещё раз"
            await message.answer(text)

        else:
            text = "<ошибка>\nВ ведённой вами задачи меньше 3-х символов, введите задачу ещё раз"
            await message.answer(text)


@dp.message_handler(state=AddTaskState.category)
async def process_add_category(message: types.Message, state: FSMContext):
    category = message.text.lower()
    user_id = message.from_user.id
    data = await state.get_data()
    date_user = data["date_user"]
    task = data["task"]
    date_db = change_date(date_user)

    if category != "-":
        if not await check_main_menu(message, message.text, state):
            if 3 <= len(category) <= 32:
                try:
                    check_tasks_date = "SELECT * FROM `tasks`"
                    check_tasks_date += "WHERE `tasks`.`user_id` = ? AND `tasks`.`date` = ? ORDER BY `tasks`.`task`"
                    rows = cursor.execute(check_tasks_date, (user_id, date_db)).fetchall()

                except Exception as err:
                    text = f"{err}\nОЙ, какая-то ошибочка, напишите мне о ней: @Becenniytilt"
                    await to_main_menu(message, text)
                    await state.finish()

                else:
                    counter = 1
                    if rows != ():
                        for row in rows:
                            task_number = int(row[2].split()[0])
                            if task_number == counter:
                                counter += 1
                            else:
                                break
                    task_db = f"{counter} — {task}"
                    category_db = f"#{category.replace(' ', '_')}"

                    ins_task_with_category = "INSERT INTO `tasks` VALUES (?, ?, ?, ?)"
                    cursor.execute(ins_task_with_category, (user_id, date_db, task_db, category_db))
                    db.commit()

                    text = f"Задача \"{task}\" на дату \"{date_user}\" с категорией \"{category}\" успешно добавлена!"
                    await to_main_menu(message, text)
                    await state.finish()

            elif len(category) > 32:
                text = "Категория слишком длинная, попробуйте сократить её\nНапишите категорию ещё раз"
                await message.answer(text)

            else:
                text = "Категория слишком маленькая!\nНапишите категорию ещё раз"
                await message.answer(text)

    else:
        try:
            check_tasks_date = "SELECT * FROM `tasks` WHERE `tasks`.`user_id` = ? AND `tasks`.`date` = ? "
            check_tasks_date += "ORDER BY `tasks`.`task`"
            rows = cursor.execute(check_tasks_date, (user_id, date_db)).fetchall()

        except Exception as err:
            text = f"{err}\nОЙ, какая-то ошибочка,\nнапишите мне о ней: @Becenniytilt"
            await to_main_menu(message, text)
            await state.finish()

        else:
            counter = 1
            if rows != ():
                for row in rows:
                    task_number = int(row[2].split()[0])
                    if task_number == counter:
                        counter += 1

                    else:
                        break

            task_db = f"{counter} — {task}"
            category_db = ""

            ins_task_without_category = "INSERT INTO `tasks` VALUES (?, ?, ?, ?)"
            cursor.execute(ins_task_without_category, (user_id, date_db, task_db, category_db))
            db.commit()

            text = f"Задача \"{task}\" на дату \"{date_user}\" успешно добавлена!"
            await to_main_menu(message, text)
            await state.finish()
