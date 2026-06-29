# ═══════════════════════════════════════════════════════════════════════════════════════
# ║                                                                                     ║
# ║   ██████╗ ██╗██╗  ██╗     ██████╗ ██████╗  ██████╗ ██████╗ ██╗██╗   ██╗            ║
# ║   ██╔══██╗██║╚██╗██╔╝     ██╔══██╗██╔══██╗██╔═══██╗██╔══██╗██║██║   ██║            ║
# ║   ██║  ██║██║ ╚███╔╝      ██████╔╝██████╔╝██║   ██║██████╔╝██║██║   ██║            ║
# ║   ██║  ██║██║ ██╔██╗      ██╔═══╝ ██╔══██╗██║   ██║██╔══██╗██║╚██╗ ██╔╝            ║
# ║   ██████╔╝██║██╔╝ ██╗     ██║     ██║  ██║╚██████╔╝██████╔╝██║ ╚████╔╝             ║
# ║   ╚═════╝ ╚═╝╚═╝  ╚═╝     ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝              ║
# ║                                                                                     ║
# ║   DIX PROBIV BOT v4.0 — ПОЛНАЯ ВЕРСИЯ                                               ║
# ║   Проект #Амнезия                                                                   ║
# ║   Команда: Dixyi                                                                    ║
# ║   Дата: 13.10.2025                                                                  ║
# ║                                                                                     ║
# ═══════════════════════════════════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════════════════════════════════
# ИМПОРТЫ
# ═══════════════════════════════════════════════════════════════════════════════════════

import asyncio
import json
import re
import os
import sys
import time
import shutil
import sqlite3
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Set, Tuple
from collections import defaultdict

from telethon import TelegramClient, events, Button
from telethon.tl.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButtonRow,
    ChatBannedRights
)
from telethon.errors import (
    FloodWaitError,
    ChatAdminRequiredError,
    UserAdminInvalidError
)
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.functions.messages import DeleteChatRequest

import aiohttp
from aiohttp import ClientSession, ClientTimeout

# ═══════════════════════════════════════════════════════════════════════════════════════
# КОНФИГУРАЦИЯ
# ═══════════════════════════════════════════════════════════════════════════════════════

API_ID: int = 2040
API_HASH: str = 'b18441a1ff607e10a989891a5462e627'
BOT_TOKEN: str = '7968692327:AAHbj9lrD0BXgtls0vfbFHBQdQYiU2MqxSw'
ADMIN_ID: int = 1913718956
ADMIN_USERNAME: str = '@kapolam'

SESSION_PATH: str = '/storage/emulated/0/Download/DIX_SESSION_DATA/searchbot_session'
MIRRORS_FOLDER: str = '/storage/emulated/0/Download/DIX_MIRRORS'
MIRRORS_FILE: str = '/storage/emulated/0/Download/DIX_MIRRORS/mirrors.json'
DATABASE_FILE: str = '/storage/emulated/0/Download/DIX_TOTAL_BOT/dix_results.db'
WHITELIST_FILE: str = '/storage/emulated/0/Download/DIX_TOTAL_BOT/dix_whitelist.json'
CACHE_FOLDER: str = '/storage/emulated/0/Download/DIX_CACHE'
LOGS_FOLDER: str = '/storage/emulated/0/Download/DIX_LOGS'
BANS_FILE: str = '/storage/emulated/0/Download/DIX_TOTAL_BOT/bans.json'
MUTES_FILE: str = '/storage/emulated/0/Download/DIX_TOTAL_BOT/mutes.json'

SEARCH_BOT_USERNAME: str = '@sjgdfj0ghjdhjjegtjjebot'

# ═══════════════════════════════════════════════════════════════════════════════════════
# API КЛЮЧИ
# ═══════════════════════════════════════════════════════════════════════════════════════

VK_ACCESS_TOKEN: str = '0af157510af157510af15751aa0a89e69600af10af157516a0bc15996e74fe2b440998c'
LEAKCHECK_API_KEY: str = '49535f49545f5245414c4c595f4150495f4b4559'
LEAKOSINT_API_KEY: str = '7949201327:7z2O7xWq'
INTELX_API_KEY: str = 'e918253c-b46d-41c4-ba23-f1247eba5293'
IPINFO_API_KEY: str = '1d26e0613d1988'
SHODAN_API_KEY: str = 'DF7LYF16WVqSCW5C715egWBpnS03y6si'

# ═══════════════════════════════════════════════════════════════════════════════════════
# ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ
# ═══════════════════════════════════════════════════════════════════════════════════════

user_states: Dict[int, Optional[str]] = {}
user_last_request: Dict[int, float] = {}
user_request_count: Dict[int, List[float]] = defaultdict(list)
banned_users: Dict[int, Dict[str, Any]] = {}
muted_users: Dict[int, Dict[str, Any]] = {}
# registered_users отключены

FLOOD_LIMIT: int = 5  # Максимум запросов за период
FLOOD_PERIOD: int = 10  # Период в секундах
FLOOD_BAN_TIME: int = 3600  # Бан на час за флуд

bot_statistics: Dict[str, Any] = {
    'total_requests': 0,
    'phone_lookups': 0,
    'email_lookups': 0,
    'ip_lookups': 0,
    'vk_searches': 0,
    'mac_lookups': 0,
    'id_lookups': 0,
    'mirrors_created': 0,
    'start_count': 0,
    'bans_issued': 0,
    'mutes_issued': 0,
    'start_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'unique_users': set()
}

# ═══════════════════════════════════════════════════════════════════════════════════════
# ФУНКЦИИ БАЗЫ ДАННЫХ
# ═══════════════════════════════════════════════════════════════════════════════════════

def init_database() -> None:
    """Инициализация SQLite базы данных."""
    os.makedirs(os.path.dirname(DATABASE_FILE), exist_ok=True)
    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lookups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            query TEXT NOT NULL,
            result TEXT,
            date TEXT NOT NULL,
            user_id INTEGER NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            first_name TEXT,
            username TEXT,
            requests INTEGER DEFAULT 0,
            first_seen TEXT,
            last_seen TEXT,
            is_banned INTEGER DEFAULT 0,
            is_muted INTEGER DEFAULT 0,
            ban_reason TEXT,
            mute_until TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mirrors (
            token TEXT PRIMARY KEY,
            name TEXT,
            username TEXT,
            created_date TEXT
        )
    ''')
    
    connection.commit()
    connection.close()

def save_lookup_to_database(lookup_type: str, query: str, result: str, user_id: int) -> None:
    """Сохраняет результат поиска в базу данных."""
    try:
        connection = sqlite3.connect(DATABASE_FILE)
        cursor = connection.cursor()
        cursor.execute(
            'INSERT INTO lookups (type, query, result, date, user_id) VALUES (?, ?, ?, datetime("now","localtime"), ?)',
            (lookup_type, query, str(result)[:5000], user_id)
        )
        connection.commit()
        connection.close()
    except Exception as error:
        print(f"[DB ERROR] save_lookup: {error}")

def save_user_to_database(user_id: int, first_name: str, username: str) -> None:
    """Сохраняет или обновляет информацию о пользователе."""
    try:
        connection = sqlite3.connect(DATABASE_FILE)
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO users (user_id, first_name, username, requests, first_seen, last_seen)
            VALUES (?, ?, ?, 1, datetime("now","localtime"), datetime("now","localtime"))
            ON CONFLICT(user_id) DO UPDATE SET
                requests = requests + 1,
                last_seen = datetime("now","localtime"),
                first_name = excluded.first_name,
                username = excluded.username
        ''', (user_id, first_name, username))
        connection.commit()
        connection.close()
    except Exception as error:
        print(f"[DB ERROR] save_user: {error}")

def get_database_statistics() -> Dict[str, int]:
    """Возвращает статистику базы данных."""
    try:
        connection = sqlite3.connect(DATABASE_FILE)
        cursor = connection.cursor()
        cursor.execute('SELECT COUNT(*) FROM lookups')
        lookups_count = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM users')
        users_count = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM mirrors')
        mirrors_count = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM users WHERE is_banned = 1')
        banned_count = cursor.fetchone()[0]
        connection.close()
        return {
            'lookups': lookups_count,
            'users': users_count,
            'mirrors': mirrors_count,
            'banned': banned_count
        }
    except Exception as error:
        print(f"[DB ERROR] stats: {error}")
        return {'lookups': 0, 'users': 0, 'mirrors': 0, 'banned': 0}

# ═══════════════════════════════════════════════════════════════════════════════════════
# ФУНКЦИИ БЕЛОГО СПИСКА
# ═══════════════════════════════════════════════════════════════════════════════════════

def load_whitelist() -> Dict[str, Any]:
    """Загружает белый список."""
    if not os.path.exists(WHITELIST_FILE):
        return {}
    try:
        with open(WHITELIST_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception:
        return {}

def save_to_whitelist(phone: str, data: Dict[str, Any]) -> None:
    """Сохраняет номер в белый список."""
    whitelist = load_whitelist()
    whitelist[phone] = data
    os.makedirs(os.path.dirname(WHITELIST_FILE), exist_ok=True)
    with open(WHITELIST_FILE, 'w', encoding='utf-8') as file:
        json.dump(whitelist, file, ensure_ascii=False, indent=4)

def check_whitelist(phone: str) -> bool:
    """Проверяет номер в белом списке."""
    whitelist = load_whitelist()
    cleaned = re.sub(r'\D', '', phone)
    return cleaned in whitelist

# ═══════════════════════════════════════════════════════════════════════════════════════
# ФУНКЦИИ БАНОВ И МУТОВ
# ═══════════════════════════════════════════════════════════════════════════════════════

def load_bans() -> Dict[int, Dict[str, Any]]:
    """Загружает список забаненных пользователей."""
    if not os.path.exists(BANS_FILE):
        return {}
    try:
        with open(BANS_FILE, 'r', encoding='utf-8') as file:
            return {int(k): v for k, v in json.load(file).items()}
    except Exception:
        return {}

def save_bans(bans: Dict[int, Dict[str, Any]]) -> None:
    """Сохраняет список банов."""
    os.makedirs(os.path.dirname(BANS_FILE), exist_ok=True)
    with open(BANS_FILE, 'w', encoding='utf-8') as file:
        json.dump({str(k): v for k, v in bans.items()}, file, ensure_ascii=False, indent=4)

def load_mutes() -> Dict[int, Dict[str, Any]]:
    """Загружает список замьюченных пользователей."""
    if not os.path.exists(MUTES_FILE):
        return {}
    try:
        with open(MUTES_FILE, 'r', encoding='utf-8') as file:
            return {int(k): v for k, v in json.load(file).items()}
    except Exception:
        return {}

def save_mutes(mutes: Dict[int, Dict[str, Any]]) -> None:
    """Сохраняет список мьютов."""
    os.makedirs(os.path.dirname(MUTES_FILE), exist_ok=True)
    with open(MUTES_FILE, 'w', encoding='utf-8') as file:
        json.dump({str(k): v for k, v in mutes.items()}, file, ensure_ascii=False, indent=4)

def ban_user(user_id: int, reason: str = "Нарушение правил") -> None:
    """Банит пользователя."""
    banned_users[user_id] = {
        'user_id': user_id,
        'reason': reason,
        'banned_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'banned_by': ADMIN_ID
    }
    save_bans(banned_users)
    bot_statistics['bans_issued'] += 1

def unban_user(user_id: int) -> bool:
    """Разбанивает пользователя."""
    if user_id in banned_users:
        del banned_users[user_id]
        save_bans(banned_users)
        return True
    return False

def mute_user(user_id: int, minutes: int = 60, reason: str = "Нарушение правил") -> None:
    """Мьютит пользователя на указанное количество минут."""
    mute_until = datetime.now() + timedelta(minutes=minutes)
    muted_users[user_id] = {
        'user_id': user_id,
        'reason': reason,
        'muted_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'mute_until': mute_until.strftime('%Y-%m-%d %H:%M:%S'),
        'minutes': minutes
    }
    save_mutes(muted_users)
    bot_statistics['mutes_issued'] += 1

def unmute_user(user_id: int) -> bool:
    """Размьючивает пользователя."""
    if user_id in muted_users:
        del muted_users[user_id]
        save_mutes(muted_users)
        return True
    return False

def is_user_banned(user_id: int) -> bool:
    """Проверяет забанен ли пользователь."""
    return user_id in banned_users

def is_user_muted(user_id: int) -> bool:
    """Проверяет замьючен ли пользователь."""
    if user_id not in muted_users:
        return False
    mute_data = muted_users[user_id]
    mute_until = datetime.strptime(mute_data['mute_until'], '%Y-%m-%d %H:%M:%S')
    if datetime.now() > mute_until:
        del muted_users[user_id]
        save_mutes(muted_users)
        return False
    return True

# ═══════════════════════════════════════════════════════════════════════════════════════
# ФУНКЦИИ АНТИ-ФЛУДА
# ═══════════════════════════════════════════════════════════════════════════════════════

def check_flood(user_id: int) -> bool:
    """Проверяет пользователя на флуд. Возвращает True если флуд."""
    current_time = time.time()
    user_request_count[user_id].append(current_time)
    user_request_count[user_id] = [t for t in user_request_count[user_id] if current_time - t < FLOOD_PERIOD]
    if len(user_request_count[user_id]) > FLOOD_LIMIT:
        ban_user(user_id, f"Флуд: более {FLOOD_LIMIT} запросов за {FLOOD_PERIOD} секунд")
        return True
    return False

# ═══════════════════════════════════════════════════════════════════════════════════════
# ЛОГГИРОВАНИЕ
# ═══════════════════════════════════════════════════════════════════════════════════════

def log_message(level: str, message: str) -> None:
    """Записывает сообщение в лог."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    text = f"[{timestamp}] [{level}] {message}"
    print(text)
    try:
        os.makedirs(LOGS_FOLDER, exist_ok=True)
        log_file = os.path.join(LOGS_FOLDER, 'bot.log')
        with open(log_file, 'a', encoding='utf-8') as file:
            file.write(text + '\n')
    except Exception:
        pass

def log_info(message: str) -> None:
    log_message('INFO', message)

def log_warning(message: str) -> None:
    log_message('WARNING', message)

def log_error(message: str) -> None:
    log_message('ERROR', message)

# ═══════════════════════════════════════════════════════════════════════════════════════
# КЛАВИАТУРЫ
# ═══════════════════════════════════════════════════════════════════════════════════════

def create_main_menu_keyboard(user_id: int) -> ReplyKeyboardMarkup:
    """Создаёт главное меню."""
    row1 = KeyboardButtonRow(buttons=[KeyboardButton('📞 Номер'), KeyboardButton('📧 Email')])
    row2 = KeyboardButtonRow(buttons=[KeyboardButton('🌐 IP'), KeyboardButton('🔍 VK')])
    row3 = KeyboardButtonRow(buttons=[KeyboardButton('💻 MAC'), KeyboardButton('🆔 По ID')])
    row4 = KeyboardButtonRow(buttons=[KeyboardButton('🤖 Зеркало')])
    row5 = KeyboardButtonRow(buttons=[KeyboardButton('ℹ️ О боте')])
    buttons_rows = [row1, row2, row3, row4, row5]
    if user_id == ADMIN_ID:
        admin_row = KeyboardButtonRow(buttons=[KeyboardButton('🛡 Админ панель'), KeyboardButton('📊 Статистика')])
        buttons_rows.append(admin_row)
    return ReplyKeyboardMarkup(rows=buttons_rows, resize=True, placeholder='Выберите действие...')

def create_cancel_keyboard() -> ReplyKeyboardMarkup:
    """Создаёт клавиатуру с кнопкой отмены."""
    row = KeyboardButtonRow(buttons=[KeyboardButton('🔙 Отмена')])
    return ReplyKeyboardMarkup(rows=[row], resize=True)

def create_back_keyboard() -> ReplyKeyboardMarkup:
    """Создаёт клавиатуру с кнопкой возврата."""
    row = KeyboardButtonRow(buttons=[KeyboardButton('🔙 В меню')])
    return ReplyKeyboardMarkup(rows=[row], resize=True)

def create_admin_panel_keyboard() -> ReplyKeyboardMarkup:
    """Создаёт клавиатуру админ-панели."""
    row1 = KeyboardButtonRow(buttons=[KeyboardButton('📊 Статистика бота'), KeyboardButton('📋 База данных')])
    row2 = KeyboardButtonRow(buttons=[KeyboardButton('👥 Пользователи'), KeyboardButton('🪞 Зеркала')])
    row3 = KeyboardButtonRow(buttons=[KeyboardButton('🔨 Бан пользователя'), KeyboardButton('🔇 Мут пользователя')])
    row4 = KeyboardButtonRow(buttons=[KeyboardButton('✅ Разбан'), KeyboardButton('🔊 Размут')])
    row5 = KeyboardButtonRow(buttons=[KeyboardButton('🔄 Перезапуск'), KeyboardButton('📢 Рассылка')])
    row6 = KeyboardButtonRow(buttons=[KeyboardButton('🗑 Очистить базу'), KeyboardButton('⚡ Белый список')])
    row7 = KeyboardButtonRow(buttons=[KeyboardButton('📋 Список банов'), KeyboardButton('🔙 В меню')])
    return ReplyKeyboardMarkup(rows=[row1, row2, row3, row4, row5, row6, row7], resize=True, placeholder='Админ-панель...')

# ═══════════════════════════════════════════════════════════════════════════════════════
# ФОРМАТИРОВАНИЕ
# ═══════════════════════════════════════════════════════════════════════════════════════

def format_phone_number(phone: str) -> str:
    """Форматирует номер телефона."""
    cleaned = re.sub(r'\D', '', phone)
    if len(cleaned) == 11 and cleaned.startswith('7'):
        return f"+7 ({cleaned[1:4]}) {cleaned[4:7]}-{cleaned[7:9]}-{cleaned[9:11]}"
    return phone

def get_country_flag(country: str) -> str:
    """Возвращает флаг страны."""
    flags = {
        'Россия': '🇷🇺', 'Российская Федерация': '🇷🇺',
        'Украина': '🇺🇦', 'Беларусь': '🇧🇾', 'Казахстан': '🇰🇿',
        'США': '🇺🇸', 'Германия': '🇩🇪', 'Франция': '🇫🇷'
    }
    return flags.get(country, '🌍')

def format_phone_result(phone: str, htmlweb_data: Dict[str, Any], bot_data: Optional[str]) -> str:
    """Форматирует результат пробива номера."""
    current_date = datetime.now().strftime('%d.%m.%Y %H:%M')
    formatted_phone = format_phone_number(phone)
    country = htmlweb_data.get('country', 'Неизвестно')
    region = htmlweb_data.get('region', 'Неизвестно')
    city = htmlweb_data.get('city', 'Неизвестно')
    operator = htmlweb_data.get('operator', 'Неизвестно')
    brand = htmlweb_data.get('brand', 'Неизвестно')
    dial_range = htmlweb_data.get('range', htmlweb_data.get('diapazon', 'Неизвестно'))
    is_mobile = 'Да' if htmlweb_data.get('mobile') else 'Нет'
    timezone = htmlweb_data.get('timezone', 'Неизвестно')
    postal = htmlweb_data.get('postal', 'Неизвестно')
    flag = get_country_flag(country)
    
    result = f"""
<b>🕵️ DIX PROBIV — РЕЗУЛЬТАТ</b>
<b>📅 {current_date}</b>

<b>📱 ТЕЛЕФОН</b>
<b>▸ Телефон:</b> <code>{formatted_phone}</code>
<b>▸ Оператор:</b> {operator}
<b>▸ Регион:</b> {region}
<b>▸ Страна:</b> {flag} {country}
<b>▸ Город:</b> {city}
<b>▸ Бренд:</b> {brand}
<b>▸ Диапазон:</b> {dial_range}
<b>▸ Мобильный:</b> {is_mobile}
<b>▸ Часовой пояс:</b> {timezone}
<b>▸ Индекс:</b> {postal}
"""
    
    if bot_data:
        result += f"""
<b>━━━━━━━━━━━━━━━━━━━━━━━━━</b>
<b>🔎 ДАННЫЕ ПО НОМЕРУ:</b>

{bot_data}
"""
    
    result += """
<b>━━━━━━━━━━━━━━━━━━━━━━━━━</b>
"""
    return result

def format_id_result(user_id: str, user_data: Optional[Dict[str, Any]]) -> str:
    """Форматирует результат поиска по ID."""
    first_name = user_data.get('first_name', 'Не указано') if user_data else 'Не указано'
    last_name = user_data.get('last_name', 'Не указана') if user_data else 'Не указана'
    username = user_data.get('username', '') if user_data else ''
    
    return f"""
<b>🆔 РЕЗУЛЬТАТ ПОИСКА ПО ID</b>

<b>🆔 ID:</b> <code>{user_id}</code>
<b>👤 Имя:</b> {first_name}
<b>👤 Фамилия:</b> {last_name}
<b>📛 Username:</b> @{username if username else 'Не указан'}
<b>📱 Телефон:</b> {user_data.get('phone') if user_data and user_data.get('phone') else 'Скрыт'}

<b>━━━━━━━━━━━━━━━━━━━━━━━━━</b>
<b>🕵️ Поиск от @antiseach_bot | Dixyi © 2025</b>
"""

# ═══════════════════════════════════════════════════════════════════════════════════════
# API ЗАПРОСЫ
# ═══════════════════════════════════════════════════════════════════════════════════════

async def lookup_htmlweb(phone_number: str) -> Dict[str, Any]:
    """Запрос к htmlweb.ru."""
    cleaned = re.sub(r'\D', '', phone_number)
    url = f'https://htmlweb.ru/geo/api.php?json&telcod={cleaned}'
    try:
        async with ClientSession() as session:
            async with session.get(url, timeout=ClientTimeout(total=10)) as response:
                data = await response.json()
                return {
                    'country': data.get('fullname', 'Неизвестно'),
                    'region': data.get('region', {}).get('name', 'Неизвестно'),
                    'city': data.get('0', {}).get('name', 'Неизвестно'),
                    'operator': data.get('0', {}).get('oper', 'Неизвестно'),
                    'brand': data.get('0', {}).get('oper_brand', 'Неизвестно'),
                    'range': data.get('0', {}).get('def', 'Неизвестно'),
                    'mobile': data.get('0', {}).get('mobile', False),
                    'timezone': data.get('tz', 'Неизвестно'),
                    'postal': data.get('0', {}).get('post', 'Неизвестно'),
                }
    except Exception as error:
        log_error(f"HTMLWEB ошибка: {error}")
        return {'error': str(error)}

async def search_vk_profiles(query: str) -> List[Dict[str, Any]]:
    """Поиск профилей ВКонтакте."""
    url = f'https://api.vk.com/method/users.search?access_token={VK_ACCESS_TOKEN}&v=5.131&q={query}&fields=first_name,last_name,photo_max_orig'
    try:
        async with ClientSession() as session:
            async with session.get(url, timeout=ClientTimeout(total=10)) as response:
                data = await response.json()
                return data.get('response', [])
    except Exception as error:
        log_error(f"VK ошибка: {error}")
        return []

async def check_leaks_leakcheck(query: str) -> List[Dict[str, Any]]:
    """Проверка утечек через LeakCheck."""
    url = f'https://leakcheck.net/api/public?key={LEAKCHECK_API_KEY}&check={query}'
    try:
        async with ClientSession() as session:
            async with session.get(url, timeout=ClientTimeout(total=15)) as response:
                data = await response.json()
                if data.get('success') and data.get('result'):
                    return data['result']
                return []
    except Exception as error:
        log_error(f"LeakCheck ошибка: {error}")
        return []

async def lookup_ip_address(ip: str) -> Dict[str, Any]:
    """Запрос к IPInfo."""
    url = f'https://ipinfo.io/{ip}/json?token={IPINFO_API_KEY}'
    try:
        async with ClientSession() as session:
            async with session.get(url, timeout=ClientTimeout(total=10)) as response:
                return await response.json()
    except Exception as error:
        log_error(f"IPInfo ошибка: {error}")
        return {}

async def lookup_mac_address(mac: str) -> Optional[str]:
    """Определение производителя MAC."""
    url = f'https://api.macvendors.com/{mac}'
    try:
        async with ClientSession() as session:
            async with session.get(url, timeout=ClientTimeout(total=10)) as response:
                return await response.text()
    except Exception as error:
        log_error(f"MAC ошибка: {error}")
        return None

async def search_by_telegram_id(user_id: str) -> Optional[Dict[str, Any]]:
    """Поиск пользователя по Telegram ID."""
    client = TelegramClient(SESSION_PATH, API_ID, API_HASH)
    try:
        await client.start()
        entity = await client.get_entity(int(user_id))
        result = {
            'first_name': entity.first_name or '',
            'last_name': entity.last_name or '',
            'username': entity.username or '',
            'phone': getattr(entity, 'phone', None)
        }
        return result
    except Exception as error:
        log_error(f"Поиск по ID ошибка: {error}")
        return None
    finally:
        try:
            await client.disconnect()
        except Exception:
            pass

async def search_with_bot(phone_number: str) -> Optional[str]:
    """Поиск через поисковый бот."""
    log_info(f"Поисковый бот: {phone_number}")
    client = TelegramClient(SESSION_PATH, API_ID, API_HASH)
    result_text = None
    try:
        await client.start()
        await client.send_message(SEARCH_BOT_USERNAME, '/start')
        await asyncio.sleep(1.5)
        
        messages = await client.get_messages(SEARCH_BOT_USERNAME, limit=1)
        if messages and messages[0].buttons:
            await messages[0].click(0, 0)
            await asyncio.sleep(1)
            
            submenu = await client.get_messages(SEARCH_BOT_USERNAME, limit=1)
            if submenu and submenu[0].buttons:
                await submenu[0].click(0, 0)
                await asyncio.sleep(0.5)
                
                await client.send_message(SEARCH_BOT_USERNAME, phone_number)
                await asyncio.sleep(4)
                
                results = await client.get_messages(SEARCH_BOT_USERNAME, limit=5)
                for msg in results:
                    if msg.text and '📱' in msg.text:
                        result_text = msg.text
                        result_text = result_text.replace('by ****@sjgdfj0ghjdhjjegtjjebot', '')
                        result_text = result_text.replace('by @sjgdfj0ghjdhjjegtjjebot', '')
                        break
        
        return result_text
    except Exception as error:
        log_error(f"Поисковый бот ошибка: {error}")
        return None
    finally:
        try:
            await client.disconnect()
        except Exception:
            pass

# ═══════════════════════════════════════════════════════════════════════════════════════
# ЗЕРКАЛА
# ═══════════════════════════════════════════════════════════════════════════════════════

def get_mirrors_list() -> Dict[str, Dict[str, str]]:
    """Возвращает список зеркал."""
    if not os.path.exists(MIRRORS_FILE):
        return {}
    try:
        with open(MIRRORS_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception:
        return {}

def save_mirror_info(bot_token: str, bot_name: str, bot_username: str) -> None:
    """Сохраняет информацию о зеркале."""
    os.makedirs(MIRRORS_FOLDER, exist_ok=True)
    mirrors = get_mirrors_list()
    mirrors[bot_token] = {
        'name': bot_name,
        'username': bot_username,
        'created_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    with open(MIRRORS_FILE, 'w', encoding='utf-8') as file:
        json.dump(mirrors, file, ensure_ascii=False, indent=4)

# ═══════════════════════════════════════════════════════════════════════════════════════
# СПИСОК КНОПОК
# ═══════════════════════════════════════════════════════════════════════════════════════

KEYBOARD_BUTTONS: List[str] = [
    '📞 Номер', '📧 Email', '🌐 IP', '🔍 VK', '💻 MAC', '🆔 По ID',
    '🤖 Зеркало', '📊 Статистика', 'ℹ️ О боте', '🛡 Админ панель',
    '🔙 Отмена', '🔙 В меню',
    '📊 Статистика бота', '📋 База данных', '👥 Пользователи',
    '🪞 Зеркала', '🔄 Перезапуск', '📢 Рассылка', '🗑 Очистить базу', '⚡ Белый список',
    '🔨 Бан пользователя', '🔇 Мут пользователя', '✅ Разбан', '🔊 Размут', '📋 Список банов'
]

# ═══════════════════════════════════════════════════════════════════════════════════════
# СОЗДАНИЕ БОТА
# ═══════════════════════════════════════════════════════════════════════════════════════

log_info("Создаю клиент Telegram бота...")

# Настройка Tor прокси
PROXY_HOST = '127.0.0.1'
PROXY_PORT = 9050

bot = TelegramClient(
    'dix_telegram_bot',
    API_ID,
    API_HASH,
    
    device_model='Samsung Galaxy S24 Ultra',
    system_version='Android 14',
    app_version='11.5.3',
    lang_code='ru',
    system_lang_code='ru-RU'
)

try:
    bot.start(bot_token=BOT_TOKEN)
    log_info("Бот успешно запущен через Tor")
    log_info(f"Прокси: SOCKS5 {PROXY_HOST}:{PROXY_PORT}")
except FloodWaitError as error:
    log_warning(f"FloodWait {error.seconds} секунд. Ожидание...")
    time.sleep(error.seconds + 5)
    bot.start(bot_token=BOT_TOKEN)
except Exception as error:
    log_error(f"Ошибка Tor: {error}. Пробуем без прокси...")
    bot = TelegramClient(
        'dix_telegram_bot',
        API_ID,
        API_HASH,
        device_model='iPhone 15 Pro Max',
        system_version='iOS 18.0',
        app_version='11.5.3',
        lang_code='ru',
        system_lang_code='ru-RU'
    )
    bot.start(bot_token=BOT_TOKEN)

# ═══════════════════════════════════════════════════════════════════════════════════════
# ЗАГРУЗКА БАНОВ И МУТОВ
# ═══════════════════════════════════════════════════════════════════════════════════════

banned_users = load_bans()
muted_users = load_mutes()

# Разбаниваем админа на всякий случай
if ADMIN_ID in banned_users:
    del banned_users[ADMIN_ID]
    save_bans(banned_users)


# ═══════════════════════════════════════════════════════════════════════════════════════
# ОБРАБОТЧИК /start
# ═══════════════════════════════════════════════════════════════════════════════════════

@bot.on(events.NewMessage(pattern='/start'))
async def command_start(event):
    user_id = event.sender_id
    user_name = event.sender.first_name
    user_username = event.sender.username
    
    # Проверка бана
    
    
    user_states[user_id] = None
    bot_statistics['start_count'] += 1
    bot_statistics['unique_users'].add(user_id)
    
    save_user_to_database(user_id, user_name, user_username or '')
    
    # Уведомление админу о новом пользователе
    if user_id not in registered_users:
        registered_users[user_id] = {
            'first_name': user_name,
            'username': user_username or '',
            'first_seen': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        try:
            await bot.send_message(
                ADMIN_ID,
                f'<b>👤 НОВЫЙ ПОЛЬЗОВАТЕЛЬ</b>\n\n'
                f'<b>Имя:</b> {user_name}\n'
                f'<b>ID:</b> <code>{user_id}</code>\n'
                f'<b>Username:</b> @{user_username or "Нет"}',
                parse_mode='html'
            )
        except Exception:
            pass
    
    welcome_text = f"""
<b>🕵️ Прoект #Амнезия</b>

<b>Сервис прoверки публичнoй инфoрмации</b>
<b>и цифрoвых следoв пoльзoвателя</b>

<b>Сoздатель: @kapolam</b>
<b>Владелец: @kepber</b>

<b>👇 Выберите действие:</b>
"""
    
    keyboard = create_main_menu_keyboard(user_id)
    await event.respond(welcome_text, buttons=keyboard, parse_mode='html')

# ═══════════════════════════════════════════════════════════════════════════════════════
# ОБРАБОТЧИК КНОПОК
# ═══════════════════════════════════════════════════════════════════════════════════════

@bot.on(events.NewMessage(func=lambda e: e.is_private and e.text in KEYBOARD_BUTTONS))
async def keyboard_handler(event):
    user_id = event.sender_id
    text = event.text.strip()
    
    # Проверка бана
    if is_user_banned(user_id) and user_id != ADMIN_ID:
        await event.respond('<b>⛔ Вы заблокированы.</b>', parse_mode='html')
        return
    
    # Проверка мута
    if is_user_muted(user_id):
        await event.respond('<b>🔇 Вы замьючены. Ожидайте.</b>', parse_mode='html')
        return
    
    # Проверка флуда
    
    if text == '📞 Номер':
        user_states[user_id] = 'waiting_phone'
        cancel_kb = create_cancel_keyboard()
        message_text = '<b>📞 Введите номер телефона:</b>' + chr(10) + chr(10) + '<i>Пример: +79999999999</i>'
        await event.respond(message_text, buttons=cancel_kb, parse_mode='html')
    
    elif text == '📧 Email':
        user_states[user_id] = 'waiting_email'
        cancel_kb = create_cancel_keyboard()
        message_text = '<b>📧 Введите email адрес:</b>' + chr(10) + chr(10) + '<i>Пример: example@gmail.com</i>'
        await event.respond(message_text, buttons=cancel_kb, parse_mode='html')
    
    elif text == '🌐 IP':
        user_states[user_id] = 'waiting_ip'
        cancel_kb = create_cancel_keyboard()
        message_text = '<b>🌐 Введите IP адрес:</b>' + chr(10) + chr(10) + '<i>Пример: 8.8.8.8</i>'
        await event.respond(message_text, buttons=cancel_kb, parse_mode='html')
    
    elif text == '🔍 VK':
        user_states[user_id] = 'waiting_vk'
        cancel_kb = create_cancel_keyboard()
        message_text = '<b>🔍 Введите ID или имя для поиска VK:</b>' + chr(10) + chr(10) + '<i>Пример: 1 или Иван Иванов</i>'
        await event.respond(message_text, buttons=cancel_kb, parse_mode='html')
    
    elif text == '💻 MAC':
        user_states[user_id] = 'waiting_mac'
        cancel_kb = create_cancel_keyboard()
        message_text = '<b>💻 Введите MAC адрес:</b>' + chr(10) + chr(10) + '<i>Пример: 00:1A:2B:3C:4D:5E</i>'
        await event.respond(message_text, buttons=cancel_kb, parse_mode='html')
    
    elif text == '🆔 По ID':
        user_states[user_id] = 'waiting_tg_id'
        cancel_kb = create_cancel_keyboard()
        message_text = '<b>🆔 Введите Telegram ID:</b>' + chr(10) + chr(10) + '<i>Пример: 5817293461</i>'
        await event.respond(message_text, buttons=cancel_kb, parse_mode='html')
    
    elif text == '🤖 Зеркало':
        user_states[user_id] = 'waiting_mirror_token'
        cancel_kb = create_cancel_keyboard()
        message_text = '<b>🤖 СОЗДАНИЕ ЗЕРКАЛА</b>' + chr(10) + chr(10)
        message_text += '<b>Инструкция:</b>' + chr(10)
        message_text += '1. Зайдите в @BotFather' + chr(10)
        message_text += '2. Отправьте /newbot' + chr(10)
        message_text += '3. Придумайте имя и username' + chr(10)
        message_text += '4. Скопируйте токен' + chr(10) + chr(10)
        message_text += '<b>⬇️ Отправьте токен:</b>'
        await event.respond(message_text, buttons=cancel_kb, parse_mode='html')
    
    elif text == '📊 Статистика':
        stats = get_database_statistics()
        stats_text = '<b>📊 СТАТИСТИКА</b>' + chr(10) + chr(10)
        stats_text += f'<b>🔍 Запросов:</b> {bot_statistics["total_requests"]}' + chr(10)
        stats_text += f'<b>👤 Пользователей:</b> {len(bot_statistics["unique_users"])}' + chr(10)
        stats_text += f'<b>💾 В базе:</b> {stats["lookups"]} записей' + chr(10)
        stats_text += f'<b>🪞 Зеркал:</b> {stats["mirrors"]}' + chr(10)
        stats_text += f'<b>🚫 Забанено:</b> {stats["banned"]}'
        await event.respond(stats_text, parse_mode='html')
    
    elif text == 'ℹ️ О боте':
        about_text = '<b>🕵️ DIX OSINT</b>' + chr(10) + chr(10)
        about_text += '📞 Номер' + chr(10)
        about_text += '📧 Email' + chr(10)
        about_text += '🌐 IP' + chr(10)
        about_text += '🔍 VK' + chr(10)
        about_text += '💻 MAC' + chr(10)
        about_text += '🆔 По ID' + chr(10)
        about_text += '🤖 Зеркала'
        await event.respond(about_text, parse_mode='html')
    
    elif text == '🔙 Отмена':
        user_states[user_id] = None
        await event.respond('<b>❌ Действие отменено.</b>', buttons=create_main_menu_keyboard(user_id), parse_mode='html')
    
    elif text == '🔙 В меню':
        user_states[user_id] = None
        await event.respond('<b>🕵️ Прoект #Амнезия</b>' + chr(10) + chr(10) + '<b>👇 Выберите действие:</b>', buttons=create_main_menu_keyboard(user_id), parse_mode='html')
    
    # Админ-панель
    elif text == '🛡 Админ панель':
        if user_id != ADMIN_ID:
            await event.respond('<b>⛔ Доступ запрещён.</b>', parse_mode='html')
            return
        user_states[user_id] = None
        stats = get_database_statistics()
        admin_text = '<b>🛡 АДМИН ПАНЕЛЬ</b>' + chr(10) + chr(10)
        admin_text += '<b>👑 Админ:</b> #Амнезия' + chr(10)
        admin_text += '<b>🤖 Бот:</b> @antiseach_bot' + chr(10)
        admin_text += f'<b>📅 Аптайм:</b> {bot_statistics["start_date"]}' + chr(10) + chr(10)
        admin_text += f'<b>Пользователей:</b> {len(bot_statistics["unique_users"])}' + chr(10)
        admin_text += f'<b>Забанено:</b> {stats["banned"]}' + chr(10)
        admin_text += f'<b>Замьючено:</b> {len(muted_users)}' + chr(10) + chr(10)
        admin_text += '<b>👇 Выберите действие:</b>'
        await event.respond(admin_text, buttons=create_admin_panel_keyboard(), parse_mode='html')
    
    # Админские кнопки
    elif text == '📊 Статистика бота' and user_id == ADMIN_ID:
        stats = get_database_statistics()
        stats_text = '<b>📊 ПОЛНАЯ СТАТИСТИКА</b>' + chr(10) + chr(10)
        stats_text += f'<b>🔍 Всего запросов:</b> {bot_statistics["total_requests"]}' + chr(10)
        stats_text += f'<b>📞 Номеров:</b> {bot_statistics["phone_lookups"]}' + chr(10)
        stats_text += f'<b>📧 Email:</b> {bot_statistics["email_lookups"]}' + chr(10)
        stats_text += f'<b>🌐 IP:</b> {bot_statistics["ip_lookups"]}' + chr(10)
        stats_text += f'<b>🔍 VK:</b> {bot_statistics["vk_searches"]}' + chr(10)
        stats_text += f'<b>💻 MAC:</b> {bot_statistics["mac_lookups"]}' + chr(10)
        stats_text += f'<b>🆔 ID:</b> {bot_statistics["id_lookups"]}' + chr(10)
        stats_text += f'<b>👤 Пользователей:</b> {len(bot_statistics["unique_users"])}' + chr(10)
        stats_text += f'<b>💾 В базе:</b> {stats["lookups"]} записей' + chr(10)
        stats_text += f'<b>🚫 Забанено:</b> {stats["banned"]}' + chr(10)
        stats_text += f'<b>🔇 Замьючено:</b> {len(muted_users)}' + chr(10)
        stats_text += f'<b>🪞 Зеркал:</b> {stats["mirrors"]}' + chr(10)
        stats_text += f'<b>🚀 Запусков:</b> {bot_statistics["start_count"]}'
        await event.respond(stats_text, parse_mode='html')
    
    elif text == '📋 База данных' and user_id == ADMIN_ID:
        stats = get_database_statistics()
        db_text = '<b>📋 БАЗА ДАННЫХ</b>' + chr(10) + chr(10)
        db_text += f'<b>📁 Файл:</b> dix_results.db' + chr(10)
        db_text += f'<b>📝 Записей:</b> {stats["lookups"]}' + chr(10)
        db_text += f'<b>👤 Пользователей:</b> {stats["users"]}' + chr(10)
        db_text += f'<b>🚫 Забанено:</b> {stats["banned"]}'
        await event.respond(db_text, parse_mode='html')
    
    elif text == '👥 Пользователи' and user_id == ADMIN_ID:
        users_list = list(bot_statistics['unique_users'])
        users_text = '<b>👥 ПОЛЬЗОВАТЕЛИ</b>' + chr(10) + chr(10)
        users_text += f'<b>Всего:</b> {len(users_list)}' + chr(10) + chr(10)
        for uid in users_list[:30]:
            banned_mark = ' 🚫' if is_user_banned(uid) else ''
            muted_mark = ' 🔇' if is_user_muted(uid) else ''
            users_text += f'• <code>{uid}</code>{banned_mark}{muted_mark}' + chr(10)
        if len(users_list) > 30:
            users_text += chr(10) + f'<i>... и ещё {len(users_list) - 30}</i>'
        await event.respond(users_text, parse_mode='html')
    
    elif text == '🪞 Зеркала' and user_id == ADMIN_ID:
        mirrors = get_mirrors_list()
        if not mirrors:
            await event.respond('<b>🪞 Зеркал пока нет</b>', parse_mode='html')
        else:
            mirrors_text = f'<b>🪞 ЗЕРКАЛА ({len(mirrors)})</b>' + chr(10) + chr(10)
            for token, info in list(mirrors.items())[:10]:
                mirrors_text += f'• @{info.get("username", "?")} — {info.get("created_date", "?")}' + chr(10)
            await event.respond(mirrors_text, parse_mode='html')
    
    elif text == '🔨 Бан пользователя' and user_id == ADMIN_ID:
        user_states[user_id] = 'waiting_ban_user'
        cancel_kb = create_cancel_keyboard()
        ban_text = '<b>🔨 БАН ПОЛЬЗОВАТЕЛЯ</b>' + chr(10) + chr(10)
        ban_text += '<b>Отправьте ID пользователя и причину:</b>' + chr(10)
        ban_text += '<i>Формат:</i>' + chr(10)
        ban_text += '<code>123456789 причина бана</code>'
        await event.respond(ban_text, buttons=cancel_kb, parse_mode='html')
    
    elif text == '🔇 Мут пользователя' and user_id == ADMIN_ID:
        user_states[user_id] = 'waiting_mute_user'
        cancel_kb = create_cancel_keyboard()
        mute_text = '<b>🔇 МУТ ПОЛЬЗОВАТЕЛЯ</b>' + chr(10) + chr(10)
        mute_text += '<b>Отправьте ID пользователя, минуты и причину:</b>' + chr(10)
        mute_text += '<i>Формат:</i>' + chr(10)
        mute_text += '<code>123456789 60 причина мута</code>'
        await event.respond(mute_text, buttons=cancel_kb, parse_mode='html')
    
    elif text == '✅ Разбан' and user_id == ADMIN_ID:
        user_states[user_id] = 'waiting_unban_user'
        cancel_kb = create_cancel_keyboard()
        await event.respond('<b>✅ РАЗБАН</b>' + chr(10) + chr(10) + '<b>Отправьте ID пользователя:</b>', buttons=cancel_kb, parse_mode='html')
    
    elif text == '🔊 Размут' and user_id == ADMIN_ID:
        user_states[user_id] = 'waiting_unmute_user'
        cancel_kb = create_cancel_keyboard()
        await event.respond('<b>🔊 РАЗМУТ</b>' + chr(10) + chr(10) + '<b>Отправьте ID пользователя:</b>', buttons=cancel_kb, parse_mode='html')
    
    elif text == '📋 Список банов' and user_id == ADMIN_ID:
        if not banned_users:
            await event.respond('<b>📋 Список банов пуст</b>', parse_mode='html')
        else:
            bans_text = f'<b>📋 ЗАБАНЕННЫЕ ({len(banned_users)})</b>' + chr(10) + chr(10)
            for uid, info in list(banned_users.items())[:20]:
                bans_text += f'• <code>{uid}</code> — {info["reason"]} ({info["banned_at"]})' + chr(10)
            await event.respond(bans_text, parse_mode='html')
    
    elif text == '🔄 Перезапуск' and user_id == ADMIN_ID:
        await event.respond('<b>🔄 Перезапускаю бота...</b>', parse_mode='html')
        os.execl(sys.executable, sys.executable, *sys.argv)
    
    elif text == '📢 Рассылка' and user_id == ADMIN_ID:
        user_states[user_id] = 'waiting_broadcast'
        cancel_kb = create_cancel_keyboard()
        await event.respond('<b>📢 РАССЫЛКА</b>' + chr(10) + chr(10) + '<b>Отправьте сообщение для всех пользователей:</b>', buttons=cancel_kb, parse_mode='html')
    
    elif text == '🗑 Очистить базу' and user_id == ADMIN_ID:
        try:
            connection = sqlite3.connect(DATABASE_FILE)
            connection.execute('DELETE FROM lookups')
            connection.commit()
            connection.close()
            await event.respond('<b>🗑 База данных очищена!</b>', parse_mode='html')
        except Exception as error:
            await event.respond(f'<b>❌ Ошибка:</b> {error}', parse_mode='html')
    
    elif text == '⚡ Белый список' and user_id == ADMIN_ID:
        user_states[user_id] = 'waiting_whitelist'
        cancel_kb = create_cancel_keyboard()
        whitelist_text = '<b>⚡ ДОБАВЛЕНИЕ В БЕЛЫЙ СПИСОК</b>' + chr(10) + chr(10)
        whitelist_text += '<b>Формат:</b>' + chr(10)
        whitelist_text += 'Номер: +79999999999' + chr(10)
        whitelist_text += 'ФИО: Иванов Иван Иванович' + chr(10)
        whitelist_text += 'Адрес: г. Москва' + chr(10) + chr(10)
        whitelist_text += '<b>⬇️ Отправьте данные:</b>'
        await event.respond(whitelist_text, buttons=cancel_kb, parse_mode='html')

# ═══════════════════════════════════════════════════════════════════════════════════════
# ОБРАБОТЧИК ВХОДЯЩИХ СООБЩЕНИЙ
# ═══════════════════════════════════════════════════════════════════════════════════════

@bot.on(events.NewMessage(func=lambda e: not e.text.startswith('/') and e.is_private and e.text not in KEYBOARD_BUTTONS))
async def incoming_handler(event):
    user_id = event.sender_id
    state = user_states.get(user_id)
    text = event.text.strip()
    
    # Проверка бана
    if is_user_banned(user_id) and user_id != ADMIN_ID:
        await event.respond('<b>⛔ Вы заблокированы.</b>', parse_mode='html')
        return
    
    # Проверка мута
    if is_user_muted(user_id):
        await event.respond('<b>🔇 Вы замьючены.</b>', parse_mode='html')
        return
    
    if not state:
        await event.respond('<b>⚠️ Используйте кнопки меню. Отправьте /start</b>', parse_mode='html')
        return
    
    # Обработка пробива номера
    if state == 'waiting_phone':
        cleaned = re.sub(r'\D', '', text)
        if len(cleaned) < 10:
            await event.respond('<b>❌ Неверный формат номера.</b>', buttons=create_cancel_keyboard(), parse_mode='html')
            return
        if check_whitelist(cleaned):
            await event.respond('<b>⚡ ДАННЫЕ НАХОДЯТСЯ В БЕЛОМ СПИСКЕ</b>' + chr(10) + chr(10) + '<i>Подробнее у тех.поддержки.</i>', buttons=create_back_keyboard(), parse_mode='html')
            return
        
        bot_statistics['total_requests'] += 1
        bot_statistics['phone_lookups'] += 1
        save_user_to_database(user_id, event.sender.first_name, event.sender.username or '')
        status = await event.respond('<b>🔍 ЗАПУСК ПОИСКА...</b>' + chr(10) + '<i>Ожидайте...</i>', parse_mode='html')
        await status.edit('<b>⏳ [1/3] Город и оператор...</b>', parse_mode='html')
        htmlweb_data = await lookup_htmlweb(cleaned)
        await status.edit('<b>⏳ [2/3] Проверка утечек...</b>', parse_mode='html')
        leaks_data = await check_leaks_leakcheck(cleaned)
        await status.edit('<b>⏳ [3/3] Телефонные книги...</b>', parse_mode='html')
        bot_data = await search_with_bot(cleaned)
        result = format_phone_result(text, htmlweb_data, bot_data)
        user_states[user_id] = None
        
        # Очищаем все переменные сразу
        htmlweb_data = {}
        bot_data = None
        leaks_data = []
        cleaned = ''
        
        try:
            await status.edit(result, buttons=create_back_keyboard(), parse_mode='html')
        except Exception:
            await status.edit('<b>✅ Готово!</b>', buttons=create_back_keyboard(), parse_mode='html')
    
    # Обработка email
    elif state == 'waiting_email':
        if '@' not in text:
            await event.respond('<b>❌ Неверный email.</b>', buttons=create_cancel_keyboard(), parse_mode='html')
            return
        bot_statistics['total_requests'] += 1
        bot_statistics['email_lookups'] += 1
        status = await event.respond('<b>⏳ Проверка утечек...</b>', parse_mode='html')
        leaks = await check_leaks_leakcheck(text)
        user_states[user_id] = None
        if leaks:
            result = f'<b>📧 РЕЗУЛЬТАТ</b>' + chr(10) + chr(10) + f'<b>Email:</b> <code>{text}</code>' + chr(10) + f'<b>⚠️ Найдено утечек:</b> {len(leaks)}'
        else:
            result = f'<b>📧 РЕЗУЛЬТАТ</b>' + chr(10) + chr(10) + f'<b>Email:</b> <code>{text}</code>' + chr(10) + '<b>✅ Утечек не найдено</b>'
        await status.edit(result, buttons=create_back_keyboard(), parse_mode='html')
    
    # Обработка IP
    elif state == 'waiting_ip':
        if not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', text):
            await event.respond('<b>❌ Неверный IP.</b>', buttons=create_cancel_keyboard(), parse_mode='html')
            return
        bot_statistics['total_requests'] += 1
        bot_statistics['ip_lookups'] += 1
        status = await event.respond('<b>⏳ Поиск IP...</b>', parse_mode='html')
        ip_data = await lookup_ip_address(text)
        user_states[user_id] = None
        result = '<b>🌐 РЕЗУЛЬТАТ</b>' + chr(10) + chr(10)
        result += f'<b>IP:</b> <code>{text}</code>' + chr(10)
        result += f'<b>Город:</b> {ip_data.get("city", "?")}' + chr(10)
        result += f'<b>Регион:</b> {ip_data.get("region", "?")}' + chr(10)
        result += f'<b>Страна:</b> {ip_data.get("country", "?")}' + chr(10)
        result += f'<b>Провайдер:</b> {ip_data.get("org", "?")}'
        await status.edit(result, buttons=create_back_keyboard(), parse_mode='html')
    
    # Обработка VK
    elif state == 'waiting_vk':
        bot_statistics['total_requests'] += 1
        bot_statistics['vk_searches'] += 1
        status = await event.respond('<b>⏳ Поиск VK...</b>', parse_mode='html')
        profiles = await search_vk_profiles(text)
        user_states[user_id] = None
        if profiles:
            result = f'<b>🔍 НАЙДЕНО VK:</b> {len(profiles)}' + chr(10) + chr(10)
            for p in profiles[:5]:
                result += f'• <a href="https://vk.com/id{p["id"]}">{p.get("first_name","")} {p.get("last_name","")}</a>' + chr(10)
        else:
            result = '<b>❌ VK профили не найдены</b>'
        await status.edit(result, buttons=create_back_keyboard(), parse_mode='html')
    
    # Обработка MAC
    elif state == 'waiting_mac':
        bot_statistics['total_requests'] += 1
        bot_statistics['mac_lookups'] += 1
        status = await event.respond('<b>⏳ Определение MAC...</b>', parse_mode='html')
        vendor = await lookup_mac_address(text)
        user_states[user_id] = None
        result = f'<b>💻 MAC:</b> <code>{text}</code>' + chr(10) + f'<b>Производитель:</b> {vendor if vendor else "Не найден"}'
        await status.edit(result, buttons=create_back_keyboard(), parse_mode='html')
    
    # Обработка поиска по ID
    elif state == 'waiting_tg_id':
        bot_statistics['total_requests'] += 1
        bot_statistics['id_lookups'] += 1
        status = await event.respond('<b>⏳ Поиск по ID...</b>', parse_mode='html')
        user_data = await search_by_telegram_id(text)
        user_states[user_id] = None
        result = format_id_result(text, user_data)
        save_lookup_to_database('id', text, result, user_id)
        await status.edit(result, buttons=create_back_keyboard(), parse_mode='html')
    
    # Обработка токена зеркала
    elif state == 'waiting_mirror_token':
        token = text.strip()
        if ':' not in token:
            await event.respond('<b>❌ Неверный токен.</b>', buttons=create_cancel_keyboard(), parse_mode='html')
            return
        status = await event.respond('<b>⏳ Проверяю токен...</b>', parse_mode='html')
        try:
            test_client = TelegramClient('mirror_test', API_ID, API_HASH)
            await test_client.start(bot_token=token)
            bot_info = await test_client.get_me()
            bot_name = bot_info.first_name
            bot_username = bot_info.username
            save_mirror_info(token, bot_name, bot_username)
            await test_client.disconnect()
            bot_statistics['mirrors_created'] += 1
            user_states[user_id] = None
            await status.edit(f'<b>✅ Успешно</b>' + chr(10) + chr(10) + f'<b>🤖</b> @{bot_username}' + chr(10) + '<b>📋 Статус:</b> Работает', buttons=create_back_keyboard(), parse_mode='html')
        except Exception as error:
            await status.edit(f'<b>❌ Ошибка:</b> {error}', parse_mode='html')
    
    # Обработка бана
    elif state == 'waiting_ban_user' and user_id == ADMIN_ID:
        parts = text.split(' ', 1)
        if len(parts) >= 1 and parts[0].isdigit():
            target_id = int(parts[0])
            reason = parts[1] if len(parts) > 1 else 'Нарушение правил'
            ban_user(target_id, reason)
            user_states[user_id] = None
            await event.respond(f'<b>✅ Пользователь <code>{target_id}</code> забанен!</b>' + chr(10) + f'<b>Причина:</b> {reason}', buttons=create_admin_panel_keyboard(), parse_mode='html')
            try:
                await bot.send_message(target_id, f'<b>⛔ ВЫ ЗАБЛОКИРОВАНЫ</b>' + chr(10) + chr(10) + f'<b>Причина:</b> {reason}' + chr(10) + chr(10) + f'<i>Обратитесь к {ADMIN_USERNAME}</i>', parse_mode='html')
            except Exception:
                pass
        else:
            await event.respond('<b>❌ Неверный формат.</b>' + chr(10) + '<i>Пример: 123456789 спам</i>', buttons=create_cancel_keyboard(), parse_mode='html')
    
    # Обработка мута
    elif state == 'waiting_mute_user' and user_id == ADMIN_ID:
        parts = text.split(' ', 2)
        if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
            target_id = int(parts[0])
            minutes = int(parts[1])
            reason = parts[2] if len(parts) > 2 else 'Нарушение правил'
            mute_user(target_id, minutes, reason)
            user_states[user_id] = None
            await event.respond(f'<b>✅ Пользователь <code>{target_id}</code> замьючен на {minutes} мин!</b>' + chr(10) + f'<b>Причина:</b> {reason}', buttons=create_admin_panel_keyboard(), parse_mode='html')
            try:
                await bot.send_message(target_id, f'<b>🔇 ВЫ ЗАМЬЮЧЕНЫ</b>' + chr(10) + chr(10) + f'<b>Причина:</b> {reason}' + chr(10) + f'<b>Срок:</b> {minutes} минут' + chr(10) + chr(10) + '<i>Ожидайте окончания мута</i>', parse_mode='html')
            except Exception:
                pass
        else:
            await event.respond('<b>❌ Неверный формат.</b>' + chr(10) + '<i>Пример: 123456789 60 спам</i>', buttons=create_cancel_keyboard(), parse_mode='html')
    
    # Обработка разбана
    elif state == 'waiting_unban_user' and user_id == ADMIN_ID:
        if text.isdigit():
            target_id = int(text)
            if unban_user(target_id):
                await event.respond(f'<b>✅ Пользователь <code>{target_id}</code> разбанен!</b>', buttons=create_admin_panel_keyboard(), parse_mode='html')
            else:
                await event.respond(f'<b>❌ Пользователь <code>{target_id}</code> не в бане.</b>', buttons=create_admin_panel_keyboard(), parse_mode='html')
            user_states[user_id] = None
        else:
            await event.respond('<b>❌ Неверный ID.</b>', buttons=create_cancel_keyboard(), parse_mode='html')
    
    # Обработка размута
    elif state == 'waiting_unmute_user' and user_id == ADMIN_ID:
        if text.isdigit():
            target_id = int(text)
            if unmute_user(target_id):
                await event.respond(f'<b>✅ Пользователь <code>{target_id}</code> размьючен!</b>', buttons=create_admin_panel_keyboard(), parse_mode='html')
            else:
                await event.respond(f'<b>❌ Пользователь <code>{target_id}</code> не в муте.</b>', buttons=create_admin_panel_keyboard(), parse_mode='html')
            user_states[user_id] = None
        else:
            await event.respond('<b>❌ Неверный ID.</b>', buttons=create_cancel_keyboard(), parse_mode='html')
    
    # Обработка рассылки
    elif state == 'waiting_broadcast' and user_id == ADMIN_ID:
        user_states[user_id] = None
        users_list = list(bot_statistics['unique_users'])
        await event.respond(f'<b>📢 РАССЫЛКА</b>' + chr(10) + chr(10) + f'<b>Получателей:</b> {len(users_list)}' + chr(10) + f'<b>Сообщение:</b>' + chr(10) + f'{text[:500]}', buttons=create_back_keyboard(), parse_mode='html')
    
    # Обработка белого списка
    elif state == 'waiting_whitelist' and user_id == ADMIN_ID:
        user_states[user_id] = None
        data = {}
        for line in text.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                data[key.strip()] = value.strip()
        phone = data.get('Номер', '')
        if not phone:
            found = re.findall(r'\+?\d{10,12}', text)
            if found:
                phone = found[0]
        if phone:
            save_to_whitelist(phone, {'data': data, 'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
            await event.respond(f'<b>✅ Добавлено в белый список!</b>' + chr(10) + chr(10) + f'<b>Номер:</b> {phone}', buttons=create_back_keyboard(), parse_mode='html')
        else:
            await event.respond('<b>❌ Номер не найден.</b>', buttons=create_back_keyboard(), parse_mode='html')

# ═══════════════════════════════════════════════════════════════════════════════════════
# ЗАПУСК БОТА
# ═══════════════════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    print("""
╔══════════════════════════════════════╗
║   🕵️ DIX PROBIV BOT v4.0           ║
║   Прoект #Амнезия                  ║
║   Dixyi © 2025                      ║
║   Анти-флуд: ✅                     ║
║   Баны/Муты: ✅                     ║
╚══════════════════════════════════════╝
    """)
    
    init_database()
    os.makedirs(CACHE_FOLDER, exist_ok=True)
    os.makedirs(LOGS_FOLDER, exist_ok=True)
    
    # Автозапуск зеркал
    mirrors = get_mirrors_list()
    if mirrors:
        for token, info in mirrors.items():
            username = info.get('username', 'unknown')
            mirror_script = os.path.join(MIRRORS_FOLDER, f'mirror_{username}.py')
            if os.path.exists(mirror_script):
                try:
                    import subprocess
                    subprocess.Popen(
                        [sys.executable, mirror_script],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        start_new_session=True
                    )
                    log_info(f"Зеркало @{username} запущено")
                except Exception as error:
                    log_error(f"Ошибка запуска зеркала @{username}: {error}")
    
    log_info("Бот запущен")
    log_info(f"Забанено: {len(banned_users)}, Замьючено: {len(muted_users)}")
    
    while True:
        try:
            bot.run_until_disconnected()
        except FloodWaitError as error:
            log_warning(f"FloodWait {error.seconds} сек")
            time.sleep(error.seconds + 5)
        except Exception as error:
            log_error(f"Ошибка: {error}")
            time.sleep(30)
