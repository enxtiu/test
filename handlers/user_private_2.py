# from aiogram import Router, types, F
# from aiogram.filters import CommandStart, StateFilter
# from aiogram.fsm.middleware import FSMContext
# from aiogram.fsm.state import State, StatesGroup
#
# from sqlalchemy.ext.asyncio import AsyncSession
#
# from database.orm import add_userpoll, add_userdata
#
# from filters.chat_type import ChatTypeFilter
#
# from ceyboards.reply import fsm_back_2, basic_ceyboard_poll
#
#
# user_priv_router_2 = Router()
#
# user_priv_router_2.message.filter(ChatTypeFilter(['private']))
#
#
# class AddProduct(StatesGroup):
#     number = State()
#     descrip = State()
#
#     texts = {
#         'AddProduct:number': 'Введите класс заново'
#     }
#
# @user_priv_router_2.message(StateFilter(None), F.text == 'Опрос')
# async def get_poll(message: types.Message, state: FSMContext):
#     await message.answer('В каком ты классе?', reply_markup=types.ReplyKeyboardRemove())
#
#
#     await state.set_state(AddProduct.number)
#
#
# @user_priv_router_2.message(StateFilter('*'), F.text == 'исправить прошлый ответ')
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
#             return
#         previos = step
#
#
#
# @user_priv_router_2.message(AddProduct.number, F.text)
# async def ger_number(message: types.Message, state: FSMContext):
#     await state.update_data(number=message.text)
#     await message.answer(
#         'Расскажи, как ты обычно смотришь свои оценки, расписание, и домашнию работу',
#         reply_markup=fsm_back_2
#     )
#     await state.set_state(AddProduct.descrip)
# @user_priv_router_2.message(AddProduct.number)
# async def ger_number(message: types.Message):
#     await message.answer('False')
#
#
# @user_priv_router_2.message(AddProduct.descrip, F.text)
# async def ger_descrip(message: types.Message, state: FSMContext, session: AsyncSession):
#     global flag
#     await state.update_data(descrip=message.text)
#
#     data = await state.get_data()
#
#     await add_userpoll(session, data)
#
#     await message.answer('Спасибо за ответы', reply_markup=basic_ceyboard_poll)
#     await state.clear()
#
#
# @user_priv_router_2.message(AddProduct.descrip)
# async def ger_descrip(message: types.Message):
#     await message.answer('False')