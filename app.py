import json

from bs4 import BeautifulSoup as BS
from flask import Flask, render_template, request, jsonify
from requests import get

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    u = request.form['username']

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

    with open(f"{u}.json", "w") as f:
        json.dump(save_json, f, indent=4)

    return jsonify(save_json)


if __name__ == '__main__':
    app.run(debug=True)
