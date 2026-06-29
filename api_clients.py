
import re, asyncio, aiohttp
from telethon import TelegramClient
from config import *

async def lookup_htmlweb(phone):
    cleaned = re.sub(r'\D', '', phone)
    url = f'https://htmlweb.ru/geo/api.php?json&telcod={cleaned}'
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get(url, timeout=10) as resp:
                data = await resp.json()
                return {
                    'country': data.get('fullname','?'),
                    'region': data.get('region',{}).get('name','?'),
                    'city': data.get('0',{}).get('name','?'),
                    'operator': data.get('0',{}).get('oper','?'),
                    'brand': data.get('0',{}).get('oper_brand','?'),
                    'range': data.get('0',{}).get('def','?'),
                    'mobile': data.get('0',{}).get('mobile',False),
                    'timezone': data.get('tz','?'),
                    'postal': data.get('0',{}).get('post','?'),
                }
    except:
        return {'error': 'htmlweb не ответил'}

async def search_vk(query):
    url = f'https://api.vk.com/method/users.search?access_token={VK_TOKEN}&v=5.131&q={query}&fields=first_name,last_name,photo_max_orig'
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get(url, timeout=10) as resp:
                data = await resp.json()
                return data.get('response', [])
    except:
        return []

async def check_leaks(query):
    url = f'https://leakcheck.net/api/public?key={LEAKCHECK_KEY}&check={query}'
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get(url, timeout=15) as resp:
                data = await resp.json()
                if data.get('success'):
                    return data['result']
                return []
    except:
        return []

async def lookup_ip(ip):
    url = f'https://ipinfo.io/{ip}/json?token={IPINFO_KEY}'
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get(url, timeout=10) as resp:
                return await resp.json()
    except:
        return {}

async def lookup_mac(mac):
    url = f'https://api.macvendors.com/{mac}'
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get(url, timeout=10) as resp:
                return await resp.text()
    except:
        return None

async def search_by_id(user_id):
    client = TelegramClient(SESSION_PATH, API_ID, API_HASH)
    try:
        await client.start()
        entity = await client.get_entity(int(user_id))
        return {
            'first_name': entity.first_name or '',
            'last_name': entity.last_name or '',
            'username': entity.username or '',
            'phone': getattr(entity, 'phone', None)
        }
    except:
        return None
    finally:
        try:
            await client.disconnect()
        except:
            pass

async def search_bot(phone):
    client = TelegramClient(SESSION_PATH, API_ID, API_HASH)
    try:
        await client.start()
        await client.send_message(SEARCH_BOT, '/start')
        await asyncio.sleep(1.5)
        msg = (await client.get_messages(SEARCH_BOT, limit=1))[0]
        if msg.buttons:
            await msg.click(0,0)
            await asyncio.sleep(1)
            sub = (await client.get_messages(SEARCH_BOT, limit=1))[0]
            if sub.buttons:
                await sub.click(0,0)
                await asyncio.sleep(0.5)
                await client.send_message(SEARCH_BOT, phone)
                await asyncio.sleep(4)
                results = await client.get_messages(SEARCH_BOT, limit=5)
                for r in results:
                    if r.text and '📱' in r.text:
                        return r.text.replace('by ****@sjgdfj0ghjdhjjegtjjebot','').replace('by @sjgdfj0ghjdhjjegtjjebot','')
        return None
    except:
        return None
    finally:
        try:
            await client.disconnect()
        except:
            pass
