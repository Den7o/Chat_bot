import telebot
from telebot import types
from config import TOKEN
import random
import time

bot = telebot.TeleBot(token=TOKEN)
players = {}
black_list = []



@bot.message_handler(commands=['game'])
def game_start(message):
    if message.chat.type == "private":
        markup = types.InlineKeyboardMarkup(row_width=2)
        button1 = types.InlineKeyboardButton('✅Готово', callback_data='ready')
        markup.add(button1)
        bot.send_message(message.chat.id, "Пожалуйста добавьте меня в группу!", reply_markup=markup)
    else:
        markup = types.InlineKeyboardMarkup(row_width=2)
        button1 = types.InlineKeyboardButton('🎲 Присоединиться!', callback_data='join', url='https://t.me/thebest_chat_bot')
        markup.add(button1)
        place = message.chat
        bot.send_message(message.chat.id, f"Пользователь @{message.json['from']['username']} начал игру!\n\nЧобы присоединиться в игру нажмите кнопку!", reply_markup=markup)
        
        @bot.message_handler(commands=['start'])
        def join(message):
            if message.from_user.id not in players.keys() and message.from_user.first_name not in players.values():
                if len(players) >= 10:
                    bot.send_message(message.from_user.id, "Простите, но свободных мест уже не осталось")

                else:
                    players[message.from_user.id] = message.from_user.first_name
                    bot.send_message(message.from_user.id, f"Вы зашли с {place.title}")
                    send_message = bot.send_message(place.id, f"Набор игроков...\n\nОсталось: {10-len(players)} игроков")
                    # bot.edit_message_text(f"Присоединилось: \n\n{players}\n\nОсталось:{10-len(players)}", chat_id=message.chat.id, message_id=send_message.message_id)
            else:
                bot.send_message(message.from_user.id, "Вы уже присоединились к игре!")

            if len(players) >= 10:
                bot.send_message(place.id, "Game START!")
                for num in range(len(players)):
                    bot.send_message(tuple(players.items())[num][0], "Игра Началась!\n\n🍀Распределение ролей, подождите пожалуйста 10 секунд!")
                time.sleep(10)
                num = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
                random1 = random.choice(num)
                citizens = {}
                number = 1
                for key,value in players.items():
                    if random1 == 5:
                        num.remove(random1)
                        mafia = bot.send_message(key, "Поздравляю вы Мафия!\n Будьте осторожны и удачи в игре!")
                        mafia = {
                            "id": key,
                            "name": value,
                            "status": "alive"}
                    elif random1 == 3:
                        num.remove(random1)
                        police = bot.send_message(key, "Поздравляю вы шериф!\n Будьте внимательны и найдите мафию!")
                        police = {
                            "id": key,
                            "name": value,
                            "status": "alive"}
                    elif random1 == 9:
                        num.remove(random1)
                        doctor = bot.send_message(key, "Поздравляю вы доктор!\n Вы сможете лечить игроков пострадавших от мафии!")
                        doctor = {
                            "id": key,   
                            "name": value,
                            "status": "alive"}
                    else:
                        bot.send_message(key, "Вы мирный житель!\nНечего страшного в следующий раз повезет")
                        citizens.update({f"citizen{number}":{
                            'id': key,
                            'name': value,
                            'status': 'alive'
                        }})
                        number += 1

                for num2 in range(len(players)):
                    bot.send_message(tuple(players.items())[num2][0], "Игра началась!\nЧтобы написать другим игрокам введите в чат сообщение!")
                status = 'Day'
                while True:
                    @bot.message_handler()
                    def chat(message):
                        if status == 'Day': 
                            for num in range(1,8):                   
                                if citizens[f'citizen{num}']['status'] == 'die':
                                    bot.send_message(citizens[f'citizen{num}']['id'], "Мертвые не могут разговаривать!")
                                else:
                                    for text in range(len(players)):
                                        bot.send_message(tuple(players.items)[text][0], f"[{message.from_user.first_name}]\n{message.text}")
                            if police['status'] == 'die':
                                bot.send_message(police['id'], "Мертвые не могут разговаривать!")
                            elif doctor['status'] == 'die':
                                bot.send_message(doctor['id'], "Мертвые не могут разговаривать!")
                            elif mafia['status'] == 'die':
                                bot.send_message(mafia['id'], "Мертвые не могут разговаривать!")
                            else:
                                for text in range(len(players)):
                                    bot.send_message(tuple(players.items)[text][0], f"[{message.from_user.first_name}]\n{message.text}")
                        else:
                            bot.send_message(message.from_user.id, "Тише!\nТебя может услышать мафия!")
                    time.sleep(50)
                    for num in range(len(players)):
                        bot.send_message(tuple(players.items())[num][0], "--Ведущий--\nОсталось 50 секунд до начала ночи!")
                    time.sleep(50)
                    status = 'Night'
                    for num in range(len(players)):
                        bot.send_message(tuple(players.items())[num][0], "--Ведущий--\nГород засыпает, просыпаеться мафия")
                    #-----Мафия-----
                    markup = types.InlineKeyboardMarkup(row_width=2)
                    button1 = types.InlineKeyboardButton({citizens[f'citizen1']['name']}, callback_data='kill1')
                    button2 = types.InlineKeyboardButton({citizens[f'citizen2']['name']}, callback_data='kill2')
                    button3 = types.InlineKeyboardButton({doctor['name']}, callback_data='kill3')
                    button4 = types.InlineKeyboardButton({citizens[f'citizen3']['name']}, callback_data='kill4')
                    button5 = types.InlineKeyboardButton({citizens[f'citizen4']['name']}, callback_data='kill5')
                    button6 = types.InlineKeyboardButton({citizens[f'citizen5']['name']}, callback_data='kill6')
                    button7 = types.InlineKeyboardButton({citizens[f'citizen6']['name']}, callback_data='kill7')
                    button8 = types.InlineKeyboardButton({police['name']}, callback_data='kill8')
                    button9 = types.InlineKeyboardButton({citizens[f'citizen7']['name']}, callback_data='kill9')
                    markup.add(button1, button2, button3, button4, button5, button6, button7, button8, button9)
                    bot.send_message(mafia['id'], "Наступила ночь, кого вы хотите убить?", reply_markup=markup)
                    @bot.callback_query_handler(func=lambda call: True)
                    def killed_players(message):
                        player_list = {'kill1': citizens['citizen1'], 'kill2': citizens['citizen2'], 'kill3': doctor, 'kill4': citizens['citizen3'], 'kill5':
                        citizens['citizen4'], 'kill6': citizens['citizen5'], 'kill7': citizens['citizen6'], 'kill8': police, 'kill9': citizens['citizen7']}
                        for command, player_data in player_list.items():
                            if message.data == command:
                                bot.send_message(mafia['id'], f"Вы убили игрока: {player_data['name']}")
                                player_data['status'] = 'die'
                                bot.send_message(player_data['id'], "Упс...\nВас убила мафия!")
                                black_list.append(player_data['name'])
                    for num in range(len(players)):
                        bot.send_message(tuple(players.items())[num][0], f"--Ведущий--\nГород просыпаеться, засыпает мафия\n\nСписок убитых за ночь: \n{black_list}")
                    
                    #-----Доктор-----
                    markup = types.InlineKeyboardMarkup(row_width=2)
                    button1 = types.InlineKeyboardButton({citizens[f'citizen1']['name']}, callback_data='heal1')
                    button2 = types.InlineKeyboardButton({citizens[f'citizen2']['name']}, callback_data='heal2')
                    button3 = types.InlineKeyboardButton(mafia['name'], callback_data='heal3')
                    button4 = types.InlineKeyboardButton({citizens[f'citizen3']['name']}, callback_data='heal4')
                    button5 = types.InlineKeyboardButton({citizens[f'citizen4']['name']}, callback_data='heal5')
                    button6 = types.InlineKeyboardButton({citizens[f'citizen5']['name']}, callback_data='heal6')
                    button7 = types.InlineKeyboardButton({citizens[f'citizen6']['name']}, callback_data='heal7')
                    button8 = types.InlineKeyboardButton({police['name']}, callback_data='heal8')
                    button9 = types.InlineKeyboardButton({citizens[f'citizen7']['name']}, callback_data='heal9')
                    markup.add(button1, button2, button3, button4, button5, button6, button7, button8, button9)
                    @bot.callback_query_handler(func=lambda call: True)
                    def killed_players(message):
                        player_list = {'heal1': citizens['citizen1'], 'heal2': citizens['citizen2'], 'heal3': mafia, 'heal4': citizens['citizen3'], 'heal5':
                        citizens['citizen4'], 'heal6': citizens['citizen5'], 'heal7': citizens['citizen6'], 'heal8': police, 'heal9': citizens['citizen7']}
                        for command, player_data in player_list.items():
                            if message.data == command:
                                bot.send_message(doctor['id'], f"Вы вылечили игрока: {player_data['name']}")
                                player_data['status'] = 'alive'
                                bot.send_message(player_data['id'], "Вас вылечил доктор!")
                                






                    if citizens['citizen1'][status] == 'die' and citizens['citizen2'][status] == 'die' and citizens['citizen4'][status] == 'die' and citizens['citizen5'][status] == 'die' and citizens['citizen6'][status] == 'die' and citizens['citizen7'][status] == 'die' and mafia['status'] == 'alive' and police['status'] == 'die' and doctor['status'] == 'die':
                        bot.send_message(place.id, "В этой игре выиграла Мафия!")
                        break
                    if mafia['status'] == 'die':
                        bot.send_message(place.id, "В этой игре выиграли Мирные жители и не только!")
                        break
                    
                            
                            
                                    





@bot.callback_query_handler(func=lambda call: True)
def callback_inline(message):
    if message.data == 'ready':
        bot.edit_message_text(chat_id=message.message.chat.id, text = "Хорошая работа!", message_id=message.message.message_id, reply_markup=None)
bot.polling(none_stop=True)




   



















