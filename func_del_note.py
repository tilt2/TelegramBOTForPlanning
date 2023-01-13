from checkers import *
from utils import DelNoteState


@dp.message_handler(regexp="Удалить заметку")
async def del_note(message: types.Message):
    kb = [
        [to_main_menu_btn],
    ]
    markup = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )

    text = "Введите номер заметки"
    await message.answer(text, reply_markup=markup)
    await DelNoteState.get_number.set()


@dp.message_handler(state=DelNoteState.get_number)
async def process_get_number_of_note(message: types.Message, state: FSMContext):
    number_of_note = message.text

    if not await check_main_menu(message, message.text, state):
        if number_of_note.isdigit():
            try:
                user_id = message.from_user.id
                number_db = f"%{number_of_note}%"

                select_note = "SELECT * FROM `notes` WHERE `notes`.`user_id` = ? AND `notes`.`note_id` LIKE ?"
                notes_db = cursor.execute(select_note, (user_id, number_db)).fetchall()

                delete_note = "DELETE FROM `notes` WHERE `notes`.`user_id` = ? AND `notes`.`note_id` LIKE ?"
                cursor.execute(delete_note, (user_id, number_db))
                db.commit()

                select_notes_number = "SELECT * FROM `notes` WHERE `notes`.`user_id` = ?"
                select_notes = cursor.execute(select_notes_number, (user_id,)).fetchall()

            except Exception as err:
                text = f"{err}\nОй, какая-то ошибочка, напишите мне о ней: @Becenniytilt"
                await to_main_menu(message, text)
                await state.finish()

            else:
                if notes_db:
                    note_number = 1
                    note_show: list[str] = notes_db[0][2].split()

                    for note in select_notes:
                        note_number_db = note[1]
                        note_id_to_db = str(note_number)

                        try:
                            upd_note_id = "UPDATE `notes` SET `note_id` = ? "
                            upd_note_id += "WHERE `notes`.`user_id` = ? AND `notes`.`note_id` LIKE ?"
                            cursor.execute(upd_note_id, (note_id_to_db, user_id, note_number_db))
                            db.commit()

                        except Exception as err:
                            text = f"{err}\nПроизошла ошибка, напишите мне о ней: @Becenniytilt"
                            await to_main_menu(message, text)
                            await state.finish()
                            break

                        else:
                            note_number += 1

                    if len(note_show) >= 4:
                        text = f"Ваша заметка \"{note_show[0]} {note_show[1]} {note_show[2]}...\" успешно удалена"

                    else:
                        if len(note_show[0]) < 10:
                            text = f"Ваша заметка \"{note_show[0]}\" успешно удалена"

                        else:
                            text = f"Ваша заметка \"{note_show[0][0:8]}...\" успешно удалена"

                    await to_main_menu(message, text)
                    await state.finish()

                else:
                    text = "У вас нет задачи с таким номером, введите другой номер или нажмите на \"Главное меню\""
                    await message.answer(text)

        else:
            text = "<ошибка>\nВы ввели не цифру, введите номер заметки ещё раз или нажмите на \"Главное меню\""
            await message.answer(text)


@dp.message_handler(regexp="Удалить ВСЕ заметки")
async def del_all(message: types.Message):
    try:
        user_id = message.from_user.id
        all_tasks = "SELECT * FROM `notes` WHERE `notes`.`user_id` = ?"
        rows = cursor.execute(all_tasks, (user_id,)).fetchall()

    except Exception as err:
        text = f"{err}\nОЙ, какая-то ошибочка, напишите мне о ней: @Becenniytilt"
        await to_main_menu(message, text)

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

            text = "Вы действительно хотите удалить все заметки?\nИх нельзя будет восстановить!"
            await message.answer(text, reply_markup=markup)
            await DelNoteState.del_all_notes_perm.set()

        else:
            text = "<ошибка>\nУ вас нет никаких заметок"
            await message.answer(text)


@dp.message_handler(state=DelNoteState.del_all_notes_perm)
async def perm_all_del_notes(message: types.Message, state: FSMContext):
    answer = message.text.lower()

    if answer == "да":
        try:
            user_id = message.from_user.id
            del_all_notes = "DELETE FROM `notes` WHERE `notes`.`user_id` = ?"
            cursor.execute(del_all_notes, (user_id,))
            db.commit()

        except Exception as err:
            text = f"{err}\nНу капец, тут ошибка короче, поэтому напишите мне о ней: @Becenniytilt"
            await to_main_menu(message, text)
            await state.finish()

        else:
            text = "Все ваши заметки успешно были удалены"
            await to_main_menu(message, text)
            await state.finish()

    elif answer == "нет":
        text = "Хорошо, не буду удалять ваши значимые заметки"
        await message.answer(text)
        await state.finish()

    else:
        text = "Я не знаю что на это ответить, поэтому даю вам еще один шанс"
        await message.answer(text)
