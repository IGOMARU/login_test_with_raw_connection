from flask import Flask
from flask import request
from flask import redirect
from flask import render_template
from flask import url_for

from login_database.login_main import LoginMain

app = Flask(__name__)


@app.route('/')
def index():
    connector = LoginMain()
    try:
        connector.create_table()
    except Exception:
        pass
    return redirect(url_for('register_info'))

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('pass')
        connector = LoginMain()
        checker = connector.login_check(name, password)
        if checker:
            return checker
        else:
            return '<h1>ログインに失敗しました</h1>'
    return render_template('login_input.html')

@app.route('/register', methods=['GET', 'POST'])
def register_info():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('pass')
        connector = LoginMain()
        response = connector.insert_data(name, password)
        if response:
            return redirect(url_for('login'))
        else:
            return '<h1>エラーが発生しました</h1>'

    return render_template('register_input.html')


if __name__ == '__main__':
    app.run()
