from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("Kategporiyalar", callback_data="categories"),
        InlineKeyboardButton("Videolar", callback_data="videos"),
    )

    return markup


def create_menu(iterable, back_to, key_word):
    markup = InlineKeyboardMarkup(row_width=1)
    btns = []
    for btn in iterable:
        btns.append(
            InlineKeyboardButton(btn[1], callback_data=f"{key_word}_{btn[0]}")
        )
    markup.add(*btns)
    markup.add(
        InlineKeyboardButton("Orqaga", callback_data=back_to)
    )

    return markup


def delete_content(message_id):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("O'chirish❌", callback_data=f"delete_{message_id}")
    )
    return markup
