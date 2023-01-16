from checkers import *

# класс с состояниями машины состояний для функции добавление заметки в БД
from utils import AddNoteState


# бот просит написать ему текст заметки
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
    # перевод машины состояний в другое состояние для запуска следующей функции
    await AddNoteState.add_note.set()


 # бот добавляет заметку в базу данных (БД)
@dp.message_handler(state=AddNoteState.add_note)
async def process_add_note(message: types.Message, state: FSMContext):
    if not await check_main_menu(message, message.text, state):
        note = message.text
        user_id = message.from_user.id

        # проверяет количество символов заметки
        if 10 <= (length_note := len(note)) <= 200:
            try:
                # SQL-запрос на наличие других заметок пользователя в БД
                check_notes = "SELECT * FROM `notes` WHERE `notes`.`user_id` = ? ORDER BY `notes`.`note`"
                rows = cursor.execute(check_notes, (user_id,))

            except Exception as err:
                text = f"{err}\nОЙ, какая-то ошибочка, напишите мне о ней: @Becenniytilt"
                await to_main_menu(message, text)
                await state.finish()

            else:
                note_id_db = 1
                if rows:
                    # цикл для номера заметки, если у пользователя уже есть заметки в БД
                    for row in rows:
                        task_number = row[1]
                        if task_number == note_id_db:
                            note_id_db += 1
                        else:
                            break

                # SQL-запрос на добавление заметки в БД
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
                # "Очистка" машины состояний
                await state.finish()

        elif length_note > 200:
            text = "Ваша заметка слишком длинная!\nВведите её ещё раз"
            await message.answer(text)

        elif length_note < 10:
            text = "Ваша заметка слишком короткая!\nВведите её ещё раз"
            await message.answer(text)
