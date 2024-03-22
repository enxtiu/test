from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton


def keybords(
        *button: str,
        placeholder: str = None,
        request_contact: int = None,
        request_location: int = None,
        sizes: tuple[int] = (2,)
    ):
    keybord = ReplyKeyboardBuilder()

    for index, text in enumerate(button, start=0):
        if request_contact == index:
            keybord.add(KeyboardButton(text=text, request_contact=True))
        elif request_location == index:
            keybord.add(KeyboardButton(text=text, request_location=True))

        keybord.add(KeyboardButton(text=text))
    return keybord.adjust(*sizes).as_markup(
        resize_keyboard=True, input_field_placeholder=placeholder
    )

basic_ceyboard = keybords(
    'О информационном помощнике',
    'Пройти Авторизацию',
    'Пройти опрос',
    placeholder='Воспользуйся клавиатурой ниже',
    sizes=(1, 1, 1)
)
basic_ceyboard_poll = keybords(
    'Пройти Авторизацию',
    placeholder='Воспользуйся клавиатурой ниже',
    sizes=(1, )
)
basic_ceyboard_aut = keybords(
    'Узнать о боте',
    'Обновить информацию',
    placeholder='Воспользуйся клавиатурой ниже',
    sizes=(1, 1)
)
fsm_back = keybords(
    'изменить прошлый ответ',
    placeholder='Ответь на вопрос',
    sizes=(1, )
)
fsm_back_2 = keybords(
    'исправить прошлый ответ',
    placeholder='Ответь на вопрос',
    sizes=(1, )
)
