import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random


def main():
    vk_session = vk_api.VkApi(
        token='64f7d38df6cbac49f2146d5037a93647b83f9897e355478551f3bee2d393cc2a8f57aefd5803bf5b88750')
    longpoll = VkBotLongPoll(vk_session, '203632426')
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            vk = vk_session.get_api()
            if 'Привет' in event.message['text']:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message="Привет",
                                 random_id=random.randint(0, 2 ** 64))
            else:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message="Привет",
                                 random_id=random.randint(0, 2 ** 64))


if __name__ == '__main__':
    main()