import asyncio
import logging


from datetime import datetime
from aiogram import Bot, Dispatcher, Router, types
from aiogram.utils.keyboard import InlineKeyboardBuilder, KeyboardBuilder, ReplyKeyboardBuilder
from aiogram.filters import Command
from aiogram.types import Message

from database import insert_into_tasks, get_tasks, get_tasks_boolean, delete_task, complete_task


Bot_Token = '6009349109:AAGyX1OEA1dEaf1dcRArthyg2HdYwiE5koA'

router = Router()

@router.message(Command(commands=["start"]))
async def command_start_handler(message):

    await message.answer(f"Здравствуйте, <b>{message.from_user.full_name}!</b> Чтобы узнать больше о боте, воспользуйтесь командой /help")
    
    
@router.message(Command(commands=['all']))
async def command_all_tasks_handler(message):
    a = get_tasks()

    await message.answer('id, name, date, completed')
    for task in a:

        task = list(map(str,task))
        task = " ".join(task)
        await message.answer(task)
    
@router.message(Command(commands=['task']))
async def command_add_task_handler(message):
    msg = message.text.split()
    date = msg[-2] + ' ' + msg[-1]
    name = " ".join(msg[1:-2:])
    dt = datetime.strptime(date, '%Y-%m-%d %H:%M')
    insert_into_tasks([name, date])
    
    await message.answer('Задание добавлено')

@router.message(Command(commands=['uncompleted']))
async def command_uncomplited_handler(message):
    msg = message.text
    d = []

    if msg == '/completed':
        d = get_tasks_boolean('true')
       
    elif msg == '/uncompleted':
        d = get_tasks_boolean('false')
    
    await message.answer('id, name, date, completed')
    for task in d:
        task = list(map(str,task))
        task = " ".join(task)
        await message.answer(task)

@router.message(Command(commands=['completed']))
async def command_completed_uncomplited_handler(message):
    msg = message.text
    d = []


    d = get_tasks_boolean('true')

    
    await message.answer('id, name, date, completed')
    for task in d:
        task = list(map(str,task))
        task = " ".join(task)
        await message.answer(task)
    
@router.message(Command(commands=['del']))
async def command_all_tasks_handler(message):
    msg = message.text.split()[1::]
    
    for id in msg:
        delete_task(int(id))
        await message.answer(f'Задание номер {id} удалено')

@router.message(Command(commands=['done']))
async def command_all_tasks_handler(message):
    msg = message.text.split()[1::]
    
    for id in msg:
        complete_task(int(id))
        await message.answer(f'Задание номер {id} выполнено')


@router.message()
async def msg_handler(message):
    
    try:
        await message.answer('hi')
    except TypeError:
        await message.answer("Nice try!")




async def main():
    dp = Dispatcher()
    dp.include_router(router)
    bot = Bot(Bot_Token, parse_mode="HTML")
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())