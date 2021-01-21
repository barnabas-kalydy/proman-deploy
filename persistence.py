import csv
from csv import reader

STATUSES_FILE = './data/statuses.csv'
BOARDS_FILE = './data/boards.csv'
CARDS_FILE = './data/cards.csv'
USERS_FILE = './data/users.csv'
BOARD_STATUSES_FILE = './data/board_statuses.csv'
FILE_HEADERS = {"statuses": ["id", "title"],
                "cards": ["id", "board_id", "title", "status_id", "order", "archived"],
                "boards": ["id", "title", "creator", "private"],
                "users": ["id", "username", "password"],
                "board_statuses": ["board_id", "status_id", "order"]}

_cache = {}


def _read_csv(file_name):
    """
    Reads content of a .csv file
    :param file_name: relative path to data file
    :return: OrderedDict
    """
    with open(file_name) as boards:
        rows = csv.DictReader(boards, delimiter=',', quotechar='"')
        formatted_data = []
        for row in rows:
            formatted_data.append(dict(row))
        return formatted_data


def _get_data(data_type, file, force):
    """
    Reads defined type of data from file or cache
    :param data_type: key where the data is stored in cache
    :param file: relative path to data file
    :param force: if set to True, cache will be ignored
    :return: OrderedDict
    """
    if force or data_type not in _cache:
        _cache[data_type] = _read_csv(file)
    return _cache[data_type]


def export_data(data_type):
    file_name = f"./data/{data_type}.csv"
    data = _cache[data_type]
    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=FILE_HEADERS[data_type])
        writer.writeheader()
        for data_row in data:
            writer.writerow(data_row)


def clear_cache():
    _cache.clear()


def get_status_by_id(status_id, force=False):
    statuses = _get_data('statuses', STATUSES_FILE, force)
    for status in statuses:
        if status['id'] == str(status_id):
            return status['title']


def get_status_id_by_status_name(status_name, force=False):
    statuses = _get_data('statuses', STATUSES_FILE, force)
    for status in statuses:
        if status['title'] == status_name:
            return status['id']


def get_statuses_dict(force=False):
    return _get_data('statuses', STATUSES_FILE, force)


def get_status_board_connections(force=False):
    return _get_data('board_statuses', BOARD_STATUSES_FILE, force)


def get_statuses_list():
    with open('./data/statuses.csv', 'r') as read_obj:
        csv_reader = reader(read_obj)
        list_of_rows = list(csv_reader)
        statuses = [status[1]
                    for status in list_of_rows if status[1] != "title"]
    return statuses


def get_boards(force=False):
    return _get_data('boards', BOARDS_FILE, force)


def get_cards(force=False):
    return _get_data('cards', CARDS_FILE, force)


def get_users(force=False):
    return _get_data('users', USERS_FILE, force)


def new_id_to_csv(csv_name):
    try:
        return int(_read_csv(csv_name)[-1]["id"]) + 1
    except IndexError:
        return 1


def new_order_number_to_cards(board_id, status_id):
    try:
        return int(max([card["order"] for card in _read_csv(CARDS_FILE)
                        if card["board_id"] == str(board_id) and card["status_id"] == str(status_id)])) + 1
    except ValueError:
        return 0


def new_order_number_to_board_status_connections(board_id, status_id):
    try:
        return int(max([connection["order"] for connection in _read_csv(BOARD_STATUSES_FILE)
                        if connection["board_id"] == str(board_id) and connection["status_id"] == str(status_id)])) + 1
    except ValueError:
        return 0
