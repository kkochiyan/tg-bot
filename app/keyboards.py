from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.database.requests import get_cities


main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Посмотреть погоду в городе', callback_data='submenu')],
    [InlineKeyboardButton(text='Написать в тех поддержку', callback_data='technical_support')]
])

submenu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Ввести город', callback_data='new city')],
    [InlineKeyboardButton(text='Сохраненные города', callback_data='save cities')],
    [InlineKeyboardButton(text='Назад в меню', callback_data='back')]
])

save_or_no = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Да', callback_data='Yes'), InlineKeyboardButton(text='Нет', callback_data='No')]
])

async def cities(tg_id):
    all_cities = await get_cities(tg_id)
    keyboard = InlineKeyboardBuilder()

    for city in all_cities:
        keyboard.add(InlineKeyboardButton(text=city.name, callback_data=f'city_{city.name}'))

    keyboard.add(InlineKeyboardButton(text='Назад', callback_data='submenu'), InlineKeyboardButton(text='Вернуться в главное меню', callback_data='back'))
    return keyboard.adjust(2).as_markup()

save_city_or_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Сохраненные города', callback_data='save cities')],
    [InlineKeyboardButton(text='Главное меню', callback_data='back')]
])


