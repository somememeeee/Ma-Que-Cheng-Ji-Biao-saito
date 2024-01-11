from flask import Flask
import os
from home import home
from view import view
from submit_scores import submit_scores
app = Flask(__name__)

app.add_url_rule('/', 'home', home)
app.add_url_rule('/view', 'view', view)
app.add_url_rule('/submit', 'submit_scores', submit_scores, methods=['POST'])



# ターミナルをクリアする関数
def clear_console():
    command = 'clear'  # Unix/Linux/MacOS
    if os.name in ('nt', 'dos'):  # Windows
        command = 'cls'
    os.system(command)

if __name__ == '__main__':
    clear_console()  # コンソールをクリアする
    app.run(host='0.0.0.0', port=8080, debug=True)
    clear_console()  # コンソールをクリアする
