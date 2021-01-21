import persistence
from password_manager import hash_password


def get_statuses_by_board_id(board_id):
    board_status_connections = persistence.get_status_board_connections()
    statuses_to_board = []
    for connection in board_status_connections:
        if int(connection['board_id']) == board_id:
            new_status = {
                'id': connection['status_id'],
                'title': persistence.get_status_by_id(connection['status_id']),
                'order': connection['order']
            }
            statuses_to_board.append(new_status)
    return statuses_to_board


def get_card_status(status_id):
    """
    Find the first status matching the given id
    :param status_id:
    :return: str
    """
    statuses = persistence.get_statuses_dict()
    return next((status['title'] for status in statuses if status['id'] == str(status_id)), 'Unknown')


def get_boards(username='unknown'):
    boards = persistence.get_boards(force=True)
    boards_to_show = []
    for board in boards:
        # public boards
        if int(board['private']) == 0:
            boards_to_show.append(board)
        elif board['creator'] == username:
            boards_to_show.append(board)
    return boards_to_show


def get_cards_for_board_and_status(board_id, status_id):
    persistence.clear_cache()
    all_cards = persistence.get_cards()
    matching_cards = []
    for card in all_cards:
        if (card['board_id'] == str(board_id) and
            card['status_id'] == str(status_id) and
                card['archived'] == '0'):
            card['status_id'] = get_card_status(card['status_id'])
            matching_cards.append(card)
    return matching_cards


def delete_board(board_id):
    # delete board from boards.csv
    boards = persistence.get_boards()
    for board in boards:
        if board['id'] == str(board_id):
            boards.remove(board)
    persistence.export_data('boards')

    # delete board status connections to this board
    connections = persistence.get_status_board_connections()
    for conn in connections:
        if conn['board_id'] == str(board_id):
            connections.remove(conn)
    persistence.export_data('board_statuses')

    # delete cards connected to this boards
    cards = persistence.get_cards()
    for card in cards:
        if card['board_id'] == str(board_id):
            cards.remove(card)
    persistence.export_data('cards')


def add_board(board_name, creator_username="unknown", private=0):
    new_board = {"id": persistence.new_id_to_csv(persistence.BOARDS_FILE),
                 "title": board_name,
                 "creator": creator_username,
                 "private": private}
    persistence.get_boards().append(new_board)
    persistence.export_data("boards")

    # add starter statuses to new boards
    starter_statuses = [{
        'board_id': new_board['id'],
        'status_id': i,
        'order': persistence.new_order_number_to_board_status_connections(new_board['id'], i)} for i in range(0, 4)]
    board_status_connections = persistence.get_status_board_connections()
    for connection in starter_statuses:
        board_status_connections.append(connection)
    persistence.export_data('board_statuses')


def rename_board(board_id, new_name):
    for board in persistence.get_boards():
        if int(board["id"]) == board_id:
            board["title"] = new_name
    persistence.export_data("boards")


def add_new_status_to_board(board_id: int, new_status_name: str):
    if new_status_name in persistence.get_statuses_list():
        status_id = persistence.get_status_id_by_status_name(new_status_name)
        persistence.get_status_board_connections().append({
            'board_id': board_id,
            'status_id': status_id,
            'order': persistence.new_order_number_to_board_status_connections(board_id, status_id)
        })
        persistence.export_data('board_statuses')
    else:
        new_id = persistence.new_id_to_csv(persistence.STATUSES_FILE)
        new_status = {
            'id': new_id,
            'title': new_status_name
        }
        persistence.get_statuses_dict().append(new_status)
        persistence.export_data('statuses')
        persistence.get_status_board_connections().append({
            'board_id': board_id,
            'status_id': new_id,
            'order': persistence.new_order_number_to_board_status_connections(board_id, status_id)})
        persistence.export_data('board_statuses')


def add_card_to_board(board_id, card_title):
    new_card = {"id": persistence.new_id_to_csv(persistence.CARDS_FILE),
                "board_id": board_id,
                "title": card_title,
                "status_id": "0",
                "order": persistence.new_order_number_to_cards(board_id, 0),
                "archived": "0"}
    persistence.get_cards().append(new_card)
    persistence.export_data("cards")


def rename_card(id, new_name):
    for card in persistence.get_cards():
        if int(card["id"]) == id:
            card["title"] = new_name
    persistence.export_data("cards")


def get_board_by_id(board_id):
    boards = persistence.get_boards()
    # returns the board title
    return [board["title"] for board in boards if board["id"] == str(board_id)][0]


def get_card_by_id(card_id):
    cards = persistence.get_cards()
    # returns the card title
    return [card["title"] for card in cards if card["id"] == str(card_id)][0]


def user_not_exist(username):
    users = persistence.get_users()
    for user in users:
        if user['username'] == username:
            return False
    return True


def register_user(username, password):
    new_user = {"id": persistence.new_id_to_csv(persistence.USERS_FILE),
                "username": username,
                "password": hash_password(password)}
    persistence.get_users().append(new_user)
    persistence.export_data("users")


def delete_card(card_id):
    # delete from cards
    cards = persistence.get_cards()
    for card in cards:
        if int(card['id']) == card_id:
            cards.remove(card)
    persistence.export_data('cards')


def archive_card(card_id):
    cards = persistence.get_cards()
    for card in cards:
        if int(card['id']) == card_id:
            card['archived'] = '1'
    persistence.export_data('cards')


def rename_status(board_id, status_id, new_status):
    new_status_id = persistence.get_status_id_by_status_name(new_status)
    if new_status_id:
        pass
    else:
        new_status_id = persistence.new_id_to_csv(persistence.STATUSES_FILE)
        new_status = {'id': new_status_id,
                      'title': new_status}
        persistence.get_statuses_dict().append(new_status)
        persistence.export_data('statuses')

    cards = persistence.get_cards()
    for card in cards:
        if int(card['status_id']) == status_id and int(card['board_id']) == board_id:
            card['status_id'] = new_status_id
    persistence.export_data('cards')

    connections = persistence.get_status_board_connections()
    for connection in connections:
        if int(connection['board_id']) == board_id and int(connection['status_id']) == status_id:
            connection['status_id'] = new_status_id
            break
    persistence.export_data('board_statuses')


def delete_status(board_id, status_id):
    # delete status board connection
    connections = persistence.get_status_board_connections()
    for connection in connections:
        if connection['board_id'] == str(board_id) and connection['status_id'] == str(status_id):
            connections.remove(connection)
    persistence.export_data('board_statuses')

    # delete cards for this board and status
    cards = persistence.get_cards()
    for card in cards:
        if card['board_id'] == str(board_id) and card['status_id'] == str(status_id):
            cards.remove(card)
    persistence.export_data('cards')


def modify_card_status(board_id, new_status_id, card_id):
    cards = persistence.get_cards()
    for card in cards:
        if card['id'] == str(card_id):
            card['status_id'] = new_status_id
            card['order'] = persistence.new_order_number_to_cards(
                board_id, new_status_id)
    persistence.export_data('cards')


def modify_cards_order(cards_to_modify):
    # cards_to_modify: [{}, {}]
    # cards_to_modify[0]: {'card_id': 1, 'new_order': 0}

    cards = persistence.get_cards()
    for card in cards:
        for modified_ordered_card in cards_to_modify:
            if str(modified_ordered_card['card_id']) == str(card['id']):
                card['order'] = modified_ordered_card['new_order']
    persistence.export_data('cards')
