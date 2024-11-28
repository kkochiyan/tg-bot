from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
import app.keyboards as kb
import app.database.requests as rq
from app.States import tech_sup as ts
from app.States import new_city as ns
from app.requests_to_api import get_weather, get_saves_weathers


router = Router()

@router.message(CommandStart())
async def start(message: Message):
    await message.answer('Привет!\nЯ бот, который показывает погоду в веденном городе.\nВыберите действие',
                         reply_markup=kb.main)

@router.callback_query(F.data == 'technical_support')
async def technical_support(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ts.mes)
    await callback.answer()
    await callback.message.answer('Напишите сообщение в чат поддержки')

@router.message(ts.mes)
async def technical_support_message(message: Message, state: FSMContext):
    await message.answer(f'Сообщение : ' + message.text + ' успешно отправлено!')
    await message.bot.send_message(1023848547,
                                   f"ID: {message.from_user.id}\nИмя: {message.from_user.first_name}\nСообщение: {message.text}")
    await message.answer('Вы в меню\nВыберите действие', reply_markup=kb.main)
    await state.clear()

@router.callback_query(F.data == 'submenu')
async def submenu(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text('Выберите действие', reply_markup=kb.submenu)

@router.callback_query(F.data == 'back')
async def back(callback: CallbackQuery):
    await callback.answer('Вы переместились в меню')
    await callback.message.edit_text('Вы в меню\nВыберите действие', reply_markup=kb.main)

@router.callback_query(F.data == 'new city')
async def new_city(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ns.city)
    await callback.answer()
    await callback.message.answer('Введите название города и я выведу текущую погоду в нем')

@router.message(ns.city)
async def new_city_name(message: Message, state: FSMContext):
    city = message.text
    await state.update_data(city=city)
    mes1, mes2, keybord = get_weather(city)
    await message.answer(mes1)
    await message.answer(mes2, reply_markup=keybord)


@router.callback_query(F.data == 'No')
async def no_save(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()
    await callback.message.edit_text('Выберите действие', reply_markup=kb.submenu)

@router.callback_query(F.data == 'Yes')
async def yes_save(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = callback.from_user.id
    city_name = data['city']
    await state.clear()
    await rq.set_user(user_id)
    await rq.set_city(city_name)
    await rq.set_pair(user_id, city_name)
    await callback.answer('Город успешно добавлен!')
    await callback.message.edit_text('Выберите действие', reply_markup=kb.submenu)


@router.callback_query(F.data == 'save cities')
async def save_cities(callback: CallbackQuery):
    await callback.answer()
    result = await rq.check(callback.from_user.id)
    if not result:
        await callback.message.edit_text('Вот ваши сохраненные города\nВыберите город, в котором хотите посмотреть погоду',
                                     reply_markup=await kb.cities(callback.from_user.id))
    else:
        await callback.message.answer('У вас еще нет сохраненных городов')
        await callback.message.answer('Выберите действие', reply_markup=kb.submenu)

@router.callback_query(F.data.startswith('city_'))
async def get_city(callback: CallbackQuery):
    await callback.answer()
    city_name = callback.data.split('_')[1]
    mes = get_saves_weathers(city_name)
    await callback.message.answer(mes)
    await callback.message.answer('Выберите действие', reply_markup=kb.save_city_or_menu)

@router.message(F.text)
async def get_text(message: Message):
    await message.reply('Некоректные данные.\nВзаимодействуйте с ботом через меню!!!\nВыберите действие',
                        reply_markup=kb.main)







