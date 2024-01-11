from flask import render_template
import json

def home():
    # users.jsonからプレイヤー情報をロードする
    with open('users.json') as f:
        users = json.load(f)
    # usersをplayersとして渡す
    return render_template('input.html', players=users.values())
