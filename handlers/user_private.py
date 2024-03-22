# from aiogram import Router, types, F
# from aiogram.filters import CommandStart, StateFilter
# from aiogram.fsm.middleware import FSMContext
# from aiogram.fsm.state import State, StatesGroup
# from aiogram.methods import delete_message
#
# from sqlalchemy.ext.asyncio import AsyncSession
#
#
# from database.orm import add_userpoll, add_userdata
#
# from filters.chat_type import ChatTypeFilter
#
# from ceyboards.reply import basic_ceyboard, basic_ceyboard_aut, fsm_back, fsm_back_2, basic_ceyboard_poll
#
# from pars.parser_journal import pars_homework_j, pars_number_j
#
#
# rout_user_priv = Router()
#
# rout_user_priv.message.filter(ChatTypeFilter(['private']))
#
#
#
#
#
#
# class AddData(StatesGroup):
#     id = State()
#     clas = State()
#     login = State()
#     password = State()
#
#     texts = {
#         'AddData:clas': 'Введите класс заново',
#         'AddData:login': 'Введите логин заново'
#     }
#
#
#
#
#
#
#
# @rout_user_priv.message(F.text == 'О боте')
# async def get_func(message: types.Message):
#     await message.answer(
#         'Текст 2',
#         reply_markup=basic_ceyboard
#     )
#     await message.delete()
#
# @rout_user_priv.message(F.text == 'назад')
# async def get_back1(message: types.Message):
#
#     await message.answer(
#         f'{message.from_user.first_name} Текст 4',
#         reply_markup=basic_ceyboard
#     )
#     await message.delete()
#     await delete_message(message.chat.id, message.message_id)
#
#
# @rout_user_priv.message(StateFilter(None), F.text == 'Авторизация')
# async def authorization(message: types.Message, state: FSMContext):
#     await state.update_data(id=message.from_user.id)
#     await message.answer('clas:', reply_markup=types.ReplyKeyboardRemove())
#
#     await state.set_state(AddData.clas)
#
#
# @rout_user_priv.message(StateFilter('*'), F.text == 'изменить прошлый ответ')
# async def get_back_data(message: types.Message, state: FSMContext) -> None:
#
#     await_state = await state.get_state()
#
#     if await_state == AddData.clas:
#         await message.answer('Предыдущегошага нету')
#         return
#
#     priv = None
#
#     for step in AddData.__all_states__:
#         if await_state == step.state:
#             await state.set_state(priv)
#             await message.answer(
#                 'Вы вернулись к прошлому шаг\n'
#                 f'{AddData.texts[priv.state]}', reply_markup=fsm_back
#             )
#             await message.delete()
#             return
#
#         priv = step
#
#
#
#
# @rout_user_priv.message(AddData.clas, F.text)
# async def get_clas(message: types.Message, state: FSMContext):
#     await state.update_data(clas=message.text)
#
#     await message.answer('login:', reply_markup=fsm_back)
#
#     await state.set_state(AddData.login)
# @rout_user_priv.message(AddData.clas)
# async def get_clas(message: types.Message):
#     await message.answer('False')
#
#
# login = ''
# @rout_user_priv.message(AddData.login, F.text)
# async def get_login(message: types.Message, state: FSMContext):
#     global login
#     await state.update_data(login=message.text)
#     login = message.text
#     await message.answer('password:', reply_markup=fsm_back)
#
#     await state.set_state(AddData.password)
# @rout_user_priv.message(AddData.login)
# async def get_login(message: types.Message):
#     await message.answer('False')
#
#
#
# @rout_user_priv.message(F.text == 'Узнать о боте')
# async def get_about(message: types.Message):
#     await message.answer('Текст 6', reply_markup=basic_ceyboard_aut)
#
#     await message.delete()
#
# class AddProduct(StatesGroup):
#     number = State()
#     descrip = State()
#
#     texts = {
#         'AddProduct:number': 'Введите класс заново'
#     }
#
# @rout_user_priv.message(StateFilter(None), F.text == 'Опрос')
# async def get_poll(message: types.Message, state: FSMContext):
#     await message.answer('В каком ты классе?', reply_markup=types.ReplyKeyboardRemove())
#
#
#     await state.set_state(AddProduct.number)
#
#
# @rout_user_priv.message(StateFilter('*'), F.text == 'исправить прошлый ответ')
# async def get_back(message: types.Message, state: FSMContext) -> None:
#
#     curen_state = await state.get_state()
#
#     if curen_state == AddProduct.number:
#         await message.answer('предыдущего шага нету')
#         return
#     previos = None
#     for step in AddProduct.__all_states__:
#         if step.state == curen_state:
#             await state.set_state(previos)
#             await message.answer(f'Вы вернулись к предыдущему вопросу \n'
#                                  f'{AddProduct.texts[previos.state]}', reply_markup=types.ReplyKeyboardRemove())
#             await message.delete()
#             return
#         previos = step
#
#
#
# @rout_user_priv.message(AddProduct.number, F.text)
# async def ger_number(message: types.Message, state: FSMContext):
#     await state.update_data(number=message.text)
#     await message.answer(
#         'Расскажи, как ты обычно смотришь свои оценки, расписание, и домашнию работу',
#         reply_markup=fsm_back_2
#     )
#     await state.set_state(AddProduct.descrip)
# @rout_user_priv.message(AddProduct.number)
# async def ger_number(message: types.Message):
#     await message.answer('False')
#
#
#
# @rout_user_priv.message(AddProduct.descrip, F.text)
# async def ger_descrip(message: types.Message, state: FSMContext, session: AsyncSession):
#     await state.update_data(descrip=message.text)
#
#     data = await state.get_data()
#
#     await add_userpoll(session, data)
#
#     await message.answer('Спасибо за ответы', reply_markup=basic_ceyboard_poll)
#     await state.clear()
# @rout_user_priv.message(AddProduct.descrip)
# async def ger_descrip(message: types.Message):
#     await message.answer('False')
#
#
#
# password = ''
# @rout_user_priv.message(AddData.password, F.text)
# async def get_password(message: types.Message,  state: FSMContext, session: AsyncSession):
#     global login, password
#     await state.update_data(password=message.text)
#
#     password = message.text
#
#     data = await state.get_data()
#     await add_userdata(session, data)
#
#     await message.answer(pars_number_j(login, password), reply_markup=basic_ceyboard_aut)
#     await message.answer(pars_homework_j(login, password), reply_markup=basic_ceyboard_aut)
#     await message.answer('Расписание ещё в разработке', reply_markup=basic_ceyboard_aut)
#
#     await state.clear()
# @rout_user_priv.message(AddData.password)
# async def get_password(message: types.Message):
#     await message.answer('False')
#
# @rout_user_priv.message(F.text == 'Обновить')
# async def update_auto(message: types.Message):
#     global login, password
#
#     await message.answer(pars_number_j(login, password), reply_markup=basic_ceyboard_aut)
#     await message.answer(pars_homework_j(login, password), reply_markup=basic_ceyboard_aut)
#     await message.answer('Расписание ещё в разработке', reply_markup=basic_ceyboard_aut)

