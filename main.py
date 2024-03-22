import asyncio
import os

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.middleware import FSMContext
from aiogram.fsm.state import State, StatesGroup


from sqlalchemy.ext.asyncio import AsyncSession


from midlware.dp import DataBaseSession

from filters.chat_type import ChatTypeFilter

from database.engin import created_db, drop_db, session_marker
from database.orm import add_userpoll, add_userdata

from ceyboards.reply import basic_ceyboard, basic_ceyboard_aut, fsm_back, fsm_back_2, basic_ceyboard_poll

from pars.parser_journal import pars_homework_j, pars_number_j


# from handlers.user_private import rout_user_priv
from handlers.echo import rout_echo_priv

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


bot = Bot(token=os.getenv('TOKEN'))

dp = Dispatcher()

dp.message.filter(ChatTypeFilter(['private']))

# dp.include_router(rout_user_priv)
dp.include_router(rout_echo_priv)

async def on_startup(bot):
    run_params = False
    if run_params:
        await drop_db()
    await created_db()
async def on_shutdown(bot):
    print('бот на коленях')






class AddData(StatesGroup):
    id = State()
    clas = State()
    login = State()
    password = State()

    texts = {
        'AddData:clas': 'Введите класс заново',
        'AddData:login': 'Введите логин заново'
    }
class AddProduct(StatesGroup):
    number = State()
    descrip = State()

    texts = {
        'AddProduct:number': 'Введите класс заново'
    }



@dp.message(CommandStart())
async def get_start(message: types.Message):
    await message.answer(
        f'{message.from_user.first_name} привет, я твой информационный помощник. С моей помощью ты будешь быстро и эфективно получать свежую информацию о домашке и о оценках',
        reply_markup=basic_ceyboard
    )
    await message.delete()




@dp.message(F.text == 'О информационном помощнике')
async def get_func(message: types.Message):
    await message.answer(
        'Я был разработан учеником 11-ого класса. Моя первостепенная задача обеспечить тебе максимально удобной и быстрой информацией о школе.\nЯ работаю 24/7 так что обращайся в любое время',
        reply_markup=basic_ceyboard
    )
    await message.delete()



@dp.message(StateFilter(None), F.text == 'Пройти Авторизацию')
async def authorization(message: types.Message, state: FSMContext):
    await state.update_data(id=message.from_user.id)
    await message.answer(f'{message.from_user.first_name} пожалуйста, заполняй данные правильно. В конце пароля и логина пробелы не следует оставлять. Мне нужно будет от тебя твой класс и пароль с логином от электронного журнала школы', reply_markup=types.ReplyKeyboardRemove())
    await message.answer('Введи свой клас:')
    await state.set_state(AddData.clas)


@dp.message(StateFilter('*'), F.text == 'изменить прошлый ответ')
async def get_back_data(message: types.Message, state: FSMContext) -> None:

    await_state = await state.get_state()

    if await_state == AddData.clas:
        await message.answer('Предыдущего шага нету')
        await asyncio.sleep(1)
        await bot.delete_message(message.chat.id, message.message_id + 1)
        return

    priv = None

    for step in AddData.__all_states__:
        if await_state == step.state:
            await state.set_state(priv)
            await message.answer(
                'Вы вернулись к прошлому шагу\n'
                f'{AddData.texts[priv.state]}', reply_markup=types.ReplyKeyboardRemove()
            )
            await message.delete()
            return

        priv = step




@dp.message(AddData.clas, F.text)
async def get_clas(message: types.Message, state: FSMContext):
    await state.update_data(clas=message.text)

    await message.answer('Теперь введи свой логин:', reply_markup=fsm_back)

    await state.set_state(AddData.login)
@dp.message(AddData.clas)
async def get_clas(message: types.Message):
    await message.answer('Вы в вели некоректный ввод')
    await asyncio.sleep(5)
    await bot.delete_message(message.chat.id, message.message_id + 1)


login = ''
@dp.message(AddData.login, F.text)
async def get_login(message: types.Message, state: FSMContext):
    global login
    await state.update_data(login=message.text)
    login = message.text
    await message.answer('И наконец пароль:', reply_markup=fsm_back)

    await state.set_state(AddData.password)
@dp.message(AddData.login)
async def get_login(message: types.Message):
    await message.answer('Вы в вели некоректный ввод')
    await asyncio.sleep(5)
    await bot.delete_message(message.chat.id, message.message_id + 1)



@dp.message(F.text == 'Узнать о боте')
async def get_about(message: types.Message):
    await message.answer('Я был разработан учеником 11-ого класса. Моя первостепенная задача обеспечить тебе максимально удобной и быстрой информацией о школе.\nЯ работаю 24/7 так что обращайся в любое время', reply_markup=basic_ceyboard_aut)

    await message.delete()


@dp.message(StateFilter(None), F.text == 'Пройти опрос')
async def get_poll(message: types.Message, state: FSMContext):
    await message.answer('В каком ты классе?', reply_markup=types.ReplyKeyboardRemove())


    await state.set_state(AddProduct.number)


@dp.message(StateFilter('*'), F.text == 'исправить прошлый ответ')
async def get_back(message: types.Message, state: FSMContext) -> None:

    curen_state = await state.get_state()

    if curen_state == AddProduct.number:
        await message.answer('предыдущего шага нету')
        await asyncio.sleep(1)
        await bot.delete_message(message.chat.id, message.message_id + 1)
        return
    previos = None
    for step in AddProduct.__all_states__:
        if step.state == curen_state:
            await state.set_state(previos)
            await message.answer(f'Вы вернулись к предыдущему вопросу \n'
                                 f'{AddProduct.texts[previos.state]}', reply_markup=types.ReplyKeyboardRemove())
            await message.delete()
            return
        previos = step



@dp.message(AddProduct.number, F.text)
async def ger_number(message: types.Message, state: FSMContext):
    await state.update_data(number=message.text)
    await message.answer(
        'Расскажи, как ты обычно смотришь свои оценки, расписание, и домашнию работу',
        reply_markup=fsm_back_2
    )
    await state.set_state(AddProduct.descrip)
@dp.message(AddProduct.number)
async def ger_number(message: types.Message):
    await message.answer('Вы в вели некоректный ввод')
    await asyncio.sleep(3)
    await bot.delete_message(message.chat.id, message.message_id + 1)



@dp.message(AddProduct.descrip, F.text)
async def ger_descrip(message: types.Message, state: FSMContext, session: AsyncSession):
    await state.update_data(descrip=message.text)

    data = await state.get_data()
    try:
        await add_userpoll(session, data)

        await message.answer('Спасибо за ответы', reply_markup=basic_ceyboard_poll)
        await state.clear()
    except Exception as a:
        await message.answer(f'Обратитесь к разработчику с ошибкой: {a},\nлибо попробуйте повторно пройти опрос', reply_markup=basic_ceyboard)

@dp.message(AddProduct.descrip)
async def ger_descrip(message: types.Message):
    await message.answer('Вы в вели некоректный ввод')
    await asyncio.sleep(3)
    await bot.delete_message(message.chat.id, message.message_id + 1)


password = ''
@dp.message(AddData.password, F.text)
async def get_password(message: types.Message,  state: FSMContext, session: AsyncSession):
    global login, password
    try:
        await state.update_data(password=message.text)
        password = message.text

        await message.answer(pars_number_j(login, password), reply_markup=basic_ceyboard_aut)
        await message.answer(pars_homework_j(login, password), reply_markup=basic_ceyboard_aut)
        await message.answer('Расписание ещё в разработке', reply_markup=basic_ceyboard_aut)

        data = await state.get_data()
        await add_userdata(session, data)

    except Exception as e:
        await message.answer(f'Вы вели некоректный ввод, проверте написание класса, логина и пароля\nЕсли повторная авторизация не помогает обратитесь к разработчику с ошибкой:\n{e}', reply_markup=basic_ceyboard_poll)
    try:
        await state.clear()
        await asyncio.sleep(360)
        await bot.delete_message(message.chat.id, message.message_id + 1)
        await bot.delete_message(message.chat.id, message.message_id + 2)
        await bot.delete_message(message.chat.id, message.message_id + 3)
    except Exception as e:
        await message.answer(f'Обратитесь к разработчику с ошибкой:\n{e},\nлибо попробуйте пройти повторную авторизацию', reply_markup=basic_ceyboard_poll)

    await message.answer('Обновите информацию', reply_markup=basic_ceyboard_aut)
@dp.message(AddData.password)
async def get_password(message: types.Message):
    await message.answer('Вы в вели некоректный ввод')
    await asyncio.sleep(5)
    await bot.delete_message(message.chat.id, message.message_id + 1)


@dp.message(F.text == 'Обновить информацию')
async def update_auto(message: types.Message):
    global login, password
    try:
        await message.answer(pars_number_j(login, password), reply_markup=basic_ceyboard_aut)
        await message.answer(pars_homework_j(login, password), reply_markup=basic_ceyboard_aut)
        await message.answer('Расписание ещё в разработке', reply_markup=basic_ceyboard_aut)

        await asyncio.sleep(360)
        await bot.delete_message(message.chat.id, message.message_id + 1)
        await bot.delete_message(message.chat.id, message.message_id + 2)
        await bot.delete_message(message.chat.id, message.message_id + 3)

        await message.answer('Обновите информацию', reply_markup=basic_ceyboard_aut)
    except Exception as e:
        await message.answer(f'Пройдите повторную авторизацию\nЕсли повторная авторизация не помогает обратитесь к разработчику с ошибкой:\n{e}', reply_markup=basic_ceyboard_poll)








async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.update.middleware(DataBaseSession(session_pool=session_marker))

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == '__main__':
    asyncio.run(main())