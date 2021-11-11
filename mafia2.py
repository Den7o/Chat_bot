import telebot
import random
from config import TOKEN
import time
from telebot import types
import my_redis




bot = telebot.TeleBot(token=TOKEN)


# ------------Функции для мафии ботa----------------------
def send_message_for_players(text):
    bot.send_message(my_redis.get_id(), text)



#---------------------------------------------------------

@bot.message_handler(commands=['game'])
def start_game(message):
    if message.chat.id == "private":
        markup = types.InlineKeyboardMarkup(row_width=2)
        button1 = types.InlineKeyboardButton('✅Готово', callback_data='ready')
        markup.add(button1)
        edit_message = bot.send_message(message.chat.id, "Пожалуйста добавьте меня в группу!", reply_markup=markup)
    else:
        markup = types.InlineKeyboardMarkup(row_width=2)
        button1 = types.InlineKeyboardButton('🎲 Присоединиться!',url='https://t.me/thebest_chat_bot')
        markup.add(button1)
        place = message.chat # сдесь храниться json группы(id и название группы)
        bot.send_message(place.id, f"Пользователь {message.json['from']['first_name']} начал игру!\n\nЧобы присоединиться в игру нажмите кнопку!", reply_markup=markup)

bot.polling(none_stop=True)   
