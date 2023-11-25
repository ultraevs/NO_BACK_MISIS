import telebot
from telebot import types
import sqlite3
import time
import datetime
import logging

logging.basicConfig(level=logging.INFO, filename="work.log",filemode="a", format="%(asctime)s | %(message)s")
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("TeleBot").setLevel(logging.CRITICAL)

token = "6501834764:AAFqw4SebhVrGgNV0ZkA9lMUmuiOb_l6Yok"

connection = sqlite3.connect('main3.db', check_same_thread=False)
cursor = connection.cursor()

admin_ids = ["763251313", "726906960", "896614392"]

cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chat_id INTEGER UNIQUE,
                    active_ticket_id INTEGER,
                    winline_id INTEGER,
                    menu_msg_id INTEGER
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS reports (
                    report_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    winline_id TEXT,
                    report_text TEXT,
                    status TEXT,
                    admin_answer TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )''')


bot = telebot.TeleBot(token)

logging.info(f"Launched.")

@bot.message_handler()
def menu(message):
    logging.info(f'{message.chat.id} | {message.from_user.first_name} | @{message.from_user.username} | -> {message.text}')

    cursor.execute("SELECT chat_id FROM users WHERE chat_id=?", (message.chat.id,))
    user_exists = cursor.fetchone()

    if user_exists is None:
        cursor.execute("INSERT INTO users (chat_id) VALUES (?)", (message.chat.id,))
        connection.commit()
        logging.info(f"{message.chat.id} | {message.from_user.first_name} -> новый пользователь")

    # check for active tickets

    cursor.execute("SELECT active_ticket_id FROM users WHERE chat_id=?", (message.chat.id,))
    active_ticket_id = cursor.fetchone()[0]
    if active_ticket_id != None:
        cursor.execute(f"SELECT status FROM reports WHERE report_id=?", (active_ticket_id,))
        try:
            status = cursor.fetchone()[0]
        except:
            status = None
    
    elif active_ticket_id == 'None':
        status = None
    else:
        status = None

    if status == 'closed' or status == None:
        markups = types.InlineKeyboardMarkup()
        button_create = types.InlineKeyboardButton("Создать тикет", callback_data='create_ticket')
        
        if str(message.chat.id) in admin_ids:
            button_admin = types.InlineKeyboardButton("Админка", callback_data='admin')
            markups.row(button_create, button_admin)
        else:
            markups.row(button_create)
        menu_msg = bot.send_message(message.chat.id, "У вас нет активных тикетов.", reply_markup=markups)
        cursor.execute(f"UPDATE users SET menu_msg_id='{str(menu_msg.id)}' WHERE chat_id='{str(message.chat.id)}'")
        connection.commit()
    else:
        cursor.execute(f"SELECT report_text FROM reports WHERE report_id='{active_ticket_id}'")
        text = cursor.fetchone()[0]
        if str(message.chat.id) in admin_ids:
            markups = types.InlineKeyboardMarkup()
            button_admin = types.InlineKeyboardButton("Админка", callback_data='admin')
            markups.add(button_admin)
            bot.send_message(message.chat.id, f"У вас уже есть активный тикет.\n\n{text}", reply_markup=markups)
        else:
            bot.send_message(message.chat.id, f"У вас уже есть активный тикет.\n\n{text}")




@bot.callback_query_handler(func=lambda callback: True)
def callback_handler(callback):
    if callback.data == 'create_ticket':
        logging.info(f"{callback.from_user.id} | {callback.from_user.first_name} -> создает тикет")
        cursor.execute(f"SELECT menu_msg_id from users WHERE chat_id='{callback.from_user.id}'")
        menu_msg_id = cursor.fetchone()
        cursor.execute(f"SELECT winline_id FROM users WHERE chat_id='{callback.from_user.id}'")
        winline_id = cursor.fetchone()[0]
        
        markups = types.InlineKeyboardMarkup()
        button_set_id = types.InlineKeyboardButton("Указать", callback_data='set_winline')
        if winline_id == None:
            markups.row(button_set_id)
        else:
            button_use_id = types.InlineKeyboardButton(str(winline_id), callback_data='use_winline')
            markups.row(button_set_id, button_use_id)

        bot.edit_message_text('Ваша почта?', callback.from_user.id, menu_msg_id[0], reply_markup=markups)
    
    if callback.data == 'set_winline':
        logging.info(f"{callback.from_user.id} | {callback.from_user.first_name} -> указывает Winline ID")
        cursor.execute(f"SELECT menu_msg_id from users WHERE chat_id='{callback.from_user.id}'")
        menu_msg_id = cursor.fetchone()
        message = bot.edit_message_text('Напишите вашу почту', callback.from_user.id, menu_msg_id[0], reply_markup=None)
        bot.register_next_step_handler(message, set_winline)
    
    if callback.data == 'use_winline':
        logging.info(f"{callback.from_user.id} | {callback.from_user.first_name} -> использует Winline ID")
        winline_id = callback.message.json['reply_markup']['inline_keyboard'][0][1]['text']
        menu_msg_id = cursor.execute(f"SELECT menu_msg_id FROM users WHERE chat_id='{callback.from_user.id}'").fetchall()[0]
        
        message = bot.edit_message_text(f'Почта: {winline_id}\n\nВведите текст репорта', callback.from_user.id, menu_msg_id, reply_markup=None)
        bot.register_next_step_handler(message, input_text, winline_id)

    if callback.data == 'send_report':
        cursor.execute(f"SELECT active_ticket_id FROM users WHERE chat_id='{callback.from_user.id}'")
        ticket_id = cursor.fetchone()[0]

        cursor.execute(f"UPDATE reports SET status='open' WHERE report_id='{ticket_id}'")
        connection.commit()

        cursor.execute(f"SELECT menu_msg_id from users WHERE chat_id='{callback.from_user.id}'")
        menu_msg_id = cursor.fetchone()

        bot.delete_message(callback.from_user.id, menu_msg_id)

        cursor.execute(f"SELECT report_text FROM reports WHERE report_id='{ticket_id}'")
        report_text = cursor.fetchone()[0]
        msg = bot.send_message(callback.from_user.id, f'Репорт отправлен.\n{report_text}')
        logging.info(f"{callback.from_user.id} | {callback.from_user.first_name} -> отправляет репорт")

        cursor.execute(f"UPDATE users SET menu_msg_id='{msg.message_id}' WHERE chat_id='{callback.from_user.id}'")
    
    if callback.data == 'cancel_report':
        logging.info(f"{callback.from_user.id} | {callback.from_user.first_name} -> отменяет репорт")
        cursor.execute(f"UPDATE reports SET status='closed' WHERE user_id='{callback.from_user.id}'")
        connection.commit()

        cursor.execute(f"UPDATE users SET active_ticket_id='None' WHERE chat_id='{callback.from_user.id}'")
        connection.commit()

        cursor.execute(f"SELECT menu_msg_id FROM users WHERE chat_id='{callback.from_user.id}'")
        menu_msg_id = cursor.fetchone()[0]
        bot.delete_message(callback.from_user.id, menu_msg_id)


        markups = types.InlineKeyboardMarkup()
        button_create = types.InlineKeyboardButton("Создать тикет", callback_data='create_ticket')
        
        if str(callback.from_user.id) in admin_ids:
            button_admin = types.InlineKeyboardButton("Админка", callback_data='admin')
            markups.row(button_create, button_admin)
        else:
            markups.row(button_create)
        menu_msg = bot.send_message(callback.from_user.id, "У вас нет активных тикетов.", reply_markup=markups)
        cursor.execute(f"UPDATE users SET menu_msg_id='{str(menu_msg.id)}' WHERE chat_id='{str(callback.from_user.id)}'")
        connection.commit()    
    
    if callback.data == 'admin':
        logging.info(f"{callback.from_user.id} | {callback.from_user.first_name} -> открывает админку")
        cursor.execute("SELECT * FROM reports WHERE status='open'")
        active_tickets = cursor.fetchall()

        cursor.execute(f"SELECT menu_msg_id FROM users WHERE chat_id='{callback.from_user.id}'")
        menu_msg_id = cursor.fetchone()[0]
        
        if not active_tickets:
            markups = types.InlineKeyboardMarkup()
            button_admin = types.InlineKeyboardButton("Обновить", callback_data='admin')
            markups.row(button_admin)
            
            bot.edit_message_text("На данный момент тикетов на проверку нет.\n\nНажмите на кнопочку ниже чуть позже.", callback.from_user.id, menu_msg_id, reply_markup=markups)
            logging.info(f"{callback.from_user.id} | {callback.from_user.first_name} -> нет тикетов для админа")
        else:
            active_ticket = active_tickets[0]
            ticket_id, user_id, winline_id, report_text, status, admin_answer = active_ticket
            markups = types.InlineKeyboardMarkup()
            button_answer = types.InlineKeyboardButton('Ответить', callback_data=f'answerr_{ticket_id}')
            button_cancel_answer = types.InlineKeyboardButton('Удалить', callback_data=f'deletee_{ticket_id}')
            markups.add(button_answer, button_cancel_answer)
            try:
                bot.delete_message(callback.from_user.id, menu_msg_id)
            except: None
            msg = bot.send_message(callback.from_user.id, f"Тикетов в очереди: {len(active_tickets)}\nТикет №{ticket_id}\n\n{report_text}", reply_markup=markups)
            cursor.execute(f"UPDATE users SET menu_msg_id='{msg.message_id}' WHERE chat_id='{callback.from_user.id}'")
            connection.commit()
            cursor.execute("UPDATE reports SET status='in operation' WHERE report_id=?", (ticket_id,))
            connection.commit()
            logging.info(f"{callback.from_user.id} | {callback.from_user.first_name} -> начинает отвечать на тикет")

    if 'answerr_' in callback.data:
        logging.info(f"{callback.from_user.id} | {callback.from_user.first_name} -> админ вводит текст ответа")
        ticket_id = callback.data.split('_')[1]

        cursor.execute(f"SELECT * FROM reports WHERE report_id='{ticket_id}'")
        ticket = cursor.fetchall()[0]
        report_id, user_id, winline_id, report_text, status, admin_answer = ticket

        cursor.execute(f"SELECT menu_msg_id FROM users WHERE chat_id='{callback.from_user.id}'")
        menu_msg_id = cursor.fetchone()[0]

        message = bot.edit_message_text(f"{report_text}\n\nВведите текст ответа.", callback.from_user.id, menu_msg_id, reply_markup=None)
        bot.register_next_step_handler(message, confirm_reply, ticket, menu_msg_id)
    if 'deletee_' in callback.data:
        logging.info(f"{callback.from_user.id} | {callback.from_user.first_name} -> админ удаляет тикет")
        ticket_id = callback.data.split('_')[1]

        cursor.execute(f"SELECT * FROM reports WHERE report_id='{ticket_id}'")
        ticket = cursor.fetchall()[0]
        report_id, user_id, winline_id, report_text, status, admin_answer = ticket

        cursor.execute(f"SELECT menu_msg_id FROM users WHERE chat_id='{user_id}'")
        menu_msg_id = cursor.fetchone()[0]

        cursor.execute(f"UPDATE reports SET status='closed' WHERE report_id='{report_id}'")
        connection.commit()
        cursor.execute(f"UPDATE users SET active_ticket_id='None' WHERE chat_id='{user_id}'")
        connection.commit()

        bot.send_message(user_id, "Ваш репорт был удален администратором.\n\nОтправить новый: /start")

        cursor.execute(f"SELECT menu_msg_id FROM users WHERE chat_id='{callback.from_user.id}'")
        menu_msg_id = cursor.fetchone()[0]

        cursor.execute("SELECT * FROM reports WHERE status='open'")
        active_tickets = cursor.fetchall()

        cursor.execute(f"SELECT menu_msg_id FROM users WHERE chat_id='{callback.from_user.id}'")
        menu_msg_id = cursor.fetchone()[0]
        
        if not active_tickets:
            markups = types.InlineKeyboardMarkup()
            button_admin = types.InlineKeyboardButton("Обновить", callback_data='admin')
            markups.row(button_admin)
            
            bot.edit_message_text("На данный момент тикетов на проверку нет.\n\nНажмите на кнопочку ниже чуть позже.", callback.from_user.id, menu_msg_id, reply_markup=markups)
            logging.info(f"{callback.from_user.id} | {callback.from_user.first_name} -> нет тикетов на проверку")
        else:
            active_ticket = active_tickets[0]
            ticket_id, user_id, winline_id, report_text, status, admin_answer = active_ticket
            markups = types.InlineKeyboardMarkup()
            button_answer = types.InlineKeyboardButton('Ответить', callback_data=f'answer_{ticket_id}')
            button_cancel_answer = types.InlineKeyboardButton('Удалить', callback_data=f'delete_{ticket_id}')
            markups.add(button_answer, button_cancel_answer)
            bot.edit_message_text(f"Тикетов в очереди: {len(active_tickets)}\nТикет №{ticket_id}\n\n{report_text}", callback.from_user.id, menu_msg_id, reply_markup=markups)
            cursor.execute("UPDATE reports SET status='in operation' WHERE report_id=?", (ticket_id,))
            connection.commit()
            logging.info(f"{message.chat.id} | {message.from_user.first_name} -> начинает отвечать на тикет")
    
    if 'confirm_answer_' in callback.data:
        ticket_id = callback.data.split('confirm_answer_')[1]

        cursor.execute(f"SELECT * FROM reports WHERE report_id='{ticket_id}'")
        ticket = cursor.fetchone()
        report_id, user_id, winline_id, report_text, status, admin_answer = ticket

        cursor.execute(f"SELECT menu_msg_id FROM users WHERE chat_id='{callback.from_user.id}'")
        menu_msg_id = cursor.fetchone()[0]

        cursor.execute(f"UPDATE reports SET status='closed' WHERE report_id='{ticket_id}'")
        connection.commit()
        cursor.execute(f"UPDATE users SET active_ticket_id='None' WHERE chat_id='{user_id}'")
        connection.commit()
        cursor.execute(f"SELECT admin_answer FROM reports WHERE report_id='{report_id}'")
        answ = cursor.fetchone()[0]
        logging.info(f"{callback.from_user.id} | {callback.from_user.first_name} -> отправил ответ на тикет [{report_id}]")
        bot.send_message(user_id, f"Получен ответ:\n\n{answ}\n\nСоздать новый репорт: /start")

        cursor.execute("SELECT * FROM reports WHERE status='open'")
        active_tickets = cursor.fetchall()

        cursor.execute(f"SELECT menu_msg_id FROM users WHERE chat_id='{callback.from_user.id}'")
        menu_msg_id = cursor.fetchone()[0]
        
        if not active_tickets:
            markups = types.InlineKeyboardMarkup()
            button_admin = types.InlineKeyboardButton("Обновить", callback_data='admin')
            markups.row(button_admin)
            
            bot.edit_message_text("На данный момент тикетов на проверку нет.\n\nНажмите на кнопочку ниже чуть позже.", callback.from_user.id, menu_msg_id, reply_markup=markups)
            logging.info(f"{callback.from_user.id} | {callback.from_user.first_name} -> нет тикетов на проверку")
        else:
            active_ticket = active_tickets[0]
            ticket_id, user_id, winline_id, report_text, status, admin_answer = active_ticket
            markups = types.InlineKeyboardMarkup()
            button_answer = types.InlineKeyboardButton('Ответить', callback_data=f'answerr_{ticket_id}')
            button_cancel_answer = types.InlineKeyboardButton('Удалить', callback_data=f'deletee_{ticket_id}')
            markups.add(button_answer, button_cancel_answer)
            bot.edit_message_text(f"Тикетов в очереди: {len(active_tickets)}\nТикет №{ticket_id}\n\n{report_text}", callback.from_user.id, menu_msg_id, reply_markup=markups)
            cursor.execute("UPDATE reports SET status='in operation' WHERE report_id=?", (ticket_id,))
            connection.commit()
            logging.info(f"{callback.from_user.id} | {callback.from_user.first_name} -> начинает отвечать на тикет")

    if 'change_answer_' in callback.data:
        logging.info(f"{callback.from_user.id} | {callback.from_user.first_name} -> изменяет ответ на тикет")
        ticket_id = callback.data.split('ge_answer_')[1]
        cursor.execute(f"SELECT menu_msg_id FROM users WHERE chat_id='{callback.from_user.id}'")
        menu_msg_id = cursor.fetchone()[0]
        cursor.execute(f"SELECT * FROM reports WHERE report_id='{ticket_id}'")
        ticket = cursor.fetchall()[0]
        report_id, user_id, winline_id, report_text, status, admin_answer = ticket

        message = bot.edit_message_text(f"{report_text}\n\nПредыдущий ответ:\n{admin_answer}\n\nВведите новый ответ.", callback.from_user.id, menu_msg_id)
        bot.register_next_step_handler(message, change_answer, menu_msg_id, ticket)

def change_answer(message, menu_msg_id, ticket):
    report_id, user_id, winline_id, report_text, status, admin_answer = ticket
    bot.delete_message(message.chat.id, message.message_id)
    cursor.execute(f"UPDATE reports SET admin_answer='{message.text}' WHERE report_id='{report_id}'")
    connection.commit()

    markups = types.InlineKeyboardMarkup()
    button_confirm_answer = types.InlineKeyboardButton('Отправить', callback_data=f'confirm_answer_{report_id}')

    button_change_answer = types.InlineKeyboardButton('Изменить', callback_data=f'change_answer_{report_id}')
    markups.add(button_confirm_answer, button_change_answer)
    bot.edit_message_text(f'{report_text}\n\nВаш ответ:\n{message.text}', message.chat.id, menu_msg_id, reply_markup=markups)
    logging.info(f"{message.chat.id} | {message.from_user.first_name} -> изменил ответ на тикет")
    


def confirm_reply(message, ticket, menu_msg_id):
    bot.delete_message(message.chat.id, message.message_id)
    report_id, user_id, winline_id, report_text, status, admin_answer = ticket
    cursor.execute(f"UPDATE reports SET admin_answer='{message.text}' WHERE report_id='{report_id}'")
    connection.commit()

    markups = types.InlineKeyboardMarkup()
    button_confirm_answer = types.InlineKeyboardButton('Отправить', callback_data=f'confirm_answer_{report_id}')

    button_change_answer = types.InlineKeyboardButton('Изменить', callback_data=f'change_answer_{report_id}')
    markups.add(button_confirm_answer, button_change_answer)
    bot.edit_message_text(f'{report_text}\n\nВаш ответ:\n{message.text}', message.chat.id, menu_msg_id, reply_markup=markups)
    logging.info(f"{message.chat.id} | {message.from_user.first_name} -> изменил ответ на тикет")

def input_text(message, winline_id):
    bot.delete_message(message.chat.id, message.message_id)
    cursor.execute(f"SELECT menu_msg_id from users WHERE chat_id='{message.chat.id}'")
    menu_msg_id = cursor.fetchone()

    markups = types.InlineKeyboardMarkup()
    button_send = types.InlineKeyboardButton("Отправить", callback_data='send_report')
    button_cancel = types.InlineKeyboardButton("Отмена", callback_data='cancel_report')
    markups.add(button_send, button_cancel)

    txt = f'Почта: {winline_id}\n\n{message.text}'

    cursor.execute("INSERT INTO reports (user_id, report_text, winline_id, status) VALUES (?, ?, ?, ?)", (message.chat.id, txt, winline_id, 'opening'))
    connection.commit()

    cursor.execute("SELECT last_insert_rowid()")
    report_id = cursor.fetchone()[0]

    cursor.execute("UPDATE users SET active_ticket_id=? WHERE chat_id=?", (report_id, message.chat.id))
    connection.commit()

    logging.info(f"{message.chat.id} | {message.from_user.first_name} -> выбирает отправлять ли репорт")

    bot.edit_message_text(txt, message.chat.id, menu_msg_id, reply_markup=markups)



def set_winline(message):
    bot.delete_message(message.chat.id, message.message_id)
    if 1:
        cursor.execute("UPDATE users SET winline_id = ? WHERE chat_id = ?", (message.text, message.from_user.id))
        connection.commit()


        cursor.execute(f"SELECT menu_msg_id from users WHERE chat_id='{message.chat.id}'")
        menu_msg_id = cursor.fetchone()

        cursor.execute(f"SELECT winline_id FROM users WHERE chat_id='{message.chat.id}'")
        winline_id = cursor.fetchone()[0]

        markups = types.InlineKeyboardMarkup()
        button_set_id = types.InlineKeyboardButton("Указать", callback_data='set_winline')
        if winline_id == None:
            markups.row(button_set_id)
        else:
            button_use_id = types.InlineKeyboardButton(str(winline_id), callback_data='use_winline')
            markups.row(button_set_id, button_use_id)

        logging.info(f"{message.chat.id} | {message.from_user.first_name} -> выбирает Winline ID")
        bot.edit_message_text('Почта?', message.chat.id, menu_msg_id[0], reply_markup=markups)



while True:
    try:
        bot.infinity_polling()
    except:
        time.sleep(5)
        logging.error(f"Произошла ошибка в работе бота, перезапуск...")