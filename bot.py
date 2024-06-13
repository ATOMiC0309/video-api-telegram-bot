from telebot import TeleBot
from telebot.types import Message, CallbackQuery
from inlinebuttons import main_menu, create_menu, delete_content
import requests

BOT_TOKEN = "6575786579:AAFbe_G-C5ObaC55OoMh-k2SgX9MQ_Wb_WI"

bot = TeleBot(BOT_TOKEN, parse_mode="HTML")


def get_response(url):
    headers = {
        "authorization": "Token 5de07e91beddce8d2edaa36d769b1516abb4d160"
    }
    res = requests.get(url, headers=headers).json()
    return res


@bot.message_handler(commands=['start'])
def start(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, f"Salom, <b>{message.from_user.full_name}</b> botga xush kelibsiz!",
                     reply_to_message_id=message.message_id)
    bot.send_message(chat_id, "Kerakli bo'limni tanlang:", reply_markup=main_menu())


@bot.callback_query_handler(func=lambda call: call.data)
def menu(call: CallbackQuery):
    chat_id = call.message.chat.id
    query = []
    message_id = call.message.message_id
    if call.data == "main_menu":
        bot.edit_message_text("Kerakli bo'limni tanlang:", chat_id, message_id, reply_markup=main_menu())

    elif call.data == "videos":
        query += [("all-videos", "Barcha videolar"), ("category-video", "Kategoriya bo'yicha videolar")]
        bot.edit_message_text("Videolar menyusi:", chat_id, message_id, reply_markup=create_menu(iterable=query,
                                                                                                 back_to="main_menu",
                                                                                                 key_word="video-menu"))

    elif call.data == "categories":
        res = get_response('http://127.0.0.1:8000/video-api/category/')
        try:
            for category in res:
                query.append((category.get('id', 1), category.get('name', "Hech nima yo'q")))
        except:
            query.append((1, "Hech nima yo'q."))
        bot.edit_message_text("Kategoriyalar:", chat_id, message_id, reply_markup=create_menu(iterable=query,
                                                                                              back_to="main_menu",
                                                                                              key_word="category"))
    elif call.data.split('_')[1] == "category-video":
        res = get_response('http://127.0.0.1:8000/video-api/category/')
        try:
            for category in res:
                query.append((category.get('id', 1), category.get('name', "Hech nima yo'q")))
        except:
            query.append((1, "Hech nima yo'q."))
        bot.edit_message_text("Kategoriyalar:", chat_id, message_id, reply_markup=create_menu(iterable=query,
                                                                                              back_to="videos",
                                                                                              key_word="category"))

    elif call.data.split('_')[1] == "all-videos":
        res = get_response('http://127.0.0.1:8000/video-api/video/')
        try:
            for video in res:
                query.append((video.get('id', 1), video.get('title', "Hech nima yo'q")))
        except:
            query.append((1, "Hech nima yo'q."))
        bot.edit_message_text("Videolar:", chat_id, message_id, reply_markup=create_menu(iterable=query,
                                                                                         back_to="videos",
                                                                                         key_word="video"))

    elif call.data.split('_')[0] == 'video':
        res = get_response(f'http://127.0.0.1:8000/video-api/video/{call.data.split('_')[1]}')
        title = res.get('title', "Yo'q")
        description = res.get('description', "Yo'q")

        content_url = res.get('video_content', "Yo'q")
        print(res)

        file_res = requests.get(content_url)
        file_extension = content_url.split('.')[-1]
        file_path = f"{chat_id}.{file_extension}"
        with open(file_path, 'wb') as file:
            file.write(file_res.content)

        category = res.get('category', "Yo'q")
        category = get_response(f'http://127.0.0.1:8000/video-api/category/{category}').get('name', "Yo'q")
        with open(file_path, 'rb') as file:
            bot.delete_message(chat_id, message_id)
            ms = bot.send_message(chat_id, "Biroz kuting...")
            msg = bot.send_document(chat_id=chat_id, document=file,
                                    caption=f"<b>Sarlavha:</b>   <i>{title}</i>\n\n"
                                            f"<b>Tavsif:</b>     <i>{description}</i>\n\n"
                                            f"<b>Kategoriya:</b> <i>{category}</i>",

                                    )
            bot.edit_message_reply_markup(chat_id=chat_id, message_id=msg.message_id,
                                          reply_markup=delete_content(msg.message_id))
            bot.send_message(chat_id, "Kerakli bo'limni tanlang:", reply_markup=main_menu())
            bot.delete_message(chat_id, ms.message_id)

    elif call.data.split('_')[0] == 'category':
        res = get_response(f'http://127.0.0.1:8000/video-api/video/by-category/{call.data.split('_')[1]}/')
        try:
            for video in res:
                query.append((video.get('id', 1), video.get('title', "Hech nima yo'q")))
        except:
            query.append((1, "Hech nima yo'q."))
        bot.edit_message_text("Videolar:", chat_id, message_id, reply_markup=create_menu(iterable=query,
                                                                                         back_to="videos",
                                                                                         key_word="video"))

    elif call.data.split('_')[0] == "delete":
        bot.delete_message(chat_id, message_id=call.data.split('_')[1])


bot.infinity_polling()
