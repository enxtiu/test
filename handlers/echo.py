from aiogram import Router, types, F


from ceyboards.reply import keybords

rout_echo_priv = Router()

basic_keybord = keybords(
            'О боте'
            'Авторизация',
            'Опрос',
            placeholder='Посмотрите на клавиатуру ниже',
            sizes=(1, 1, 1)
        )
@rout_echo_priv.message(F.text)
async def acho(message: types.Message):
    await message.answer(
        f'{message.from_user.first_name} воспользуйся клавиатурой ниже',
    )