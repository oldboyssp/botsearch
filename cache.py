
import json, os, time

CACHE_DIR = "./cache_data"
CACHE_TTL = 3600  # Время жизни кэша — 1 час

def get_cache(key):
    filepath = f"{CACHE_DIR}/{key}.json"
    if not os.path.exists(filepath):
        return None
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        if time.time() - data['timestamp'] > CACHE_TTL:
            os.remove(filepath)
            return None
        return data['value']
    except:
        return None

def set_cache(key, value):
    filepath = f"{CACHE_DIR}/{key}.json"
    with open(filepath, 'w') as f:
        json.dump({'value': value, 'timestamp': time.time()}, f)

def clear_cache():
    for f in os.listdir(CACHE_DIR):
        os.remove(os.path.join(CACHE_DIR, f))

def cache_stats():
    files = os.listdir(CACHE_DIR)
    return {'files': len(files), 'dir': CACHE_DIR}
