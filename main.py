import random
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import wikipedia
import random

wikipedia.set_lang('ru')


def main():
    vk_session = vk_api.VkApi(
        token='64f7d38df6cbac49f2146d5037a93647b83f9897e355478551f3bee2d393cc2a8f57aefd5803bf5b88750')
    longpoll = VkBotLongPoll(vk_session, 203632426)
    for event in longpoll.listen():
        url = 'https://ru.wikipedia.org/wiki/'
        if event.type == VkBotEventType.MESSAGE_NEW:
            vk = vk_session.get_api()
            txt_msg = event.obj.message['text']
            print('Текст:', txt_msg)
            print(event.obj.message['from_id'])
            url += txt_msg
            if 'Прив' in txt_msg:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message="Здравствуйте",
                                 random_id=random.randint(0, 2 ** 64))
            else:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message="Попробуем найти...",
                                 random_id=random.randint(0, 2 ** 64))
                try:
                    data = wikipedia.page(txt_msg).summary
                    a = data.split('\n')
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=f'{a[0]}',
                                     random_id=random.randint(0, 2 ** 64))
                except:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message='К сожалению произошла непредвиденная ошибка,'
                                             ' моя команда работает над её исправлением',
                                     random_id=random.randint(0, 2 ** 64))


if __name__ == '__main__':
    main()