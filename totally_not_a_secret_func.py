from config import bot
from checkers import to_main_menu_btns
import time
import random


def do_scale_heart(message, message_id, interval):
    for t in range(8, 0, -1):
        text = ""
        for i in range(t):
            for j in range(t):
                text += "❤"
            text += "\n"
        bot.edit_message_text(text[:-1], message.chat.id, message_id)
        time.sleep(interval)


def do_fil_heart(message, message_id, interval, text):
    text = list(text)
    for t in range(1, len(text) - 1, 3):
        res = ""
        if text[t - 1] != "\n":
            text[t - 1] = "❤"
        if text[t] != "\n":
            text[t] = "❤"
        if text[t + 1] != "\n":
            text[t + 1] = "❤"
        for i in text:
            res += i
        bot.edit_message_text(res, message.chat.id, message_id)
        time.sleep(interval)


def do_random_heart():
    text = ""
    list_of_hearts = ["🧡", "❤", "💛", "💚", "💙", "💜",
                      "🖤", "🤎"]
    for i in range(9):
        for j in range(9):
            if i in [0, 8]:
                text += "🤍"
            elif i == 1:
                if j in [0, 1, 4, 7, 8]:
                    text += "🤍"
                else:
                    text += random.choice(list_of_hearts)
            elif i in [2, 3, 4]:
                if j in [0, 8]:
                    text += "🤍"
                else:
                    text += random.choice(list_of_hearts)
            elif i == 5:
                if j in [0, 1, 7, 8]:
                    text += "🤍"
                else:
                    text += random.choice(list_of_hearts)
            elif i == 6:
                if j in [3, 4, 5]:
                    text += random.choice(list_of_hearts)
                else:
                    text += "🤍"
            elif i == 7:
                if j == 4:
                    text += random.choice(list_of_hearts)
                else:
                    text += "🤍"
            else:
                text += random.choice(list_of_hearts)
        text += "\n"
    return text


def do_heart():
    text = ""
    for i in range(9):
        for j in range(9):
            if i in [0, 8]:
                text += "🤍"
            elif i == 1:
                if j in [0, 1, 4, 7, 8]:
                    text += "🤍"
                else:
                    text += "❤"
            elif i in [2, 3, 4]:
                if j in [0, 8]:
                    text += "🤍"
                else:
                    text += "❤"
            elif i == 5:
                if j in [0, 1, 7, 8]:
                    text += "🤍"
                else:
                    text += "❤"
            elif i == 6:
                if j in [3, 4, 5]:
                    text += "❤"
                else:
                    text += "🤍"
            elif i == 7:
                if j == 4:
                    text += "❤"
                else:
                    text += "🤍"
            else:
                text += "❤"
        text += "\n"
    return text


@bot.message_handler(regexp="Дарина")
def lovely_message(message):
    interval = 0.2
    text = do_heart()
    message_id = bot.send_message(message.chat.id, text).id
    for i in range(9):
        time.sleep(interval)
        text = do_random_heart()
        bot.edit_message_text(text, message.chat.id, message_id)
    time.sleep(interval)
    do_fil_heart(message, message_id, interval, text)
    time.sleep(interval)
    do_scale_heart(message, message_id, interval)
    time.sleep(0.5)
    text = "Солнышко, ты самое прекрасное, что у меня есть\nЯ тебя очень-очень сильно люблю, с 1-ой Годовщиной, "
    text += "уверен, что это не последний год вместе❤❤❤"
    text += "\n\nПрости, пожалуйста, что вот так плохо получилось с поздравлением, я полный еблан, "
    text += "но я думаю о тебе постоянно и эту функцию я написал до твоего ДР, так что я написал этот код только потому"
    text += ", что люблю тебя и хотел сделать тебе приятное"
    to_main_menu_btns(message, text)
