#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, getopt
import logging

import telebot
from telebot import apihelper, types

help_str = '''Add you contacts to folder. You just need to startup it with your token.
    -t (--token) - Telegram token what you get from botfather
'''

# Remove it
# BOT_TOKEN = '839402464:AAG8d-xLJIssJeyCw14YAmjb5bVUGQoeagc'

# Geted from @socks5_bot. Maybe you need to update this if not worked
apihelper.proxy = {'https':'socks5://174641016:jhivW0uI@orbtl.s5.opennetwork.cc:999'}

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

def get_user_store(full_store, user_id):
    if not user_id in store:
        store[user_id] = {}
    return store[user_id]

def parce_arguments(argv):
    result = [None]
    try:
        opts, _ = getopt.getopt(argv,"ht:", ["token="])
    except getopt.GetoptError:
        print(help_str)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(help_str)
            sys.exit()
        elif opt in ("-t", "--token"):
            result[0] = arg
    return result

def create_folder(store, folder_name):
    if folder_name in store:
        return True

    store[folder_name] = []
    return True

def get_all_folders_names(store):
    result = ''
    for folder in store:
        result += folder + '\n'
    return result

def add_to_folder(store, folder_name, contact_info):
    if not folder_name in store:
        return False

    store[folder_name].append(contact_info)
    return True

def get_folder_content(store, folder_name):
    if not folder_name in store:
        return 'No such folder'

    result = ''
    for content in store[folder_name]:
        result += content + '\n'
    return result

def help_message(bot, message):
    keyboard = ['/create', '/folders', '/add', '/remove', '/delete', '/show']
    buttons = types.ReplyKeyboardMarkup()
    for keybord_item in keyboard:
        btn = types.KeyboardButton(keybord_item)
        buttons.add(btn)

    answer = '''Hello! I\'m a folder bot. I will hold your contacts in folders. 
            So there is a commands i understend:
            1. /create - Create folder
            2. /folders - Show folders
            3. /add - Add contact to folder
            4. /remove - Remove contact to folder
            5. /delete - Delete folder
            6. /show - Show contacts in folder
            7. /help - Show this message'''
    bot.send_message(message.chat.id, answer, reply_markup = buttons)

# Enable log there if you need to
# logger = telebot.logger
# telebot.logger.setLevel(logging.DEBUG) # Outputs debug messages to console.

if __name__ == '__main__':
    arguments = parce_arguments(sys.argv[1:])
    if None == arguments[0]:
        print(help_str)
        sys.exit(2)

    store = {}

    token = arguments[0]
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=['start', 'help'])
    def start(message):
        get_user_store(store, message.chat.id)
        help_message(bot, message)


    @bot.message_handler(commands=['create'])
    def create(message):
        splited_message = message.text.split(' ')
        if 2 > len(splited_message):
            bot.send_message(message.chat.id, 'You need to use command with folder name like:\n/create [folder_name]')
            return

        user_store = get_user_store(store, message.chat.id)
        folder_name = splited_message[1]
        if create_folder(user_store, folder_name):
            bot.send_message(message.chat.id, folder_name + ' created!')
        else:
            bot.send_message(message.chat.id, 'Folder creation failed!')

    @bot.message_handler(commands=['folders'])
    def show_folders(message):
        user_store = get_user_store(store, message.chat.id)
        bot.send_message(message.chat.id, get_all_folders_names(user_store))

    @bot.message_handler(commands=['add'])
    def add(message):
        splited_message = message.text.split(' ')
        if 3 > len(splited_message):
            bot.send_message(message.chat.id, 'You need to use command with like:\n/add [folder_name] [contact_info]')
            return

        user_store = get_user_store(store, message.chat.id)
        folder_name = splited_message[1]
        contact_info = splited_message[2]
        if add_to_folder(user_store, folder_name, contact_info):
            bot.send_message(message.chat.id, contact_info + ' added to ' + folder_name)
        else:
            bot.send_message(message.chat.id, 'Can\'t add contact to folder! Does this folder exsists?')


    @bot.message_handler(commands=['remove'])
    def remove(message):
        bot.send_message(message.chat.id, 'Not supported yet')

    @bot.message_handler(commands=['delete'])
    def delete(message):
        bot.send_message(message.chat.id, 'Not supported yet')

    @bot.message_handler(commands=['show'])
    def show(message):
        splited_message = message.text.split(' ')
        if 2 > len(splited_message):
            bot.send_message(message.chat.id, 'You need to use command with like:\n/show [folder_name]')
            return

        user_store = get_user_store(store, message.chat.id)
        folder_name = splited_message[1]
        bot.send_message(message.chat.id, get_folder_content(user_store, folder_name))

    bot.polling(none_stop=False, interval=0, timeout=20)