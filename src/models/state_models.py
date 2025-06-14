from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StatesGroup, State




class ReflectionModel(StatesGroup):
    evaluations = State()
    positive_moments = State()
    growth_points = State()
    