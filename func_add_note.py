from checkers import *
from utils import AddNoteState


@dp.message_handler(regexp="Добавить заметку")
async def add_note(message: types.Message):
    kb = [
        [to_main_menu_btn],
    ]
    markup = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )

    text = "Напишите заметку"
    await message.answer(text, reply_markup=markup)
    await AddNoteState.add_note.set()


@dp.message_handler(state=AddNoteState.add_note)
async def process_add_note(message: types.Message, state: FSMContext):
    if not await check_main_menu(message, message.text, state):
        note = message.text
        user_id = message.from_user.id

        if 10 <= (length_note := len(note)) <= 200:
            try:
                check_notes = "SELECT * FROM `notes` WHERE `notes`.`user_id` = ? ORDER BY `notes`.`note`"
                rows = cursor.execute(check_notes, (user_id,))

            except Exception as err:
                text = f"{err}\nОЙ, какая-то ошибочка, напишите мне о ней: @Becenniytilt"
                await to_main_menu(message, text)
                await state.finish()

            else:
                note_id_db = 1
                if rows:
                    for row in rows:
                        task_number = row[1]
                        if task_number == note_id_db:
                            note_id_db += 1
                        else:
                            break

                add_note_query = "INSERT INTO `notes` VALUES (?, ?, ?)"
                cursor.execute(add_note_query, (user_id, note_id_db, note))
                db.commit()

                words_note = note.split()
                if len(words_note) >= 4:
                    text = f"Ваша заметка \"{words_note[0]} {words_note[1]} {words_note[2]}"
                    text += f"...\" под номером \"{note_id_db}\" успешно добавлена"

                else:
                    if len(words_note[0]) < 10:
                        text = f"Ваша заметка \"{words_note[0]}\" под номером \"{note_id_db}\" успешно добавлена"

                    else:
                        text = f"Ваша заметка \"{words_note[0][0:8]}...\" "
                        text += f"под номером \"{note_id_db}\" успешно добавлена"

                await to_main_menu(message, text)
                await state.finish()

        elif length_note > 200:
            text = "Ваша заметка слишком длинная!\nВведите её ещё раз"
            await message.answer(text)

        elif length_note < 10:
            text = "Ваша заметка слишком короткая!\nВведите её ещё раз"
            await message.answer(text)
