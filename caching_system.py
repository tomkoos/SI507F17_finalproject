import json

CACHE_FNAME = "cache_contents.json"

try:
    with open(CACHE_FNAME, 'r', encoding='utf-8-sig') as cache_file:
        cache_json = cache_file.read()
        CACHE_DICTION = json.loads(cache_json)
except:
    CACHE_DICTION = {}

def get_from_cache(identifier, dictionary=CACHE_DICTION):
    identifier = identifier.upper()
    if identifier in dictionary:
        data = dictionary[identifier]['values']
    else:
        data = None
    return data

def set_in_data_cache(identifier, data):
    identifier = identifier.upper()
    CACHE_DICTION[identifier] = {'values': data}
    with open(CACHE_FNAME, 'w', encoding='utf-8-sig') as cache_file:
        cache_json = json.dumps(CACHE_DICTION)
        cache_file.write(cache_json)

def create_cache_name_to_id(diction):
  with open('name_to_id.json', 'w', encoding='utf-8-sig') as cache_file:
        cache_json = json.dumps(diction)
        cache_file.write(cache_json)