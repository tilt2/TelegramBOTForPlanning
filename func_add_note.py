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
                await to_main_menu(message, text, state)

            else:
                number = 1
                if rows:
                    for row in rows:
                        task_number = int(row[1].split()[0])
                        if task_number == number:
                            number += 1
                        else:
                            break
                note_db = f"{number} — {note}"

                add_note_query = "INSERT INTO `notes` VALUES (?, ?)"
                cursor.execute(add_note_query, (user_id, note_db,))
                db.commit()

                text = f"Ваша заметка под номером \"{number}\" успешно добавлена"
                await to_main_menu(message, text, state)

        elif length_note > 200:
            text = "Ваша заметка слишком длинная!\nВведите её ещё раз"
            await message.answer(text)

        elif length_note < 10:
            text = "Ваша заметка слишком короткая!\nВведите её ещё раз"
            await message.answer(text)
