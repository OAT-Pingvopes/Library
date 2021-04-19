import random
import requests
import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import wikipedia
from googletrans import Translator

wikipedia.set_lang('ru')
vk_session = vk_api.VkApi(
        token='64f7d38df6cbac49f2146d5037a93647b83f9897e355478551f3bee2d393cc2a8f57aefd5803bf5b88750')
longpoll = VkBotLongPoll(vk_session, 203632426)


def create_keyboard():
    keyboard = vk_api.keyboard.VkKeyboard(one_time=False)
    keyboard.add_button("!Помощь", color=vk_api.keyboard.VkKeyboardColor.NEGATIVE)
    return keyboard.get_keyboard()


def create_empty_keyboard():
    keyboard = vk_api.keyboard.VkKeyboard.get_empty_keyboard()
    return keyboard


def main():
    vk_session = vk_api.VkApi(
        token='64f7d38df6cbac49f2146d5037a93647b83f9897e355478551f3bee2d393cc2a8f57aefd5803bf5b88750')
    longpoll = VkBotLongPoll(vk_session, 203632426)

    for event in longpoll.listen():
        url = 'https://ru.wikipedia.org/wiki/'
        if event.type == VkBotEventType.MESSAGE_NEW:
            vk = vk_session.get_api()
            txt_msg = event.obj.message['text']
            url += txt_msg
            if '!' == txt_msg[0]:
                if '!запусти клавиатуру' == txt_msg.lower():
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message="Создаю...",
                                     random_id=random.randint(0, 2 ** 64),
                                     keyboard=create_keyboard())
                elif '!убери клавиатуру' == txt_msg.lower():
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message="Убираю...",
                                     random_id=random.randint(0, 2 ** 64),
                                     keyboard=create_empty_keyboard())
                elif '!найди слово' == txt_msg[:12].lower():
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message="Попробуем найти...",
                                     random_id=random.randint(0, 2 ** 64))
                    try:
                        data = wikipedia.page(txt_msg[13:]).summary
                        a = data.split('\n')
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message=f'{a[0]}',
                                         random_id=random.randint(0, 2 ** 64))
                    except:
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message='К сожалению произошла непредвиденная ошибка,'
                                                 ' моя команда работает над её исправлением',
                                         random_id=random.randint(0, 2 ** 64))
                elif '!калькулятор' == txt_msg[:12].lower():
                    try:
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message=f"Ответ: {eval(txt_msg[13:])}",
                                         random_id=random.randint(0, 2 ** 64))
                    except:
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message='Некорректное значение',
                                         random_id=random.randint(0, 2 ** 64))
                elif '!найди на карте' == txt_msg[:15].lower():
                    try:
                        geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={txt_msg[16:]}, 1&format=json"
                        response = requests.get(geocoder_request)
                        if response:
                            json_response = response.json()
                            toponym_coords = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]['Point']['pos']
                            tpc = toponym_coords.split(' ')
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message=f"https://static-maps.yandex.ru/1.x/?ll={tpc[0]},{tpc[1]}&size=450,450&z=10&l=map",
                                         random_id=random.randint(0, 2 ** 64))
                    except:
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message="Произошла непредвиденная ошибка",
                                         random_id=random.randint(0, 2 ** 64))
                elif '!помощь' == txt_msg[:7].lower():
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message='!помощь - для показа всех команд\n'
                                             '!найди слово <слово> - выводит определение слова из википедии\n',
                                     random_id=random.randint(0, 2 ** 64))
                elif '!переведи' == txt_msg[:9].lower():
                    translator = Translator()
                    to_trans = txt_msg[10:].split(' ')
                    try:
                        res = translator.translate(to_trans[0], src=to_trans[1], dest=to_trans[2])
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message=res.text,
                                         random_id=random.randint(0, 2 ** 64))
                    except:
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message="Неправильно введены данные",
                                         random_id=random.randint(0, 2 ** 64))
                else:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message='Команда введена неправильно'
                                             'Для списка команд напишите !помощь',
                                     random_id=random.randint(0, 2 ** 64))


if __name__ == '__main__':
    main()
