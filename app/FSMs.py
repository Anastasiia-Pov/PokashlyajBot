from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext


# FSM для регистрации
class Register(StatesGroup):
    fill_tg_id = State()
    fill_name = State()
    fill_age = State()
    fill_gender = State()
    fill_region = State()


# FSM для анализа кашля
class CoughRecording(StatesGroup):
    record_voice = State()


# FSM для изменения имени
class ChangeName(StatesGroup):
    changed_name = State()


# FSM для изменения возраста
class ChangeAge(StatesGroup):
    changed_age = State()


# FSM для изменения пола
class ChangeGender(StatesGroup):
    changed_gender = State()


# FSM для изменения региона
class ChangeRegion(StatesGroup):
    changed_region = State()
