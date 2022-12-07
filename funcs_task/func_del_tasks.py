from TelegramBOTSQLite3.checkers import *


@dp.message_handler(regexp="Удалить все задачи на дату")
async def del_date(message: types.Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        all_tasks = "SELECT * FROM `tasks` WHERE `tasks`.`user_id` = ?"
        rows = cursor.execute(all_tasks, (user_id,)).fetchall()

    except Exception as err:
        text = f"{err}\nОЙ, какая-то ошибочка,\nнапишите мне о ней: @Becenniytilt"
        await to_main_menu(message, text, state)

    else:
        if rows != ():
            kb = [
                [to_main_menu_btn],
            ]
            markup = types.ReplyKeyboardMarkup(
                keyboard=kb,
                resize_keyboard=True
            )

            text = "Введите дату задачи\nВводить дату в формате ДД.ММ.ГГГГ"
            await message.answer(text, reply_markup=markup)
            await DelTaskState.del_date_user.set()

        else:
            text = "<ошибка>\nУ вас нет никаких задач"
            await to_del_tasks_menu(message, text, state)


@dp.message_handler(state=DelTaskState.del_date_user)
async def process_del_date(message: types.Message, state: FSMContext):
    if not await check_main_menu(message, message.text, state):
        date_of_task = message.text.lower()
        if date_db := change_date(date_of_task):
            try:
                user_id = message.from_user.id
                check_tasks_date = "SELECT * FROM `tasks` WHERE `tasks`.`date` = ? AND `tasks`.`user_id` = ?"
                rows = cursor.execute(check_tasks_date, (date_db, user_id,)).fetchall()

            except Exception as err:
                text = f"{err}\nОЙ, какая-то ошибочка,\nнапишите мне о ней: @Becenniytilt"
                await to_main_menu(message, text, state)

            else:
                if rows:
                    del_tasks_date = "DELETE FROM `tasks` WHERE `tasks`.`date` = ? AND `tasks`.`user_id` = ?"
                    cursor.execute(del_tasks_date, (date_db, user_id))
                    db.commit()
                    text = f"Все ваши задачи на дату \"{date_of_task}\" успешно были удалены!"
                    await to_del_tasks_menu(message, text, state)

                else:
                    text = "<ошибка>\nУ вас нет задач на эту дату, "
                    text += "введите другую дату ДД.ММ.ГГГГ или нажмите на \"Главное меню\""
                    await message.answer(text)

        else:
            text = "<ошибка>\nВы неправильно ввели дату, введите её ещё раз ДД.ММ.ГГГГ или нажмите на \"Главное меню\""
            await message.answer(text)


@dp.message_handler(regexp="Удалить ВСЕ задачи")
async def permission_to_del(message: types.Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        all_tasks = "SELECT * FROM `tasks` WHERE `tasks`.`user_id` = ?"
        rows = cursor.execute(all_tasks, (user_id,)).fetchall()

    except Exception as err:
        text = f"{err}\nОЙ, какая-то ошибочка,\nнапишите мне о ней: @Becenniytilt"
        await to_main_menu(message, text, state)

    else:
        if rows:
            yes_btn = KeyboardButton("Да")
            no_btn = KeyboardButton("Нет")

            kb = [
                [yes_btn, no_btn],
            ]
            markup = ReplyKeyboardMarkup(
                keyboard=kb,
                resize_keyboard=True
            )

            text = "Вы действительно хотите удалить все задачи?\nИх нельзя будет восстановить!"
            await message.answer(text, reply_markup=markup)
            await DelTaskState.del_all_perm.set()

        else:
            text = "<ошибка>\nУ вас нет никаких задач"
            await message.answer(text)


@dp.message_handler(state=DelTaskState.del_all_perm)
async def process_all_del(message: types.Message, state: FSMContext):
    answer = message.text.lower()
    if answer == "да":
        try:
            user_id = message.from_user.id
            del_all_tasks = "DELETE FROM `tasks` WHERE `tasks`.`user_id` = ?"
            cursor.execute(del_all_tasks, (user_id,))
            db.commit()

        except Exception as err:
            text = f"{err}\nНу капец, тут ошибка произошла в общем, так что напишите мне о ней: @Becenniytilt"
            await to_main_menu(message, text, state)

        else:
            text = "Все ваши задачи успешно были удалены!"
            await to_main_menu(message, text, state)

    elif answer == "нет":
        text = "Вы вернулись в меню удаления"
        await to_del_tasks_menu(message, text, state)

    else:
        text = "Я не знаю что на это ответить, поэтому даю вам ещё один шанс"
        await message.answer(text)


@dp.message_handler(regexp="Удалить задачу на дату")
async def del_task(message: types.Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        all_tasks = "SELECT * FROM `tasks` WHERE `tasks`.`user_id` = ?"
        rows = cursor.execute(all_tasks, (user_id,)).fetchall()

    except Exception as err:
        text = f"{err}\nОЙ, какая-то ошибочка,\nнапишите мне о ней: @Becenniytilt"
        await to_main_menu(message, text, state)

    else:
        if rows != ():
            kb = [
                [to_main_menu_btn],
            ]
            markup = ReplyKeyboardMarkup(
                keyboard=kb,
                resize_keyboard=True
            )

            text = "Введите дату задачи вводить дату в формате ДД.ММ.ГГГГ"
            await message.answer(text, reply_markup=markup)
            await DelTaskState.get_date_user.set()

        else:
            text = "<ошибка>\nУ вас нет никаких задач"
            await to_del_tasks_menu(message, text, state)


@dp.message_handler(state=DelTaskState.get_date_user)
async def process_get_date_of_task(message: types.Message, state: FSMContext):
    date_of_task = message.text

    if not await check_main_menu(message, date_of_task, state):
        if date_db := change_date(date_of_task):
            try:
                user_id = message.from_user.id
                check_tasks_date = "SELECT * FROM `tasks` WHERE `tasks`.`date` = ? AND `tasks`.`user_id` = ? "
                check_tasks_date += "ORDER BY `tasks`.`task`"
                rows = cursor.execute(check_tasks_date, (date_db, user_id)).fetchall()

            except Exception as err:
                text = f"{err}\nОЙ, какая-то ошибочка, напишите мне о ней: @Becenniytilt"
                await to_main_menu(message, text, state)

            else:
                if rows:
                    date_tmp = rows[0][1].split("-")
                    date_txt = "{}.{}.{}".format(date_tmp[2], date_tmp[1], date_tmp[0])
                    text = f"{date_txt}\n"
                    for row in rows:
                        text += f"\t{row[2]} {row[3]}\n"
                    text += "\nТеперь выберите номер задачи, которую вы хотите удалить"
                    await state.update_data(get_date_user=date_of_task)
                    await message.answer(text)
                    await DelTaskState.get_number_user.set()

                else:
                    text = "<ошибка>\nУ вас нет никаких задач, введите другую дату "
                    text += "ДД.ММ.ГГГГ или нажмите на \"Главное меню\""
                    await message.answer(text)

        else:
            text = "<ошибка>\nВы неправильно ввели дату, введите её ещё раз ДД.ММ.ГГГГ или нажмите на \"Главное меню\""
            await message.answer(text)


@dp.message_handler(state=DelTaskState.get_number_user)
async def process_get_number_of_task(message: types.Message, state: FSMContext):
    number_of_task = message.text
    data = await state.get_data()
    date_db = change_date(data["get_date_user"])

    if not await check_main_menu(message, number_of_task, state):
        if number_of_task.isdigit():
            try:
                user_id = message.from_user.id
                number_db = f"%{number_of_task}%"

                select_task = "SELECT * FROM `tasks` "
                select_task += "WHERE `tasks`.`date` = ? AND `tasks`.`user_id` = ? AND `tasks`.`task` LIKE ?"
                task_db = cursor.execute(select_task, (date_db, user_id, number_db)).fetchall()

                delete_task = "DELETE FROM `tasks` "
                delete_task += "WHERE `tasks`.`date` = ? AND `tasks`.`user_id` = ? AND `tasks`.`task` LIKE ?"
                cursor.execute(delete_task, (date_db, user_id, number_db))
                db.commit()

                select_tasks_number = "SELECT * FROM `tasks` WHERE `tasks`.`date` = ? AND `tasks`.`user_id` = ?"
                select_tasks = cursor.execute(select_tasks_number, (date_db, user_id)).fetchall()

            except sqlite3.OperationalError as err:
                text = f"{err}\nОшибка с запросом в БД, напишите мне о ней: @Becenniytilt"
                await to_main_menu(message, text, state)

            except Exception as err:
                text = f"{err.__context__}\nОЙ, какая-то ошибочка, напишите мне о ней: @Becenniytilt"
                await to_main_menu(message, text, state)

            else:
                if task_db:
                    task_number = 1
                    task_show = task_db[0][2][6:]
                    for task in select_tasks:
                        task_number_db = f"%{task[2].split()[0]}%"
                        task_list = task[2].split()
                        task_list[0] = str(task_number)
                        task_to_db = "{} ".format(task_list[0]) + " ".join(map(str, task_list[1:]))

                        try:
                            upd_task = "UPDATE `tasks` SET `task` = ? "
                            upd_task += "WHERE `tasks`.`date` = ? AND `tasks`.`user_id` = ? AND `tasks`.`task` LIKE ?"
                            cursor.execute(upd_task, (task_to_db, date_db, user_id, task_number_db))
                            db.commit()

                        except Exception as err:
                            text = f"{err}\nПроизошла ошибка, напишите мне о ней: @Becenniytilt"
                            await to_main_menu(message, text, state)
                            break

                        else:
                            task_number += 1
                    text = f"Задача \"{task_show}\" успешно удалена!"
                    await to_del_tasks_menu(message, text, state)

                else:
                    text = "У вас нет задачи с таким номером, введите другой номер или нажмите на \"Главное меню\""
                    await message.answer(text)

        else:
            text = "<ошибка>\nВы ввели не цифру, введите номер ещё раз или нажмите на \"Главное меню\""
            await message.answer(text)
