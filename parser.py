import re

def parse_anime_name(name):
    name = re.sub(r'\[.*?\]', '', name)
    name = re.sub(r'\(.*?\)', '', name)
    name = re.sub(r' - \d+.*', '', name)
    name = re.sub(r'\d{1,3}.*', '', name)
    return name.strip() or "Unknown"