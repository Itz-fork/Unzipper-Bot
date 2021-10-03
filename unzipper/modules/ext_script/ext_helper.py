# Copyright (c) 2021 Itz-fork
# Don't kang this else your dad is gae
import subprocess
import os

from pyrogram.types import InlineKeyboardButton

async def extract_with_7z_helper(path, archive_path, password=None):
    if password:
        command = f"7z x -o{path} -p{password} {archive_path} -y"
    else:
        command = f"7z x -o{path} {archive_path} -y"
    ext_cmd = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    ext_out = ext_cmd.stdout.read()[:-1].decode("utf-8")
    return ext_out

# Get files in directory as a list
def get_files(path):
    path_list = []
    for r, d, f in os.walk(path):
        for file in f:
            path_list.append(os.path.join(r, file))
    return path_list

# Make keyboard
async def make_keyboard(paths, user_id, chat_id):
    num = 0
    i_kbd = []
    for file in paths:
        i_kbd.append(
            [InlineKeyboardButton(f"{num} - {os.path.basename(file)}", f"ext_f|{user_id}|{chat_id}|{num}")]
        )
        num += 1
    i_kbd.append(
        [InlineKeyboardButton(f"Upload All ♻️", f"ext_a|{user_id}|{chat_id}")]
    )
    i_kbd.append(
        [InlineKeyboardButton("Cancel ❌", callback_data="cancel_dis")]
    )
    return i_kbd
