import redis
import json


r=redis.Redis(host='localhost', port=6379, db=0)


def enter_data(key, data): # Функция для отправки данных в БД
    data = json.dumps(data) # Переводим данные в json, это нужно чтобы мы смогли отправить данные как dict
    set_data = r.set(key, data)
    return set_data

def output_data(key, id=False, name=False): #  Функция для получения дынных, Пример: если id=True то функция вернет только id игрока
    try:
        get_data = r.get(key)
        result = json.loads(get_data) # Переводим данные с json в dict
        if id == True:
            return result['id']
        elif name == True:
            return result['name']
        else:
            return result
    except TypeError:
        return r.get(key)

def delete(key): # Функция для удаления конкретного пользователя
    result = r.delete(key)
    return result

def clear_data():# Очистка БД
    for key in r.scan_iter():
        result = r.delete(key)

def get_len():
    num = 0
    for key in r.scan_iter():
        num += 1
    return num

def get_all_id(): # Получаем id всех игроков
    id_list = []
    for key in r.scan_iter():
        id = output_data(key, id=True)
        id_list.append(id)
    return id_list

def get_all_name():  # Получаем имя всех игроков
    name_list = []
    for key in r.scan_iter():
        name = output_data(key, name=True)
        name_list.append(name)
    return name_list

def get_filter_data(exception):
    data_list = {}
    for key in r.scan_iter():
        if key.decode() == exception:
            pass
        else:
            data = output_data(key, name=True)
            data_list[key.decode()] = data
    return data_list

def get_game_status():
    if output_data('Mafia') == None:
        return True
    elif get_len() == 1 and output_data('Mafia') != None:
        return False
