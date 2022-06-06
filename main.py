import telebot
from telebot import types
import menubot
from menubot import Menu
import fun

bot = telebot.TeleBot('5383683068:AAHCwuMUCfzSexVdIKrRCvxHT4mgOhOj_Pc')

@bot.message_handler(commands="start")
def command(message):
    chat_id = message.chat.id
    #bot.send_sticker(chat_id, "CAACAgIAAxkBAAIaeWJEeEmCvnsIzz36cM0oHU96QOn7AAJUAANBtVYMarf4xwiNAfojBA") узнать как получить код стикера
    txt_message = f"Привет, {message.from_user.first_name}! Меня зовут Денли. Желаю приятно провести время)"
    bot.send_message(chat_id, text=txt_message, reply_markup=Menu.getMenu(chat_id, "Главное меню").markup)

@bot.message_handler(content_types=['sticker'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    sticker = message.sticker
    bot.send_message(message.chat.id, sticker)

@bot.message_handler(content_types=['audio'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    audio = message.audio
    bot.send_message(message.chat.id, audio)

@bot.message_handler(content_types=['voice'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    voice = message.voice
    bot.send_message(message.chat.id, voice)

@bot.message_handler(content_types=['photo'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    photo = message.photo
    bot.send_message(message.chat.id, photo)

@bot.message_handler(content_types=['video'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    video = message.video
    bot.send_message(message.chat.id, video)

@bot.message_handler(content_types=['document'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    document = message.document
    bot.send_message(message.chat.id, document)
    if message.document.mime_type == "video/mp4":
        bot.send_message(message.chat.id, "Это GIF")

@bot.message_handler(content_types=['contact'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    contact = message.contact
    bot.send_message(message.chat.id, contact)

@bot.message_handler(content_types=['text'])
def get_messages(message):
    chat_id = message.chat.id
    ms_text = message.text

    cur_user = menubot.Users.getUser(chat_id)
    if cur_user is None:
        cur_user = menubot.Users(chat_id, message.json["from"])

    subMenu = menubot.goto_menu(bot, chat_id, ms_text)
    if subMenu is not None:
        return
    
    cur_menu = Menu.getCurMenu(chat_id)
    if cur_menu is not None and ms_text in cur_menu.buttons:
        module = cur_menu.module

        if module != "":
            exec(module + ".get_text_messages(bot, cur_user, message)")

        if ms_text == "Игровой бот":
            game_bot(bot, chat_id)

        if ms_text == "Помощь":
            send_help(bot, chat_id)

    else:
        bot.send_message(chat_id, text="Сорян, но я не понял это: " + ms_text)
        menubot.goto_menu(bot, chat_id, "Главное меню")

def game_bot(bot, chat_id):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Нажми на меня", url = "https://t.me/ggonex_Game_bot")
    markup.add(btn1)
    img = open("D:/ggonex_Game.jpg", 'rb')
    bot.send_photo(chat_id, img, reply_markup=markup)

def send_help(bot, chat_id):
    bot.send_message(chat_id, "Автор: Мамаев Илья")
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Если есть вопросы, пишите автору", url= "https://t.me/@ggonex)
    markup.add(btn1)
    bot.send_photo(chat_id, img, reply_markup=markup)

    bot.send_message(chat_id, "Наши активные ребята:")
    for el in menubot.Users.activeUsers:
        bot.send_message(chat_id, menubot.Users.activeUsers[el].getUserHTML(), parse_mode='HTML')

bot.polling(none_stop=True, interval=0)