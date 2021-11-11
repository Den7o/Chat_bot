import redis
import json

r=redis.Redis(host='localhost', port=6379, db=0)

def enter_data(key, data):# функция  которая отправляем данные в Редис
    data = json.dumps(data) # Переводим данные в json, это нужно чтобы мы смогли отправить данные как словарь
    set_data = r.set(key, data)
    return set_data

def output_data(key): #  Функция которая выводит данные с Redis
    get_data = r.get(key)
    result = json.loads(get_data) # Переводим данные с json в тип данных dict
    return result

def clear_data():# Очистили все данные в Redis
    for key in r.scan_iter():
        result = r.delete(key)
        return result




