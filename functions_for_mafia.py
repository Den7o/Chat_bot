import random

# Функция которая отправляет сообщение в лс всем игрокам
def send_message_for_players(text):
    for key, value in players.items():
        bot.send_message(key, text)

# Раздаем роли пользователям 
def give_roles():
    num = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    citizens = {}
    number = 1
    #Раздaем роли пользователям 
    for key,value in players.items():# из словаря players береться id и имя пользователя, далее с помощью списка и рандома раздаеться роль
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

# Inline кнопки
def buttons(text, role):
    markup = types.InlineKeyboardMarkup(row_width=2)
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