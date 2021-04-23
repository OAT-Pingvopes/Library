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


languages = {'африканский': 'afrikaans', 'албанский': 'albanian', 'амхарский': 'amharic',
                                 'арабский': 'arabic', 'армянский': 'armenian', 'азербайджанский': 'azerbaijani',
                                 'баскский': 'basque', 'белорусский': 'belarusian', 'бенгальский': 'bengali',
                                 'боснийский': 'bosnian', 'болгарский': 'bulgarian', 'каталонский': 'catalan',
                                 'кебуано': 'cebuano', 'чичева': 'chichewa',
                                 'китайский(упрощённый)': 'chinese (simplified)',
                                 'китайский(традиционный)': 'chinese (traditional)', 'корсиканский': 'corsican',
                                 'хорватский': 'croatian', 'чешский': 'czech', 'датский': 'danish',
                                 'голландский': 'dutch', 'английский': 'english', 'эсперантский': 'esperanto',
                                 'эстонский': 'estonian', 'филипинский': 'filipino', 'финский': 'finnish',
                                 'французский': 'french', 'фризский': 'frisian', 'галицкий': 'galician',
                                 'грузинский': 'georgian', 'немецкий': 'german', 'греческий': 'greek',
                                 'гуджарати': 'gujarati', 'гаитянский': 'haitian creole', 'хауса': 'hausa',
                                 'гавайский': 'hawaiian', 'еврейский': 'hebrew', 'израильский': 'hebrew',
                                 'хинди': 'hindi', 'хминг': 'hmong', 'венгерский': 'hungarian',
                                 'исландский': 'icelandic', 'игбо': 'igbo', 'индонезийский': 'indonesian',
                                 'ирландский': 'irish', 'итальянский': 'italian', 'японский': 'japanese',
                                 'яванский': 'javanese', 'канадский': 'kannada', 'казахский': 'kazakh',
                                 'кхмерский': 'khmer', 'корейский': 'korean', 'курдский': 'kurdish (kurmanji)',
                                 'киргизский': 'kyrgyz', 'лао': 'lao', 'латинский': 'latin', 'латвийский': 'latvian',
                                 'литвийский': 'lithuanian', 'люксембургский': 'luxembourgish',
                                 'македонский': 'macedonian', 'малагасийский': 'malagasy', 'малайский': 'malay',
                                 'малайялама': 'malayalam', 'мальтийский': 'maltese', 'маори': 'maori',
                                 'маратхи': 'marathi', 'монгольский': 'mongolian', 'мьянма': 'myanmar (burmese)',
                                 'непальский': 'nepali', 'норвежский': 'norwegian', 'одия': 'odia',
                                 'пушту': 'pashto', 'персидский': 'persian', 'польский': 'polish',
                                 'португальский': 'portuguese', 'пенджаби': 'punjabi', 'румынский': 'romanian',
                                 'русский': 'russian', 'самоанский': 'samoan', 'шотландский гэльский': 'scots gaelic',
                                 'сербский': 'serbian', 'сесото': 'sesotho', 'шона': 'shona', 'синдхи': 'sindhi',
                                 'синдбала': 'sinhala', 'словакский': 'slovak', 'словенский': 'slovenian',
                                 'сомалийский': 'somali', 'испанский': 'spanish', 'сунданский': 'sundanese',
                                 'суахили': 'swahili', 'шведский': 'swedish', 'таджикский': 'tajik',
                                 'тамильский': 'tamil', 'телугу': 'telugu', 'тайский': 'thai', 'турецкий': 'turkish',
                                 'украинский': 'ukrainian', 'урду': 'urdu', 'уйгур': 'uyghur', 'узбекский': 'uzbek',
                                 'вьетнамский': 'vietnamese', 'валлийский': 'welsh', 'коса': 'xhosa', 'идиш': 'yiddish',
                                 'йоруба': 'yoruba', 'зулу': 'zulu'}


def create_keyboard():
    keyboard = vk_api.keyboard.VkKeyboard(one_time=False)
    keyboard.add_button("!Помощь", color=vk_api.keyboard.VkKeyboardColor.PRIMARY)
    keyboard.add_button("!убери клавиатуру", color=vk_api.keyboard.VkKeyboardColor.POSITIVE)
    keyboard.add_button("!играть", color=vk_api.keyboard.VkKeyboardColor.POSITIVE)
    return keyboard.get_keyboard()


def gaming_keyboard():
    keyboard = vk_api.keyboard.VkKeyboard(one_time=False)
    keyboard.add_button("!баланс", color=vk_api.keyboard.VkKeyboardColor.POSITIVE)
    keyboard.add_button("!сделать бросок", color=vk_api.keyboard.VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button("!помощь", color=vk_api.keyboard.VkKeyboardColor.PRIMARY)
    keyboard.add_button("!закончить игру", color=vk_api.keyboard.VkKeyboardColor.NEGATIVE)
    return keyboard.get_keyboard()


def create_empty_keyboard():
    keyboard = vk_api.keyboard.VkKeyboard.get_empty_keyboard()
    return keyboard


def main():
    vk_session = vk_api.VkApi(
        token='64f7d38df6cbac49f2146d5037a93647b83f9897e355478551f3bee2d393cc2a8f57aefd5803bf5b88750')
    longpoll = VkBotLongPoll(vk_session, 203632426)
    c = 0
    for event in longpoll.listen():
        url = 'https://ru.wikipedia.org/wiki/'
        if event.type == VkBotEventType.MESSAGE_NEW:
            vk = vk_session.get_api()
            txt_msg = event.obj.message['text']
            url += txt_msg
            if '!' == txt_msg[0] and c == 0:
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
                                         message=f"https://static-maps.yandex.ru/1.x/?ll={tpc[0]},{tpc[1]}&size=450,450&z=8&l=map",
                                         random_id=random.randint(0, 2 ** 64))
                    except:
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message="Произошла непредвиденная ошибка",
                                         random_id=random.randint(0, 2 ** 64))
                elif '!помощь' == txt_msg[:7].lower():
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message='!помощь - для показа всех команд\n'
                                             '!найди слово <слово> - выводит определение слова из википедии\n'
                                             '!переведи <слово> <исходный язык> <целевой язык> - переводит слово, '
                                             'для просмотра списка языков введите !языки_переводчика\n'
                                             '!запусти клавиатуру/!убери клавиатуру - запускает и убирает клавиатуру\n'
                                             '!калькулятор <выражение> - вычисляет заданное выражение\n'
                                             '!найди на карте <объект> - выводит ссылку на картинку с объектом\n'
                                             '!играть - запускает небольшую игру\n'
                                             '  !сделать бросок - кидает шестигранный кубик(выводит число от 1 до 6)\n'
                                             '  !угадать число <диапазон> <ставка> <число>- игра на угадывание числа\n'
                                             '  !баланс - выводит баланс(beta)\n'
                                             '  !закончить игру - заканчивает игру',
                                     random_id=random.randint(0, 2 ** 64))
                elif '!играть' == txt_msg.lower():
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message="Запускаю...",
                                     random_id=random.randint(0, 2 ** 64),
                                     keyboard=create_empty_keyboard())
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message="Запустил...",
                                     random_id=random.randint(0, 2 ** 64),
                                     keyboard=gaming_keyboard())
                    c = 1
                elif '!переведи' == txt_msg[:9].lower():
                    translator = Translator()
                    to_trans = txt_msg[10:].split(' ')
                    try:
                        res = translator.translate(to_trans[0], src=languages[to_trans[1]], dest=languages[to_trans[2]])
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message=res.text,
                                         random_id=random.randint(0, 2 ** 64))
                    except:
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message="Неправильно введены данные",
                                         random_id=random.randint(0, 2 ** 64))
                elif '!языки_переводчика' == txt_msg.lower():
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=f'{languages.keys()}',
                                     random_id=random.randint(0, 2 ** 64))
                else:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message='Команда введена неправильно'
                                             'Для списка команд напишите !помощь',
                                     random_id=random.randint(0, 2 ** 64))
            elif '!' == txt_msg[0] and c == 1:
                all_count = 100
                if '!сделать бросок' == txt_msg.lower():
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=random.randint(1, 6),
                                     random_id=random.randint(0, 2 ** 64))
                elif '!угадать число' == txt_msg[:14].lower():
                    values = txt_msg[15:].lower().split(' ')
                    r_num = random.randint(1, int(values[0]))
                    count = int(values[1]) * (int(values[0]) - 1)
                    if r_num == int(values[2]):
                        all_count += count
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message=f"Вы угадали. Выигрыш составил {count}(множитель: {int(values[0]) - 1})",
                                         random_id=random.randint(0, 2 ** 64))
                    else:
                        all_count -=count
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message=f"Вы проиграли {count}. Правильный ответ {r_num}",
                                         random_id=random.randint(0, 2 ** 64))
                elif '!баланс' == txt_msg.lower():
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=f"{all_count}",
                                     random_id=random.randint(0, 2 ** 64))
                elif '!закончить игру' == txt_msg.lower():
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message="Выключаю...",
                                     random_id=random.randint(0, 2 ** 64),
                                     keyboard=create_empty_keyboard())
                    c = 0
                else:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message="Команда введена неправильно",
                                     random_id=random.randint(0, 2 ** 64))


if __name__ == '__main__':
    main()
