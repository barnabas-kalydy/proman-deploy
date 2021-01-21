// (watch out: when you would like to use a property/function of an object from the
// object itself then you must use the 'this' keyword before. For example: 'this._data' below)
export let dataHandler = {
    _data: {}, // it is a "cache for all data received: boards, cards and statuses. It is not accessed from outside.
    _api_get: function (url, callback) {
        fetch(url, {
            method: 'GET',
            credentials: 'same-origin'
        })
        .then(response => response.json())  // parse the response as JSON
        .then(json_response => callback(json_response));  // Call the `callback` with the returned object
    },
    getBoards: function (callback) {
        this._api_get('/get-boards', (response) => {
            this._data['boards'] = response;
            callback(response);
        });
    },
    getStatusesByBoardId: function (boardId, callback) {
        this._api_get(`/get-statuses-for-board/${boardId}`, (response) => {
            callback(response);
        });
    },
    getCardsByBoardIdAndStatusId: function (boardId, statusId, callback) {
        "/get-cards/<int:board_id>/<int:status_id>"
            this._api_get(`/get-cards/${boardId}/${statusId}`, (response) => {
            callback(response);
        });
    },
};
