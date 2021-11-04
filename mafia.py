import telebot
from telebot import types
from config import TOKEN
import functions_for_mafia as FFM
import random
import time

bot = telebot.TeleBot(token=TOKEN)
players = {}
black_list = []



@bot.message_handler(commands=['game'])
def game_start(message):
    # Проверка на статус группы если группа приватная то игра не начнеться 
    if message.chat.type == "private":
        markup = types.InlineKeyboardMarkup(row_width=2)
        button1 = types.InlineKeyboardButton('✅Готово', callback_data='ready')
        markup.add(button1)
        edit_message = bot.send_message(message.chat.id, "Пожалуйста добавьте меня в группу!", reply_markup=markup)
        @bot.callback_query_handler(func=lambda call: True)
        def callback_inline(message):
            if message.data == 'ready':
                bot.edit_message_text(chat_id=message.message.chat.id, text = "Хорошая работа!", message_id=edit_message, reply_markup=None)

    else:
        markup = types.InlineKeyboardMarkup(row_width=2)
        button1 = types.InlineKeyboardButton('🎲 Присоединиться!',url='https://t.me/thebest_chat_bot')
        markup.add(button1)
        place = message.chat # сдесь храниться json группы(id и название группы)
        bot.send_message(message.chat.id, f"Пользователь @{message.json['from']['username']} начал игру!\n\nЧобы присоединиться в игру нажмите кнопку!", reply_markup=markup)
        
        @bot.message_handler(commands=['start'])
        def join(message):
            # Проверка находиться ли пользователь в словаре players, если нет то добавляют в словарь
            if message.from_user.id not in players.keys() and message.from_user.first_name not in players.values():
                if len(players) >= 10:
                    bot.send_message(message.from_user.id, "Простите, но свободных мест уже не осталось")

                else:
                    players[message.from_user.id] = message.from_user.first_name
                    bot.send_message(message.from_user.id, f"Вы зашли с {place.title}\nКогда начнеться новая игра пожалуйста введите снова /start\n\nЭто нужно чтобы вы добавились в игру!")
                    send_message = bot.send_message(place.id, f"Набор игроков...\n\nОсталось: {10-len(players)} игроков")#place.id - Это id группы
                    # bot.edit_message_text(f"Присоединилось: \n\n{players}\n\nОсталось:{10-len(players)}", chat_id=message.chat.id, message_id=send_message.message_id)
            else:
                bot.send_message(message.from_user.id, "Вы уже присоединились к игре!")
            # Если набереться 10 игроков то игра начнеться
            if len(players) >= 10:
                bot.send_message(place.id, "Game START!")
                FFM.send_message_for_players("Игра Началась!\n\n🍀Распределение ролей, подождите пожалуйста 10 секунд!")
                time.sleep(10)
                FFM.give_roles()
                FFM.send_message_for_players("Игра началась!\nЧтобы написать другим игрокам введите в чат сообщение!")
                status = 'Day'
                
                @bot.message_handler() #Создали чат в котором игроки смогут разговаривать
                def chat(message):
                    if status == 'Day': 
                        for num in range(1,8):                   
                            if citizens[f'citizen{num}']['status'] == 'die':#Проверка на статус игроков
                                bot.send_message(citizens[f'citizen{num}']['id'], "Мертвые не могут разговаривать!")
                            else:
                                FFM.send_message_for_players(f"[{message.from_user.first_name}]\n{message.text}")
                        if police['status'] == 'die':
                            bot.send_message(police['id'], "Мертвые не могут разговаривать!")
                        elif doctor['status'] == 'die':
                            bot.send_message(doctor['id'], "Мертвые не могут разговаривать!")
                        elif mafia['status'] == 'die':
                            bot.send_message(mafia['id'], "Мертвые не могут разговаривать!")
                        else:
                            FFM.send_message_for_players(f"[{message.from_user.first_name}]\n{message.text}")
                    else:
                        bot.send_message(message.from_user.id, "Тише!\nТебя может услышать мафия!")

                while True:
                    time.sleep(50)
                    FFM.send_message_for_players( "--Ведущий--\nОсталось 50 секунд до начала ночи!")
                    time.sleep(50)
                    status = 'Night'
                    FFM.send_message_for_players("--Ведущий--\nГород засыпает, просыпаеться мафия")
                    #-----Мафия-----
                    if mafia['status'] == 'alive':
                        FFM.buttons('kill', 'mafia')
                        bot.send_message(mafia['id'], "Наступила ночь, кого вы хотите убить?", reply_markup=markup)
                        @bot.callback_query_handler(func=lambda call: True)
                        def killed_players(message):
                            player_list = {'kill1': citizens['citizen1'], 'kill2': citizens['citizen2'], 'kill3': doctor, 'kill4': citizens['citizen3'], 'kill5':
                            citizens['citizen4'], 'kill6': citizens['citizen5'], 'kill7': citizens['citizen6'], 'kill8': police, 'kill9': citizens['citizen7']}
                            for command, player_data in player_list.items():
                                if message.data == command:
                                    bot.edit_message_text(chat_id=message.message.chat.id, text = f"Вы убили игрока: {player_data['name']}", message_id=message.message.message_id, reply_markup=None)
                                    player_data['status'] = 'die'
                                    bot.send_message(player_data['id'], "Упс...\nВас убила мафия!")
                                    black_list.append(player_data['name'])
                    else:
                        pass
                                

                        
                    FFM.send_message_for_players(f"--Ведущий--\nГород просыпаеться, засыпает мафия\n\nКол-во убитых за ночь: \n{len(black_list)}")
                    status = 'Day'

                    #-----Доктор-----
                    if doctor['status'] == 'alive':
                        FFM.buttons('heal', 'doctor')
                        @bot.send_message(doctor['id'], "В эту ночь один человек пострадал от мафии пожалуйста помогите ему", reply_markup=markup)
                        @bot.callback_query_handler(func=lambda call: True)
                        def killed_players(message):
                            player_list = {'heal1': citizens['citizen1'], 'heal2': citizens['citizen2'], 'heal4': citizens['citizen3'], 'heal5':
                            citizens['citizen4'], 'heal6': citizens['citizen5'], 'heal7': citizens['citizen6'], 'heal8': police, 'heal9': citizens['citizen7'], 'heal10': mafia}
                            for command, player_data in player_list.items():
                                if message.data == command:
                                    bot.edit_message_text(chat_id=message.message.chat.id, text = f"Вы вылечили игрока: {player_data['name']}", message_id=message.message.message_id, reply_markup=None)
                                    player_data['status'] = 'alive'
                                    bot.send_message(player_data['id'], "Вас вылечил доктор!")
                    else:
                        pass

                    #-----Шериф-----
                    if police['status'] == 'alive':
                        FFM.buttons('arrest', 'police')
                        bot.send_message(police['id'], "В городе появилась мафия, у вас есть предположения кто это может быть?\n Если вы не уверены нажмите кнопку Skip", reply_markup=markup)
                        @bot.callback_query_handler(func=lambda call: True)
                        def killed_players(message):
                            player_list = {'arrest1': citizens['citizen1'], 'arrest2': citizens['citizen2'], 'arrest3': doctor, 'arrest4': citizens['citizen3'], 'arrest5':
                            citizens['citizen4'], 'arrest6': citizens['citizen5'], 'arrest7': citizens['citizen6'], 'arrest9': citizens['citizen7'], 'arrest10': mafia}
                            for command, player_data in player_list.items():
                                if message.data == command:
                                    if player_data == mafia:
                                        bot.edit_message_text(chat_id=message.message.chat.id, text = "Поздравляю вы арестовали мафию!", message_id=message.message.message_id, reply_markup=None)
                                        FFM.send_message_for_players(f"Шериф {police['name']} арестовал мафию, теперь город может спать спокойно!")
                                    else:
                                        bot.edit_message_text(chat_id=message.message.chat.id, text = "Вы убили мирного жителя...\nВас уволили с данной должности", message_id=message.message.message_id, reply_markup=None)
                                        police['status'] == 'die'
                                elif message.data == 'skip':
                                    bot.edit_message_text(chat_id=message.message.chat.id, text = "Скип успешно завершен!", message_id=message.message.message_id, reply_markup=None)
                    else:
                        pass
                    


                    # Игра закончилась!
                    if citizens['citizen1'][status] == 'die' and citizens['citizen2'][status] == 'die' and citizens['citizen4'][status] == 'die' and citizens['citizen5'][status] == 'die' and citizens['citizen6'][status] == 'die' and citizens['citizen7'][status] == 'die' and mafia['status'] == 'alive' and police['status'] == 'die' and doctor['status'] == 'die':
                        bot.send_message(place.id, "В этой игре выиграла Мафия!")
                        break
                    if mafia['status'] == 'die':
                        bot.send_message(place.id, "В этой игре выиграли Мирные жители и не только!")
                        break
                    
                            

bot.polling(none_stop=True)

                            
                                    









   



















