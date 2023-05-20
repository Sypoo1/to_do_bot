import asyncio
import logging
import emoji

from datetime import datetime
from aiogram import Bot, Dispatcher, Router, types
from aiogram.utils.keyboard import InlineKeyboardBuilder, KeyboardBuilder, ReplyKeyboardBuilder
from aiogram.filters import Command
from aiogram.types import Message

from database import insert_into_tasks, get_tasks, get_tasks_boolean, insert_into_hide, complete_task, get_by_id
from logic import which_emoji, sort_by_date, chek_deadline, time_to_complete, time_to_deadline

Bot_Token = '6009349109:AAGyX1OEA1dEaf1dcRArthyg2HdYwiE5koA'

router = Router()

@router.message(Command(commands=["start"]))
async def command_start_handler(message):

    await message.answer(f"Здравствуйте, <b>{message.from_user.full_name}!</b> Чтобы узнать больше о боте, воспользуйтесь командой /help")
    
    
@router.message(Command(commands=["time"]))
async def command_time_handler(message):
    try:
        kb = [

            [
                types.KeyboardButton(text="На сегодня"),
                types.KeyboardButton(text="На неделю") 
            ],
            [
                types.KeyboardButton(text="На месяц"),
                types.KeyboardButton(text="На год") 
            ]
        ]
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True,
            input_field_placeholder='Выберите задания на какой этап вы хотите увидеть'
        )
        await message.answer('Какие какой этап?' , reply_markup=keyboard)
    except:
        await message.answer('Команда /time не сработала')

@router.message(Command(commands=["print"]))
async def command_print_handler(message):
    try:
        kb = [
            [
                types.KeyboardButton(text="Все задания")
            ],
            [
                types.KeyboardButton(text="Только завершенные" + emoji.emojize("✅")),
                types.KeyboardButton(text="Только незавершенные" + emoji.emojize("❌")) 
            ],
            [
                types.KeyboardButton(text="Пропущен дедлайн☠")
            ]
        ]
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True,
            input_field_placeholder='Выберите какие задания вы хотите увидеть'
        )
        await message.answer('Какие задания вывести?' , reply_markup=keyboard)
    except:
        await message.answer('Команда /print не сработала')

@router.message(Command(commands=['all']))
async def command_all_tasks_handler(message):
    try:
        a = get_tasks()
        if len(a) == 0:
            await message.answer('Заданий нет')
            
        else:
            a = sort_by_date(a)
            await message.answer('id, name, date, completed')

            for task in a:

                if chek_deadline(task):
                    task = list(map(str,task))
                    task = which_emoji(task)
                    task = " ".join(task)
                    await message.answer(task)
                else:
                    task = list(map(str,task))
                    task = which_emoji(task)
                    task = " ".join(task)
                    await message.answer(f'<s>{task}!</s>')
    except:
        await message.answer('Команда /all не сработала')
    
@router.message(Command(commands=['task']))
async def command_add_task_handler(message):
    try:
        msg = message.text.split()
        date = msg[-2] + ' ' + msg[-1]
        name = " ".join(msg[1:-2:])
        dt = datetime.strptime(date, '%Y-%m-%d %H:%M')
        insert_into_tasks([name, date])
        
        await message.answer('Задание добавлено')
    except:
        await message.answer('Команда /task не сработала')

@router.message(Command(commands=['uncompleted']))
async def command_uncompleted_handler(message):
    try:
        d = get_tasks_boolean('false')
        if len(d) == 0:
            await message.answer('Таких заданий нет')
        else:
            
            d = sort_by_date(d)
            
            await message.answer('id, name, date, completed')
            
            for task in d:
                task = list(map(str,task))
                task = which_emoji(task)
                task = " ".join(task)
                await message.answer(task)
    except:
        await message.answer('Команда /uncompleted не сработала')

@router.message(Command(commands=['help']))
async def command_help_handler(message):
    try:
        a = ['/print Отображает клавиатуру с командами для вывода заданий',
             '/all Выводит все задания',
             '/completed Выводит все завершенные задания ', '/uncompleted Выводит все незавершенные задания',
             '/done Делает задание завершенным \n Пример использования: \n /done 2 3 \n Делает 2-ое и 3-е задание завершенными',
             '/del Удаляет задание \n Пример использования: \n /del 2 3 \n Удаляет 2-ое и 3-е',
             '/task Добавляет задание \n Пример использования: \n /task Пробежать 10 метров 2023-05-21 19:30 \n Добавляет невыполненное задание "Пробежать 10 метров" \n С дедлайном "2023-05-21 19:30"',
             '/dead Отображает невыполненные задания с пропущенным дедлайном☠',
             '/to_dead Отображает сколько часов и минут осталось до дедлайна \n Пример использования: \n /to_dead 6 7 \n Показывает сколько времени осталось до \n дедлайнов 6-го и 7-го задания',
             '/today Выводит задания на сегодня',
             '/week Выводит задания на неделю',
             '/month Выводит задания на месяц',
             '/year Выводт задания на год',
             '/time Выводит клавиатуру с предудыщими 4 командами']
        for item in a:
            await message.answer(item)
        
    except:
        await message.answer('Команда /help не сработала')

@router.message(Command(commands=['completed']))
async def command_completed_handler(message):
    try:
        d = get_tasks_boolean('true')
        if len(d) == 0:
            await message.answer('Таких заданий нет')
        else:
            
            d = sort_by_date(d)
            
            await message.answer('id, name, date, completed')
            
            for task in d:
                task = list(map(str,task))
                task = which_emoji(task)
                task = " ".join(task)
                await message.answer(task)
    except:
        await message.answer('Команда /completed не сработала')
    
@router.message(Command(commands=['del']))
async def command_del_task_handler(message):
    try:
        msg = message.text.split()[1::]
        for id in msg:
            insert_into_hide(int(id))
            await message.answer(f'Задание номер {id} удалено')
    except:
        await message.answer('Команда /del не сработала')

@router.message(Command(commands=['done']))
async def command_done_tasks_handler(message):

    try:
        msg = message.text.split()[1::]
        for id in msg:
            complete_task(int(id))
            await message.answer(f'Задание номер {id} выполнено')
    except:
        await message.answer('Команда /done не сработала')


@router.message(Command(commands=['dead']))
async def command_dead_handler(message):
    try:
        a = get_tasks_boolean('false')
        if len(a) == 0:
            await message.answer('Заданий нет')
            
        else:
            a = sort_by_date(a)
            await message.answer('id, name, date, completed')

            for task in a:

                if not chek_deadline(task):
                    task[3] = emoji.emojize("☠")
                    task = list(map(str,task))
                    task = which_emoji(task)
                    task = " ".join(task)
                    await message.answer(task)

    except:
        await message.answer('Команда /dead не сработала')


@router.message(Command(commands=['today', 'week', 'month', 'year']))
async def command_today_handler(message):
    try:
        
        a = get_tasks_boolean('false')

        msg = message.text 
        print(msg)
        if msg in ['/today', 'На сегодня']:
            a = time_to_complete(0,a)
        elif msg in ['/week', 'На неделю']:
            a = time_to_complete(7,a)
        elif msg in ['/month', 'На месяц']:
            a = time_to_complete(30,a)           
        elif msg in ['/year', 'На год']:
            a = time_to_complete(365,a)

        if len(a) == 0:
            await message.answer('Таких заданий нет')
        else:

            a = sort_by_date(a)

            await message.answer('id, name, date, completed')
            
            for task in a:
                task = list(map(str,task))
                task = which_emoji(task)
                task = " ".join(task)
                await message.answer(task)
            

    except:
        await message.answer(f'Команда {message.text} не сработала')
      

@router.message(Command(commands=['to_dead']))
async def command_to_dead_handler(message):
    try:
        msg = message.text.split()[1::]
        for id in msg:
            
            time = time_to_deadline(get_by_id(id)[0])
            if time == '':
                await message.answer(f'Для задание номер {id} дедлайн закончился')
            else:
                await message.answer(f'До задание номер {id} осталось {time}')
    except:
        await message.answer(f'Команда /to_dead не сработала')         
@router.message()
async def msg_handler(message):
    try:
        msg = message.text
        if msg == "Все задания":
            await command_all_tasks_handler(message)
        elif msg == "Только завершенные✅":
            await command_completed_handler(message)
        elif msg == "Только незавершенные❌": 
            await command_uncompleted_handler(message)
        elif msg == "Пропущен дедлайн☠":
            await command_dead_handler(message)
        elif msg == "На сегодня":
            await command_today_handler(message)
        elif msg == "На неделю": 
            await command_today_handler(message)
        elif msg == "На месяц":
            await command_today_handler(message)
        elif msg == "На год":
            await command_today_handler(message)
        else: 
            await message.answer('Я вас не понимаю')
    except TypeError:
        await message.answer('Ошибка в типе сообщения')

async def main():
    dp = Dispatcher()
    dp.include_router(router)
    bot = Bot(Bot_Token, parse_mode="HTML")
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())