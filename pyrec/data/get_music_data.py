import os
from pyrec.config import DATA_DIR


def parse_line(line):
    user_id, song_info = line.split(',', maxsplit=1)
    user_id = int(user_id)
    song_info = song_info.rstrip()

    return user_id, song_info


def get_music_data(file_name, max_lines_num=10000):
    user_items = {}
    with open(os.path.join(DATA_DIR, file_name)) as file_:
        for i, line in enumerate(file_):
            if i >= max_lines_num:
                break
            user_id, song_info = parse_line(line)
            if user_id in user_items:
                user_items[user_id].append(song_info)
            else:
                user_items[user_id] = [song_info]
    return user_items
