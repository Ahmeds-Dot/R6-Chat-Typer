import json
import os
import time

import keyboard
from typing import List


def get_keys() -> dict:
    try:
        with open("keys.json", "r") as keys_file:
            data = json.load(keys_file)
    except FileNotFoundError:
        with open("keys.json", "w") as keys_file:
            keys_file.write("{}")
        data = {}
    return data


def load_keys(keys_: dict) -> None:
    os.system("cls")
    print("Keys Loaded:")
    for key in keys_.keys():
        value: str = keys_.get(key)
        keyboard.add_hotkey(key, key_write, args=(key, value))
        print(" ", key, "->", value[:100] + "..." if len(value) > 100 else value)


def refresh_keys(hotkey: str):
    keyboard.remove_all_hotkeys()
    keyboard.add_hotkey(hotkey, refresh_keys, args=(hotkey,))
    load_keys(get_keys())


try:
    with open("settings.json", "r") as settings_file:
        settings: dict = json.load(settings_file)
except FileNotFoundError:
    with open("settings.json", "w+") as settings_file:
        settings_file.write(json.dumps(
            {
                "Keyboard Input Delay": 0.008,
                "Character Limit Break": 127,
                "Text Chat Button": "t",
                "Refresh Keys": "ctrl+`"
            }
        ))
        settings: dict = json.load(settings_file)
finally:
    KEY_IN_DELAY: float = settings.get("Keyboard Input Delay")
    CHAR_LIMIT: int = settings.get("Character Limit Break")
    TEXT_CHAT_BUTTON: str = settings.get("Text Chat Button")
    REFRESH_KEY: str = settings.get("Refresh Keys")
    keyboard.add_hotkey(REFRESH_KEY, refresh_keys, args=(REFRESH_KEY,))


def split_chars(string: str, limit: int = CHAR_LIMIT) -> List[str]:
    if len(string) <= limit:
        return [string]

    idx = 0
    last = limit
    lst = []

    while len(string[idx:]) >= limit:
        lst.append(string[idx:last])
        idx += limit
        last += limit
    lst.append(string[idx:last])

    return lst


def better_press(key: str) -> None:
    time.sleep(KEY_IN_DELAY)
    keyboard.press(key)
    time.sleep(KEY_IN_DELAY)
    keyboard.release(key)
    time.sleep(KEY_IN_DELAY)


def key_write(key, string: str) -> None:
    if len(string) > CHAR_LIMIT:
        for substr in split_chars(string):
            better_press(TEXT_CHAT_BUTTON)
            keyboard.write(substr, delay=KEY_IN_DELAY)
            better_press("enter")
    else:
        better_press(TEXT_CHAT_BUTTON)
        keyboard.write(string, delay=KEY_IN_DELAY)
        better_press('enter')

    keyboard.release(key)


keys = get_keys()

if not keys:
    print("No Keyboard Shortcuts Detected. Add some in 'keys.json' in this folder.\n\nExample: {\"ctrl+1\":\"GG!\"}")
    input()
    exit()

load_keys(keys)

keyboard.wait()
