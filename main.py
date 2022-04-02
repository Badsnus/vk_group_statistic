import operator
import time

import vk_api

#логинимся в вк
vk = vk_api.VkApi(
    token='TOKEN').get_api()

chat_id = 0 #id группы

users_id = vk.messages.getChat(chat_id=chat_id)['users']

users = {}.fromkeys(users_id, 0)
offset = 0

message_count = 0
while True:
    try:
        print(message_count)
        messages = vk.messages.getHistory(count=200, peer_id=2000000000 + chat_id, offset=offset)['items']
        if len(messages) != 0:
            for message in messages:
                message = message['from_id']
                try:
                    users[message] += 1
                except:
                    users[message] = 1
            offset += 200
            message_count += len(messages)
        else:
            break
    except Exception as ex:
        print(ex)
        break

sorted_tuples = sorted(users.items(), key=operator.itemgetter(1), reverse=True)
sorted_dict = {k: v for k, v in sorted_tuples}

users_name = []
users = {}.fromkeys(users_id, '')

names = vk.users.get(user_ids=users_id)
for name in names:
    user = name['id']
    name = f'{name["first_name"]} {name["last_name"]}'
    users_name.append([user, name])
    users[user] = name

result = f'Статистика беседы за {message_count} сообщений\n'
for user in sorted_dict:
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
