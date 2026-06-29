
from telethon.tl.types import KeyboardButton, ReplyKeyboardMarkup, KeyboardButtonRow
from config import ADMIN_ID

def main_menu(uid):
    rows = [
        KeyboardButtonRow(buttons=[KeyboardButton('📞 Номер'), KeyboardButton('📧 Email')]),
        KeyboardButtonRow(buttons=[KeyboardButton('🌐 IP'), KeyboardButton('🔍 VK')]),
        KeyboardButtonRow(buttons=[KeyboardButton('💻 MAC'), KeyboardButton('🆔 По ID')]),
        KeyboardButtonRow(buttons=[KeyboardButton('🤖 Зеркало'), KeyboardButton('📊 Статистика')]),
        KeyboardButtonRow(buttons=[KeyboardButton('ℹ️ О боте')]),
    ]
    if uid == ADMIN_ID:
        rows.append(KeyboardButtonRow(buttons=[KeyboardButton('🛡 Админ панель')]))
    return ReplyKeyboardMarkup(rows=rows, resize=True, placeholder='Выберите действие...')

def cancel():
    return ReplyKeyboardMarkup(
        rows=[[KeyboardButtonRow(buttons=[KeyboardButton('🔙 Отмена')])]],
        resize=True
    )

def back_to_menu():
    return ReplyKeyboardMarkup(
        rows=[[KeyboardButtonRow(buttons=[KeyboardButton('🔙 В меню')])]],
        resize=True
    )

def admin_panel():
    return ReplyKeyboardMarkup(
        rows=[
            KeyboardButtonRow(buttons=[KeyboardButton('📊 Статистика бота'), KeyboardButton('📋 База данных')]),
            KeyboardButtonRow(buttons=[KeyboardButton('👥 Пользователи'), KeyboardButton('🪞 Зеркала')]),
            KeyboardButtonRow(buttons=[KeyboardButton('🔄 Перезапуск'), KeyboardButton('📢 Рассылка')]),
            KeyboardButtonRow(buttons=[KeyboardButton('🗑 Очистить базу'), KeyboardButton('⚡ Белый список')]),
            KeyboardButtonRow(buttons=[KeyboardButton('🔙 В меню')]),
        ],
        resize=True,
        placeholder='Админ-панель...'
    )
