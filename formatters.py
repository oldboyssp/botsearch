
from datetime import datetime
import re

def format_phone(phone):
    cleaned = re.sub(r'\D', '', phone)
    if len(cleaned) == 11 and cleaned.startswith('7'):
        return f"+7 ({cleaned[1:4]}) {cleaned[4:7]}-{cleaned[7:9]}-{cleaned[9:11]}"
    return phone

def flag(country):
    flags = {'Россия':'🇷🇺','Российская Федерация':'🇷🇺','Украина':'🇺🇦','Беларусь':'🇧🇾','Казахстан':'🇰🇿'}
    return flags.get(country, '🌍')

def format_phone_result(phone, htmlweb, bot_data):
    date = datetime.now().strftime('%d.%m.%Y %H:%M')
    fphone = format_phone(phone)
    
    result = f"""
<b>🕵️ DIX PROBIV — РЕЗУЛЬТАТ</b>
<b>📅 {date}</b>

<b>📱 ТЕЛЕФОН</b>
<b>▸ Телефон:</b> <code>{fphone}</code>
<b>▸ Оператор:</b> {htmlweb.get('operator','?')}
<b>▸ Регион:</b> {htmlweb.get('region','?')}
<b>▸ Страна:</b> {flag(htmlweb.get('country','?'))} {htmlweb.get('country','?')}
<b>▸ Город:</b> {htmlweb.get('city','?')}
<b>▸ Бренд:</b> {htmlweb.get('brand','?')}
<b>▸ Диапазон:</b> {htmlweb.get('range','?')}
<b>▸ Мобильный:</b> {'Да' if htmlweb.get('mobile') else 'Нет'}
<b>▸ Часовой пояс:</b> {htmlweb.get('timezone','?')}
<b>▸ Индекс:</b> {htmlweb.get('postal','?')}
"""
    
    if bot_data:
        result += f"""

<b>━━━━━━━━━━━━━━━━━━━━━━━━━</b>
<b>🔎 ДАННЫЕ ПО НОМЕРУ:</b>

{bot_data}
"""
    
    result += f"""

<b>━━━━━━━━━━━━━━━━━━━━━━━━━</b>
<b>🕵️ Поиск от @antiseach_bot | Dixyi © 2025</b>
"""
    return result

def format_id_result(uid, data):
    return f"""
<b>🆔 РЕЗУЛЬТАТ ПОИСКА ПО ID</b>

<b>🆔 ID:</b> <code>{uid}</code>
<b>👤 Имя:</b> {data.get('first_name','?')}
<b>👤 Фамилия:</b> {data.get('last_name','?')}
<b>📛 Username:</b> @{data.get('username','?') if data.get('username') else 'Не указан'}
<b>📱 Телефон:</b> {data.get('phone') if data.get('phone') else 'Скрыт'}

<b>━━━━━━━━━━━━━━━━━━━━━━━━━</b>
<b>🕵️ Поиск от @antiseach_bot | Dixyi © 2025</b>
"""
