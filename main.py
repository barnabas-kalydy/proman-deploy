from flask import Flask, render_template, url_for, request, session, redirect
from password_manager import verify_password, get_password_hash_for_username
from util import json_response
import json

import data_handler

app = Flask(__name__)

# necessary to use sessions
app.secret_key = "randomword"


@app.route("/login-user", methods=["POST", "GET"])
def login_page():
    if request.method == "POST":
        if verify_password(request.form['password'],
                           get_password_hash_for_username(request.form["username"])):
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        else:
            return redirect(url_for("login_page"))
    return render_template("login.html")


@app.route("/register-user", methods=["POST", "GET"])
def register_page():
    if request.method == "POST":
        username = request.form['username']
        if data_handler.user_not_exist(username):
            password = request.form['password']
            data_handler.register_user(username, password)
            return redirect(url_for('login_page'))
    return render_template("register.html")


@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route("/", methods=['GET', 'POST'])
def index():
    # main page
    return render_template('index.html')


@app.route('/add-board', methods=['POST'])
def add_board():
    if request.method == 'POST':
        if session['username']:
            new_board_name = request.form['new_board_name']
            creator_username = session['username']
            if request.form['private'] == 'private':
                private = 1
            else:
                private = 0
            data_handler.add_board(new_board_name, creator_username=creator_username, private=private)

        else:
            new_board_name = request.form['new_board_name']
            data_handler.add_board(new_board_name)

    return redirect(url_for('index'))


@app.route('/rename/<int:board_id>', methods=['POST'])
def rename(board_id):
    if request.method == 'POST':
        data_handler.rename_board(board_id, request.form['newName'])
    return redirect(url_for('index'))


@app.route('/add-card/<int:board_id>', methods=['POST'])
def add_card_to_board(board_id):
    if request.method == 'POST':
        data_handler.add_card_to_board(board_id, request.form['newCardName'])
    return redirect(url_for('index'))


@app.route('/add-status-to-board/<int:board_id>', methods=['POST'])
def add_status_to_board(board_id):
    if request.method == 'POST':
        data_handler.add_new_status_to_board(board_id, request.form['newStatusName'])
    return redirect(url_for('index'))


@app.route('/delete-card/<int:card_id>', methods=['GET'])
def delete_card(card_id):
    if request.method == 'GET':
        data_handler.delete_card(card_id)
    return ''


@app.route('/archive-card/<int:card_id>')
def archive_card(card_id):
    data_handler.archive_card(card_id)
    return ''


@app.route('/rename-status/<int:board_id>/<int:status_id>/<new_status>')
def rename_status(board_id, status_id, new_status):
    data_handler.rename_status(board_id, status_id, new_status)
    return ''


@app.route('/delete-status/<int:board_id>/<int:status_id>')
def delete_status(board_id, status_id):
    data_handler.delete_status(board_id, status_id)
    return ''


@app.route('/delete-board/<int:board_id>')
def delete_board(board_id):
    data_handler.delete_board(board_id)
    return ''


@app.route('/modify-cards-order/<json_data>')
def modify_cards_order(json_data):
    cards_to_modify = json.loads(json_data)
    data_handler.modify_cards_order(cards_to_modify)
    return ''


@app.route("/get-boards")
@json_response
def get_boards():
    try:
        return data_handler.get_boards(session['username'])
    except KeyError:
        return data_handler.get_boards()


@app.route('/get-statuses-for-board/<int:board_id>')
@json_response
def get_statuses_for_board(board_id):
    return data_handler.get_statuses_by_board_id(board_id)


@app.route("/get-cards/<int:board_id>/<int:status_id>")
@json_response
def get_cards_for_board_and_status(board_id: int, status_id: int):
    return data_handler.get_cards_for_board_and_status(board_id, status_id)


@app.route("/rename-card/<int:card_id>/<new_name>")
def rename_card(card_id: int, new_name: str):
    data_handler.rename_card(card_id, new_name)
    return ''


@app.route('/modify-card-status/<int:board_id>/<int:new_status_id>/<int:card_id>')
def modify_card_status(board_id, new_status_id, card_id):
    data_handler.modify_card_status(board_id, new_status_id, card_id)
    return ''


def main():
    app.run(debug=True)

    # Serving the favicon
    with app.app_context():
        app.add_url_rule('/favicon.ico', redirect_to=url_for('static', filename='favicon/favicon.ico'))


if __name__ == '__main__':
    main()
