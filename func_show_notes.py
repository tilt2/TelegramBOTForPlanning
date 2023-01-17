from checkers import *


# запускается при нажатии кнопки "Показать все заметки"
@dp.message_handler(regexp="Показать все заметки") 
# показывает все заметки пользователю
async def show_notes(message: types.Message):
    user_id = message.from_user.id

    try:
        #SQL-запрос для выбора всех заметок пользователя
        select_notes = "SELECT * FROM `notes` WHERE `notes`.`user_id` = ?"
        rows = cursor.execute(select_notes, (user_id,)).fetchall()

    except Exception as err:
        text = f"{err}\nОЙ, какая-то ошибочка, напишите мне о ней: @Becenniytilt"
        await to_main_menu(message, text)

    else:
        if select_notes:
            # Показ заметок
            text = "Все ваши заметки\n"
            for note in rows:
                text += f"\n{note[1]} — {note[2]}\n"
            await message.answer(text)

        else:
            text = "<ошибка>\nУ вас нет никаких заметок"
            await message.answer(text)
