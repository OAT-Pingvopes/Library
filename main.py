import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random

hellos = ['hello', 'привет', 'ало', 'алло', 'здравствуйте', 'здравствуй', 'ку', 'q', 'здарова']
def main():
    vk_session = vk_api.VkApi(
        token='64f7d38df6cbac49f2146d5037a93647b83f9897e355478551f3bee2d393cc2a8f57aefd5803bf5b88750')
    longpoll = VkBotLongPoll(vk_session, 203632426)
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            vk = vk_session.get_api()
            txt_msg = event.obj.message['text']
            ID = event.obj.message['from_id']
            user_get = vk.users.get(user_ids=ID)
            user_get = user_get[0]
            first_name = user_get['first_name']
            last_name = user_get['last_name']
            txt_msg_remade = str(txt_msg[0:6]).lower()
            string_hello = 'Добрый день, ' + first_name + ' ' + last_name + '''\n Чтобы оставить заявку, начните сообщение со слова - заявка\nТакже уточните вашу ФИО и класс, если вы не хотите разшлащать свои данные, можете оставить заявку без указания ФИО и класс'''
            print(txt_msg_remade)
            if txt_msg_remade in hellos:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=string_hello,
                                 random_id=random.randint(0, 2 ** 64))
            if txt_msg_remade == 'заявка':
                vk.messages.send(user_id=392486366,
                                 message=txt_msg,
                                 random_id=random.randint(0, 2 ** 64))
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message='Ваша заявка будет принята к рассмотрению',
                                 random_id=random.randint(0, 2 ** 64))


if __name__ == '__main__':
    main()