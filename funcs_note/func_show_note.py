from TelegramBOTSQLite3.checkers import *


@dp.message_handler(regexp="Показать все заметки")
async def show_notes(message: types.Message):
    user_id = message.from_user.id

    try:
        select_notes = "SELECT * FROM `notes` WHERE `notes`.`user_id` = ?"
        cursor.execute(select_notes, (user_id,))

    except Exception as err:
        text = f"{err}\nОЙ, какая-то ошибочка, напишите мне о ней: @Becenniytilt"
        await to_main_menu(message, text)

    else:
        if select_notes:
            text = "Все ваши заметки\n\n"
            for note in select_notes:
                text += f"\n{note[1]} — {note[2]}\n"
            await message.answer(text)

        else:
            text = "<ошибка>\nУ вас нет никаких заметок"
            await message.answer(text)
