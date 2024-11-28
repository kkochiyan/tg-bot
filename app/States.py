from aiogram.fsm.state import StatesGroup,State

class tech_sup(StatesGroup):
    mes = State()

class new_city(StatesGroup):
    city = State()