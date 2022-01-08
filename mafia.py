import telebot
from telebot import types
from telebot.async_telebot import AsyncTeleBot
from config import TOKEN
import my_redis
import random
import asyncio
import time

"""-------Заметки--------"""
"""Починить баг с чатом"""



print('Бот был запущен!')


bot = AsyncTeleBot(token=TOKEN)
url = 'https://t.me/Testing_0000001_bot'
players_name = ['n', 'b', 'c', 'd']
nums = 4
status=True



async def send_message_for_all(text, markup=None): # Функция для отправки сообщения всем игрокам
    for id in my_redis.get_all_id():
        await bot.send_message(id, text, reply_markup=markup)


async def generate_buttons(role, id, text): #Функция для генерации кнопок
    markup = types.InlineKeyboardMarkup()
    button_skip = types.InlineKeyboardButton('Skip', callback_data='skip')
    for key, value in my_redis.get_filter_data(role).items(): # Создаем кнопки основываясь на кол-во игроков
        buttons = types.InlineKeyboardButton(value, callback_data=key)
        markup.row(buttons)
    markup.row(button_skip)
    if id:
        await bot.send_message(id, text, reply_markup=markup)
    else:
        await bot.send_message_for_all(text, reply_markup=markup)



@bot.message_handler(commands=['game'])
async def start_game(message):
    chat_location = message.chat
    role_dict = {'skip': 0, 'Mafia': 0, 'Police': 0, 'Citizen1': 0, 'Citizen2': 0, 'Citizen3': 0, 'Citizen4': 0, 'Citizen5': 0, 'Citizen6': 0, 'Citizen7': 0, 'Citizen8': 0}
    id_list = my_redis.get_all_id()
    if message.chat.type == 'private':
        await bot.send_message(message.chat.id, "Добавьте бота в группу!")
    else:
        markup = types.InlineKeyboardMarkup()
        button_10 = types.InlineKeyboardButton(10, callback_data='num-10')
        button_5 = types.InlineKeyboardButton(5, callback_data='num-5')
        markup.row(button_5, button_10)

        await bot.send_message(message.chat.id, "Выберите количество игроков:", reply_markup=markup)


        @bot.callback_query_handler(func=lambda call: call.data.startswith('num-'))
        async def get_num_of_players(message):
            if int(message.data.replace('num-', '')) == 10:
                list_of_players = [num for num in range(1, 11)]
                num_of_players = 10
            elif int(message.data.replace('num-', '')) == 5:
                list_of_players = [num for num in range(1, 6)]
                num_of_players = 5
            markup = types.InlineKeyboardMarkup()
            button_join = types.InlineKeyboardButton("🎲 Присоединиться!", url=url)
            markup.row(button_join)

            await bot.edit_message_text(
                chat_id = chat_location.id,
                text = f"Пользователь {message.from_user.first_name} начал игру!\n\nЧобы присоединиться в игру нажмите кнопку!\n[Введите /join после захода]",
                message_id = message.message.message_id,
                reply_markup=markup
            )


            @bot.message_handler(commands=['join'])
            async def join_to_game(message):
                global nums
                if message.chat.type == 'private':
                    if message.from_user.first_name not in players_name:
                        if nums >= num_of_players:
                            await bot.send_message(message.from_user.id, "Простите, но свободных мест не осталось!")
                        else:
                            nums += 1
                            players_name.append(message.from_user.first_name)
                            await bot.send_message(chat_location.id, f'Набор игроков...\n\nОсталось {num_of_players-nums} игроков')
                            random_role = random.choice(list_of_players)
                            a = 1

                            """РАЗДАЧА РОЛЕЙ"""
                            if random_role == 1: # Мафия
                                list_of_players.remove(random_role)
                                my_redis.enter_data('Mafia', {'name': message.from_user.first_name, 'id': message.from_user.id})
                                await bot.send_message(message.from_user.id, "🎲 Ваша роль - Мафия!")
                            elif random_role == 2: # Полиция
                                list_of_players.remove(random_role)
                                my_redis.enter_data('Police', {'name': message.from_user.first_name, 'id': message.from_user.id})
                                await bot.send_message(message.from_user.id, "🎲 Ваша роль - Детектив!")
                            else:
                                list_of_players.remove(random_role)
                                my_redis.enter_data(f'Citizen{a}', {'name': message.from_user.first_name, 'id': message.from_user.id})
                                await bot.send_message(message.from_user.id, "🎲 Ваша роль - Житель!")
                                a += 1

                    else:
                         await bot.send_message(message.from_user.id, "Вы уже присоединились к игре!")
                else:
                    await bot.send_message(message.chat.id, f"{message.from_user.first_name} сперва нажмите на кнопку а после введите /join")

                if nums >= num_of_players:
                    await bot.send_message(chat_location.id, "GAME START!")
                    await send_message_for_all('Игра началась!\n\nЧтобы написать другим игрокам введите в чат сообщение!')


                    @bot.callback_query_handler(func=lambda call: call.message.text.startswith('Выберите'))
                    async def delete_one_player(message):
                        role_list = ['Mafia', 'Police', 'Citizen1', 'Citizen2', 'Citizen3', 'Citizen4', 'Citizen5', 'Citizen6', 'Citizen7', 'Citizen8']
                        if message.data in role_list:
                            my_redis.delete(message.data)
                            await bot.delete_message(message.from_user.id, message.message.message_id)
                        elif message.data == 'skip':
                            await bot.delete_message(message.from_user.id, message.message.message_id)

                    @bot.callback_query_handler(func=lambda call: call.message.text.startswith('--Голосование--'))
                    async def vote(message):
                        if message.data in role_dict:
                            await bot.delete_message(message.from_user.id, message.message.message_id)
                            role_dict[message.data] += 1
                            id_list.remove(message.from_user.id)
                            for id in id_list:
                                await bot.send_message(id, 'Пожалуйста голосуйте быстрее!')
                            if len(id_list) == 0:
                                max_num = max(role_dict.values())
                                result = {key: value for key, value in role_dict.items() if value == max_num}
                                if len(result) == 1:
                                    final = list(result.keys())
                                    my_redis.delete(final[-1])



                    @bot.message_handler() # Чат для игры
                    async def chat_for_game(message):
                        if status: # Проверка на ночь/день
                            if message.from_user.first_name in my_redis.get_all_name():
                                await send_message_for_all(f"[{message.from_user.first_name}]\n{message.text}")
                            else:
                                await send_message(message.from_user.id, 'Простите вы не можете отправлять сообщения, вы умерли!')
                        else:
                            await bot.send_message(message.from_user.id, "Тише!\nТебя может услышать мафия!")




                    while True:
                        status = True
                        await time.sleep(20)
                        await send_message_for_all( "--Ведущий--\nОсталось 50 секунд до начала ночи!")
                        await time.sleep(50)
                        await send_message_for_all("--Ведущий--\nГород засыпает, просыпаеться мафия")
                        status = False
                        await generate_buttons('Mafia', my_redis.output_data('Mafia', id=True), 'Выберите кого вы хотите убить\n\n[Для скипа нажмите кнопку Skip]')
                        await send_message_for_all("--Ведущий--\nГород просыпаеться, засыпает мафия")
                        await send_message_for_all(f"--Ведущий--\nОсталось: {len(my_redis.get_len())} игроков")
                        status = True
                        await generate_buttons('Police', my_redis.output_data('Police', id=True), 'Выберите кого вы подозриваете\n\n[Для скипа нажмите кнопку Skip]')
                        await generate_buttons('N', id=None, text='--Голосование--\nКого вы подозриваете?')

                        gamestat = my_redis.get_game_status()
                        if gamestat:
                            await bot.send_message(chat_location.id, 'В этой игре выиграли Жители и Детектив')
                            my_redis.clear_data() # Очищаем БД
                            break
                        else:
                            await bot.send_message(chat_location.id, 'В этой игре выиграла Мафия!')
                            my_redis.clear_data() # Очищаем БД
                            break

asyncio.run(bot.polling())