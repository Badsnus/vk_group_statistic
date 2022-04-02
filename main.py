import operator
import time

import vk_api

#логинимся в вк
vk = vk_api.VkApi(
    token='TOKEN').get_api()
#id чата
chat_id = 0

#получаем id всех юзеров
users_id = vk.messages.getChat(chat_id=chat_id)['users']

#создаем словарь с ключами id юзеров и кол-вом сообщений 0
users = {}.fromkeys(users_id, 0)
#устанавливаем смешение сообщений на 0 
offset = 0

#задаем переменную для подсчета общего кол-ва сообщений 
message_count = 0

#в цикле получаем все сообщения чата
while True:
    try:
        #выводим кол-во сообщений на данный момент
        print(message_count)
        #получаем 200 сообщений со смещением равным offset (тк вк не дает выгружать больше 200 сообщений)
        messages = vk.messages.getHistory(count=200, peer_id=2000000000 + chat_id, offset=offset)['items']
        #проверяем если ли в полученном масиве сообщения или нет
        if len(messages) != 0:
            for message in messages:
                #увеличиваем счетчик сообщений для юзера
                message = message['from_id']
                try:
                    users[message] += 1
                except:
                    # если юзера больше нет в группе (нет в исходном словаре), добавляем id в словарь
                    users[message] = 1
            # добавляем offset
            offset += 200
            #увеличиваем счетчик сообщений
            message_count += len(messages)
        else:
            break
    except Exception as ex:
        print(ex)
        break

#сортируем наш словарь в порядке убывания
sorted_tuples = sorted(users.items(), key=operator.itemgetter(1), reverse=True)
sorted_dict = {k: v for k, v in sorted_tuples}

# получаем имена пользователей 
users_name = []
users = {}.fromkeys(users_id, '')

names = vk.users.get(user_ids=users_id)
for name in names:
    user = name['id']
    name = f'{name["first_name"]} {name["last_name"]}'
    users_name.append([user, name])
    users[user] = name
#генерируем итоговый результат
result = f'Статистика беседы за {message_count} сообщений\n'
for user in sorted_dict:
    # Проверяем: является ли юзер ботов
    if str(user)[0] != '-':
        try:
            if users[user][-1] == 'а' or users[user][-1] == 'я':
                result += f'{users[user]} отправила {sorted_dict[user]} сообщений\n'
            else:
                result += f'{users[user]} отправил {sorted_dict[user]} сообщений\n'
        except:
            name = vk.users.get(user_ids=user)[0]
            name = f'{name["first_name"]} {name["last_name"]}'
            if name == 'а' or name == 'я':
                result += f'{name} отправила {sorted_dict[user]} сообщений\n'
            else:
                result += f'{name} отправил {sorted_dict[user]} сообщений\n'
print(result)
