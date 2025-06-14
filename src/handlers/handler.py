import json

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from docx import Document

from .file_operations import FilePhrases, WordDocument
from ..models.state_models import ReflectionModel


router_base = Router()
word_doc_obj = WordDocument()

@router_base.message(CommandStart())
async def start(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text='Готовые фразочки',
            callback_data='phrases'
        ),
        types.InlineKeyboardButton(
            text='Начать писать рефлексию',
            callback_data='start_write_ref'
        )
    )
    await message.answer(
        FilePhrases.get_phrase_when_start_bot('prepared_phrases.json'),
        reply_markup=builder.as_markup()
    )


@router_base.callback_query(F.data == 'start_write_ref')
async def start_write_ref(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(
        FilePhrases.stages_ref_text('prepared_phrases.json', 'first')
    )
    await state.set_state(ReflectionModel.evaluations)


@router_base.callback_query(F.data == 'phrases')
async def callback_phrases(callback: types.CallbackQuery):
    await callback.message.answer(
        FilePhrases.display_beautiful_format('prepared_phrases.json')
    )


@router_base.message(F.text, ReflectionModel.evaluations)
async def get_evaluations(message: types.Message, state: FSMContext):
    await state.update_data(evaluations=message.text)
    await message.answer(
        FilePhrases.stages_ref_text('prepared_phrases.json', 'second')
    )
    await state.set_state(ReflectionModel.positive_moments)


@router_base.message(F.text, ReflectionModel.positive_moments)
async def get_evaluations(message: types.Message, state: FSMContext):
    await state.update_data(positive_moments=message.text)
    await message.answer(
        FilePhrases.stages_ref_text('prepared_phrases.json', 'third')
    )
    await state.set_state(ReflectionModel.growth_points)


@router_base.message(F.text, ReflectionModel.growth_points)
async def get_evaluations(
    message: types.Message,
    state: FSMContext,
    word_doc: WordDocument = word_doc_obj):
    await state.update_data(growth_points=message.text)
    data = await state.get_data()
    result_text = f'''
        Оценки: {data.get('evaluations')}
        Позитивные моменты: {data.get('positive_moments')}
        Точки роста: {data.get('growth_points')}
        '''
    word_doc.add_text_document(result_text, message.from_user.full_name)
    await message.answer('Отлично. Ваши ответы записаны в документ \n\n'
                         + result_text)
    await state.clear()
    