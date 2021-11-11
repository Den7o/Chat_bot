from math import pi
import telebot
from telebot import types
from config import TOKEN
import random
import time

bot = telebot.TeleBot(token=TOKEN)
players = {}
black_list = []

# Функция которая отправляет сообщение в лс всем игрокам
def send_message_for_players(text):
    for value, key in players.items():
        bot.send_message(key, text)





@bot.message_handler(commands=['game'])
def game_start(message):
    # Проверка на статус группы если группа приватная то игра не начнеться 
    if message.chat.type == "private":
        markup = types.InlineKeyboardMarkup(row_width=2)
        button1 = types.InlineKeyboardButton('✅Готово', callback_data='ready')
        markup.add(button1)
        edit_message = bot.send_message(message.chat.id, "Пожалуйста добавьте меня в группу!", reply_markup=markup)
        
        
    else:
        markup = types.InlineKeyboardMarkup(row_width=2)
        button1 = types.InlineKeyboardButton('🎲 Присоединиться!',url='https://t.me/thebest_chat_bot')
        markup.add(button1)
        place = message.chat # сдесь храниться json группы(id и название группы)
        bot.send_message(message.chat.id, f"Пользователь {message.json['from']['first_name']} начал игру!\n\nЧобы присоединиться в игру нажмите кнопку!", reply_markup=markup)
        
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
            else:
                bot.send_message(message.from_user.id, "Вы уже присоединились к игре!")
            # Если набереться 10 игроков то игра начнеться
            if len(players) >= 10:
                bot.send_message(place.id, "Game START!")
                send_message_for_players("Игра Началась!\n\n🍀Распределение ролей, подождите пожалуйста 10 секунд!")
                time.sleep(10)
                num = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
                citizens = {}
                number = 1
    #Раздaем роли пользователям 
                for value,key in players.items():# из словаря players береться id и имя пользователя, далее с помощью списка и рандома раздаеться роль
                    random1 = random.choice(num) #Взяли одно число из списка num
                    if random1 == 5:
                        num.remove(random1)# из списка удаляется число которое прошло через условие, это нужно чтобы число не вызвалось дважды
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
                        num.remove(random1)
                        bot.send_message(key, "Вы мирный житель!\nНечего страшного в следующий раз повезет")
                        #Создаем словарь в котором храниться 7 мирных жителей
                        citizens.update({f"citizen{number}":{
                            'id': key,
                            'name': value,
                            'status': 'alive'
                        }})
                        number += 1
                send_message_for_players("Игра началась!\nЧтобы написать другим игрокам введите в чат сообщение!")
                status = 'Day'
                
                @bot.message_handler() #Создали чат в котором игроки смогут разговаривать
                def chat(message):
                    if status == 'Day': 
                        if police['status'] == 'die':
                            bot.send_message(police['id'], "Мертвые не могут разговаривать!")
                        elif doctor['status'] == 'die':
                            bot.send_message(doctor['id'], "Мертвые не могут разговаривать!")
                        elif mafia['status'] == 'die':
                            bot.send_message(mafia['id'], "Мертвые не могут разговаривать!")
                        else:
                            send_message_for_players(f"[{message.from_user.first_name}]\n{message.text}")
                    else:
                        bot.send_message(message.from_user.id, "Тише!\nТебя может услышать мафия!")

                    # Inline кнопки
                def buttons(text, role):
                    markup = types.InlineKeyboardMarkup(row_width=3)
                    button1 = types.InlineKeyboardButton(citizens['citizen1']['name'], callback_data=text+'1')
                    button2 = types.InlineKeyboardButton(citizens['citizen2']['name'], callback_data=text+'2')
                    button3 = types.InlineKeyboardButton(doctor['name'], callback_data=text+'3')
                    button4 = types.InlineKeyboardButton(citizens['citizen3']['name'], callback_data=text+'4')
                    button5 = types.InlineKeyboardButton(citizens['citizen4']['name'], callback_data=text+'5')
                    button6 = types.InlineKeyboardButton(citizens['citizen5']['name'], callback_data=text+'6')
                    button7 = types.InlineKeyboardButton(citizens['citizen6']['name'], callback_data=text+'7')
                    button8 = types.InlineKeyboardButton(police['name'], callback_data=text+'8')
                    button9 = types.InlineKeyboardButton(citizens['citizen7']['name'], callback_data=text+'9')
                    button10 = types.InlineKeyboardButton(mafia['name'], callback_data=text+'10')
                    skip = types.InlineKeyboardButton('Skip', callback_data='skip')
                    if role == 'mafia':     
                        button_list = [button1, button2, button3, button4, button5, button6, button7, button8, button9]
                        markup.add(random.shuffle(button_list))
                    elif role == 'doctor':
                        button_list = [button1, button2, button4, button5, button6, button7, button8, button9, button10]
                        markup.add(random.shuffle(button_list))
                    elif role == 'police':
                        button_list = [button1, button2, button3, button4, button5, button6, button7, button9, button10, skip]
                        markup.add(random.shuffle(button_list))
                while True:
                    time.sleep(50)
                    send_message_for_players( "--Ведущий--\nОсталось 50 секунд до начала ночи!")
                    time.sleep(50)
                    status = 'Night'
                    send_message_for_players("--Ведущий--\nГород засыпает, просыпаеться мафия")
                    #-----Мафия-----
                    if mafia['status'] == 'alive':
                        buttons('kill', 'mafia')
                        bot.send_message(mafia['id'], "Наступила ночь, кого вы хотите убить?", reply_markup=buttons('kill', 'mafia'))
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
                                

                        
                    send_message_for_players(f"--Ведущий--\nГород просыпаеться, засыпает мафия\n\nКол-во убитых за ночь: \n{len(black_list)}")
                    status = 'Day'

                    #-----Доктор-----
                    if doctor['status'] == 'alive':
                        buttons('heal', 'doctor')
                        @bot.send_message(doctor['id'], "В эту ночь один человек пострадал от мафии пожалуйста помогите ему", reply_markup=markup)
                        @bot.callback_query_handler(func=lambda call: True)
                        def healsed_players(message):
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
                        buttons('arrest', 'police')
                        bot.send_message(police['id'], "В городе появилась мафия, у вас есть предположения кто это может быть?\n Если вы не уверены нажмите кнопку Skip", reply_markup=markup)
                        @bot.callback_query_handler(func=lambda call: True)
                        def arrest_players(message):
                            player_list = {'arrest1': citizens['citizen1'], 'arrest2': citizens['citizen2'], 'arrest3': doctor, 'arrest4': citizens['citizen3'], 'arrest5':
                            citizens['citizen4'], 'arrest6': citizens['citizen5'], 'arrest7': citizens['citizen6'], 'arrest9': citizens['citizen7'], 'arrest10': mafia}
                            for command, player_data in player_list.items():
                                if message.data == command:
                                    if player_data == mafia:
                                        bot.edit_message_text(chat_id=message.message.chat.id, text = "Поздравляю вы арестовали мафию!", message_id=message.message.message_id, reply_markup=None)
                                        send_message_for_players(f"Шериф {police['name']} арестовал мафию, теперь город может спать спокойно!")
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

@bot.callback_query_handler(func=lambda call: True)  
def callback_inline(message):
    if message.data == 'ready':
        bot.edit_message_text(chat_id=message.message.chat.id, text = "Хорошая работа!",message_id=message.message.message_id, reply_markup=None)


bot.polling(none_stop=True)

                            
                                    









   



















