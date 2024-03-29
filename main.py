from json import dump

from aiogram import types
from aiogram.utils import executor
from bs4 import BeautifulSoup as BS
from requests import get

from config import dp, bot


@dp.message_handler(text_startswith="username")
async def scanner(message: types.Message):
    """Для старта поиска необходимо написать боту сообщение в формате: username xxx"""
    u = message.text.replace('username ', '')
    save_json = {}
    social = {
        "instagram": f"https://instagram.com/{u}",
        "github": f"https://github.com/{u}",
        "career.habr": f"https://career.habr.com/{u}",
        "tiktok": f"https://tiktok.com/@{u}",
        "pikabu": f"https://pikabu.ru/@{u}",
        "reddit": f"https://reddit.com/user/{u}",
    }

    for j in social.values():
        try:
            req = get(j, timeout=5)
            code = req.status_code
        except:
            continue
        soup = BS(req.text, 'html.parser')
        user_info = soup.find('title')
        user_info2 = soup.find('a', class_='_31VWB3vSkv19o3I7RVE710')
        if u in str(user_info) or u in str(user_info2):
            user = "Found"
            if u not in save_json:
                save_json[u] = []
            save_json[u].append(j)
        elif code == 404:
            user = "Not Found"
        else:
            user = "undefined status code"
        print(user)
    with open(u + ".json", "w") as f:
        dump(save_json, f, indent=4)
    print(f"\n Data has been saved in {u}.json")

    message_text = f"Результаты поиска для пользователя {u}:\n\n"
    for i in save_json.get(u, []):
        message_text += f"{i}\n"
    await bot.send_message(chat_id=message.chat.id, text=message_text)


if __name__ == '__main__':
    print(__name__)
    executor.start_polling(dp, skip_updates=True)
