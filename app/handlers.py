import asyncio
from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from app.tasks.Tasks import Tasks
from app.learning.Learning import Learning
from app.questions.Questions import Questions
from app.resources.Resources import Resources
import app.keyboards as kb


# initializing
router = Router()
user_mes_text = F.text
user_mes_data = F.data.split()
learning_obj = Learning()
questions_obj = Questions()
resources_obj = Resources()


async def send_notifications(bot):
    while True:
        users = Tasks.get_users()
        for i in range(len(users)):
            active_dct = Tasks.get_active_tasks(users[i])
            if active_dct:
                await bot.send_message(int(users[i]), "У вас есть незавершённые задачи👀!")
            await asyncio.sleep(60*60)


# start
@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f"Привет!\nЯ был создан для бизнеса.", reply_markup=kb.main)


# learning
@router.message(user_mes_text == "📖обучение📖")
async def help_for_user(message: Message):
    await message.answer("Выберите урок.", reply_markup=kb.kb_for_lessons)
    # asyncio.create_task(send_notifications())

@router.callback_query(user_mes_data[0] == "get_lesson")
async def choose_task(callback: CallbackQuery):
    lesson_key = callback.data.split()[1]
    await callback.message.edit_text(learning_obj.get_lesson(lesson_key), reply_markup=kb.back_to_lessons_kb)

# tasks
@router.message(user_mes_text == "📌задачи📌")
async def help_for_user(message: Message):
    await message.answer("Планировщик задач:", reply_markup=kb.tasks)
    
@router.callback_query(user_mes_data[0] == "choose_task")
async def choose_task(callback: CallbackQuery):
    await callback.message.edit_text("Выберите тип задач.", reply_markup=kb.tasks_types)

@router.callback_query(user_mes_data[0] == "day_tasks")
async def get_day_tasks(callback: CallbackQuery):
    await callback.message.edit_text("Выберите задачи.", reply_markup=kb.tasks_day)

@router.callback_query(user_mes_data[0] == "week_tasks")
async def get_week_tasks(callback: CallbackQuery):
    await callback.message.edit_text("Выберите задачи.", reply_markup=kb.tasks_week)

@router.callback_query(user_mes_data[0] == "choose_start")
async def choose_start(callback: CallbackQuery):
    second_part = callback.data.split()[1]
    await callback.message.edit_text("Начать задачу?", reply_markup=kb.start_kbs[second_part])

@router.callback_query(user_mes_data[0] == "start")
async def start(callback: CallbackQuery):
    second_part = callback.data.split()[1]
    await callback.answer("Вы начали задачу!", show_alert=True)
    Tasks.start_task(str(callback.from_user.id), second_part)

@router.callback_query(user_mes_data[0] == "get_active_tasks")
async def get_active_tasks(callback: CallbackQuery):
    active_tasks_dct = Tasks.get_active_tasks(str(callback.from_user.id))
    if active_tasks_dct:
        await callback.message.edit_text("Активные задачи: ", reply_markup=await kb.get_kb_with_active_tasks(active_tasks_dct))
    else:
        await callback.message.edit_text("У вас нет активных задач.", reply_markup=kb.empty_active_kb)
        
@router.callback_query(user_mes_data[0] == "choose_finish")
async def choose_finish(callback: CallbackQuery):
    second_part = callback.data.split()[1]
    await callback.message.edit_text("Завершить задачу?", reply_markup=await kb.get_finish_kb(second_part))

@router.callback_query(user_mes_data[0] == "finish")
async def finish(callback: CallbackQuery):
    second_part = callback.data.split()[1]
    await callback.answer("Вы завершили задачу!", show_alert=True)
    Tasks.finish_task(str(callback.from_user.id), second_part)

# resources
@router.message(user_mes_text == "📈ресурсы📈")
async def help_for_user(message: Message):
    await message.answer("Выберите тему.", reply_markup=kb.resources_kb)

@router.callback_query(user_mes_data[0] == "get_resources_advice")
async def choose_task(callback: CallbackQuery):
    resources_key = callback.data.split()[1]
    await callback.message.edit_text(resources_obj.get_question(resources_key), reply_markup=kb.back_to_resources_kb)

# questions
@router.message(user_mes_text == "❓вопросы❓")
async def help_for_user(message: Message):
    await message.answer("Выберите вопрос.", reply_markup=kb.questions_kb)

@router.callback_query(user_mes_data[0] == "get_question")
async def choose_task(callback: CallbackQuery):
    question_key = callback.data.split()[1]
    await callback.message.edit_text(questions_obj.get_question(question_key), reply_markup=kb.back_to_questions_kb)

# help
@router.message(user_mes_text == "📃помощь📃")
async def help_for_user(message: Message):
    await message.answer("📖обучение📖 - уроки бизнеса \n📌задачи📌 - задачи \n📈ресурсы📈 - управление ресурсами \n❓вопросы❓ - выберите вариант вопроса")

# getting back
@router.callback_query(user_mes_data[0] == "back")
async def back(callback: CallbackQuery):
    if callback.data.split()[1] == "to_task_planer":
        await callback.message.edit_text("Планировщик задач:", reply_markup=kb.tasks)
    elif callback.data.split()[1] == "to_types_of_tasks":
        await callback.message.edit_text("Выберите тип задач.", reply_markup=kb.tasks_types)
    elif callback.data.split()[1] == "to_day_tasks":
        await callback.message.edit_text("Выберите задачи.", reply_markup=kb.tasks_day)
    elif callback.data.split()[1] == "to_week_tasks":
        await callback.message.edit_text("Выберите задачи.", reply_markup=kb.tasks_week)
    elif callback.data.split()[1] == "to_lessons":
        await callback.message.edit_text("Выберите урок.", reply_markup=kb.kb_for_lessons)
    elif callback.data.split()[1] == "to_questions":
        await callback.message.edit_text("Выберите вопрос.", reply_markup=kb.questions_kb)
    elif callback.data.split()[1] == "to_resources":
        await callback.message.edit_text("Выберите тему.", reply_markup=kb.resources_kb)
    elif callback.data.split()[1] == "to_active_tasks":
        active_tasks_dct = Tasks.get_active_tasks(str(callback.from_user.id))
        if active_tasks_dct:
            await callback.message.edit_text("Активные задачи: ", reply_markup=await kb.get_kb_with_active_tasks(active_tasks_dct))
        else:
            await callback.message.edit_text("У вас нет активных задач.", reply_markup=kb.empty_active_kb)
        
# incorresct input
@router.message(user_mes_text != "📖обучение📖" and F.text != "📌задачи📌" and F.text != "📈ресурсы📈" and F.text != "❓вопросы❓" and F.text != "📃помощь📃")
async def reply(message: Message):
    await message.answer("↘Выберите один из вариантов ответов ниже↙")
