// It uses data_handler.js to visualize elements
import { dataHandler } from "./data_handler.js";

export let dom = {
    init: function () {

    },
    loadBoards: function () {
        dataHandler.getBoards(function (boards) {
            dom.showBoards(boards);
        });
    },
    showBoards: function (boards) {

        // shows boards appending them to #boards div
        let boardsDiv = document.getElementById('boards')

        for (let boardData of boards) {
            let board = document.createElement('section')
            board.setAttribute('class', 'board')
            board.setAttribute('id', `${boardData['id']}`)

            let boardHeader = document.createElement('div')
            boardHeader.setAttribute('class', 'board-header')
            
            let titleSpan = document.createElement('span')
            titleSpan.setAttribute('class', 'board-title')
            titleSpan.innerHTML = boardData['title'];
            titleSpan.onclick = () => {
                // rename board form
                let form = document.createElement('form')
                form.setAttribute('action', `/rename/${boardData['id']}`)
                form.setAttribute('method', 'POST')

                let inputField = document.createElement('input')
                inputField.name = 'newName'
                inputField.value = boardData['title']
                inputField.style.width = '200px'
                form.appendChild(inputField)

                let submitButton = document.createElement('button')
                submitButton.setAttribute('type', 'submit')
                submitButton.textContent = 'Rename Board!'
                form.appendChild(submitButton)

                boardHeader.innerHTML = ''
                boardHeader.appendChild(form)
            }
            boardHeader.appendChild(titleSpan)

            const addNewCardButton = document.createElement('button')
            addNewCardButton.setAttribute('class', 'board-add')
            addNewCardButton.textContent = 'New Card'
            addNewCardButton.onclick = () => {
                // add new card to board form
                let form = document.createElement('form')
                form.setAttribute('action', `/add-card/${boardData['id']}`)
                form.setAttribute('method', 'POST')

                let inputField = document.createElement('input')
                inputField.name = 'newCardName'
                inputField.style.width = '200px'
                form.appendChild(inputField)

                let submitButton = document.createElement('button')
                submitButton.setAttribute('type', 'submit')
                submitButton.textContent = 'Add New Card To Board!'
                form.appendChild(submitButton)

                boardHeader.innerHTML = ''
                boardHeader.appendChild(form)
            }
            boardHeader.appendChild(addNewCardButton)




            const addNewStatusButton = document.createElement('button')
            addNewStatusButton.setAttribute('class', 'board-add')
            addNewStatusButton.textContent = 'New Status'
            addNewStatusButton.onclick = () => {
                // add new status to board form
                let form = document.createElement('form')
                form.setAttribute('action', `/add-status-to-board/${boardData['id']}`)
                form.setAttribute('method', 'POST')

                let inputField = document.createElement('input')
                inputField.name = 'newStatusName'
                inputField.style.width = '200px'
                form.appendChild(inputField)

                let submitButton = document.createElement('button')
                submitButton.setAttribute('type', 'submit')
                submitButton.textContent = 'Add New Status To Board!'
                form.appendChild(submitButton)

                boardHeader.innerHTML = ''
                boardHeader.appendChild(form)
            }
            boardHeader.appendChild(addNewStatusButton)

            const deleteBoardSpan = document.createElement('button');
            deleteBoardSpan.setAttribute('class', 'board-add');
            deleteBoardSpan.innerHTML = "Delete board"
            deleteBoardSpan.addEventListener('click', () => {
                console.log(boardData.id)
                fetch(`/delete-board/${boardData.id}`);
                board.remove();
            });
            boardHeader.appendChild(deleteBoardSpan);


            const openCloseBoardButton = document.createElement('button')
            openCloseBoardButton.setAttribute('class', 'board-toggle')
            const iconToOpenCloseButton = document.createElement('i')
            iconToOpenCloseButton.setAttribute('class', 'fas fa-chevron-up')
            openCloseBoardButton.appendChild(iconToOpenCloseButton)

            const boardContent = document.createElement('div')

            const boardColumns = document.createElement('div')
            boardColumns.setAttribute('class', 'board-columns')
            boardColumns.setAttribute('id', `${boardData['id']}Columns`)
            boardContent.appendChild(boardColumns)

            openCloseBoardButton.onclick = () => {
                if (boardContent.style.display == 'none') {
                    boardContent.style.display = 'block'
                    iconToOpenCloseButton.setAttribute('class', 'fas fa-chevron-up')
                } else {
                    boardContent.style.display = 'none'
                    iconToOpenCloseButton.setAttribute('class', 'fas fa-chevron-down')
                }
            }
            boardHeader.appendChild(openCloseBoardButton)


            board.appendChild(boardHeader)

            dom.loadStatusesForBoard(boardData['id'])

            board.appendChild(boardContent)
            boardsDiv.appendChild(board)
        }

    },
    loadCards: function (boardId, statusId) {
        dataHandler.getCardsByBoardIdAndStatusId(boardId, statusId, (cards) => {
            dom.showCards(cards, boardId, statusId);
        });
    },
    showCards: function (cards, boardId, statusId) {
        let boardColumnContent = document.getElementById(`${boardId},${statusId}`)
        cards.sort((a, b) => (a.order > b.order) ? 1 : -1)
        for (let i = 0; i < cards.length; i++) {
            const card = document.createElement('div')
            card.setAttribute('class', 'card draggable')
            card.setAttribute('data-cardid', `${cards[i]['id']}`)
            card.setAttribute('data-order', `${i}`);
            card.setAttribute('draggable', 'true')
            const removeCardDiv = document.createElement('div')
            removeCardDiv.setAttribute('class', 'card-remove')
            removeCardDiv.addEventListener('click', (event) => {
                fetch(`/delete-card/${cards[i].id}`);
                card.remove();
            });
            const trashIcon = document.createElement('i')
            trashIcon.setAttribute('class', 'fas fa-trash-alt')
            removeCardDiv.appendChild(trashIcon)
            
            const cardArchiveDiv = document.createElement('div');
            cardArchiveDiv.setAttribute('class', 'card-archive');
            cardArchiveDiv.addEventListener('click', () => {
                fetch(`/archive-card/${cards[i].id}`)
                card.remove();
            });
            const archiveIcon = document.createElement('i');
            archiveIcon.setAttribute('class', 'fas fa-box-open');
            cardArchiveDiv.appendChild(archiveIcon);
            
            
            const cardTitle = document.createElement('div')
            cardTitle.setAttribute('class', 'card-title')
            cardTitle.setAttribute('data-value', cards[i]['title']);
            let innerCardTitleDiv = document.createElement('div');
            innerCardTitleDiv.innerHTML = cards[i]['title']
            cardTitle.appendChild(innerCardTitleDiv);

            innerCardTitleDiv.addEventListener('click', () => {
                let inputField = document.createElement('input');
                inputField.setAttribute('data-value', cardTitle.dataset.value);
                inputField.setAttribute('type','text');
                inputField.value = cardTitle.dataset.value;
                cardTitle.innerText = "";
                cardTitle.appendChild(inputField);
                inputField.addEventListener('keypress', (event) => {
                    if (event.key === 'Enter') {
                        fetch(`/rename-card/${cards[i]['id']}/${inputField.value}`);
                        cardTitle.innerHTML = `<div>${inputField.value}</div>`;
                    }
                });
            });

            card.appendChild(removeCardDiv)
            card.appendChild(cardArchiveDiv)
            card.appendChild(cardTitle)

            boardColumnContent.appendChild(card)

            card.addEventListener('dragstart', () => {
                card.classList.add('dragging');
            });

            card.addEventListener('dragend', (event) => {
                card.classList.remove('dragging');
                this.sortColumn(boardId, statusId, event)
            });
        }


    },
    loadStatusesForBoard: function (boardId) {
        dataHandler.getStatusesByBoardId(boardId, (statuses) => {
            dom.showStatuses(boardId, statuses);
        });
    },
    showStatuses: function (boardId, statuses) {
        const boardColumns = document.getElementById(`${boardId}Columns`)

        // sord statuses by order 
        statuses.sort((a, b) => (a.order > b.order) ? 1 : -1)

        for (const status of statuses) {
            let statusId = status['id']
            let statusName = status['title']
            const boardColumn = document.createElement('div')
            boardColumn.setAttribute('class', 'board-column')

            // set status to boardColumnTitle
            const boardColumnTitle = document.createElement('span')
            boardColumnTitle.setAttribute('class', 'board-column-title')
            boardColumnTitle.setAttribute('data-value', statusName);

            const innerBoardColTitleDiv = document.createElement('span')
            
            innerBoardColTitleDiv.addEventListener('click', () => {
                let inputField = document.createElement('input');
                inputField.setAttribute('data-value', boardColumnTitle.dataset.value)
                inputField.setAttribute('type', 'text');
                inputField.value = boardColumnTitle.dataset.value;
                boardColumnTitle.innerText = "";
                boardColumnTitle.appendChild(inputField);
                inputField.addEventListener('keypress', (event) => {
                    if (event.key === 'Enter') {
                        fetch(`/rename-status/${boardId}/${statusId}/${inputField.value}`)
                        boardColumnTitle.innerHTML= `<span>${inputField.value}</span>`;
                    }
                });
            });

            innerBoardColTitleDiv.innerHTML = statusName
            boardColumnTitle.appendChild(innerBoardColTitleDiv)
            boardColumn.appendChild(boardColumnTitle)
            const boardColumnContent = document.createElement('div')
            boardColumnContent.setAttribute('class', 'board-column-content card-slot')
            boardColumnContent.setAttribute('data-boardid', `${boardId}`);
            boardColumnContent.setAttribute('id', `${boardId},${statusId}`)
            
            let removeStatusSpan = document.createElement('span');
            removeStatusSpan.setAttribute('class', 'status-remove');
            const trashIcon = document.createElement('i')
            trashIcon.setAttribute('class', 'fas fa-trash-alt')
            removeStatusSpan.appendChild(trashIcon);
            boardColumn.appendChild(removeStatusSpan);
            removeStatusSpan.addEventListener('click', () => {
                fetch(`/delete-status/${boardId}/${statusId}`)
                boardColumn.remove();
            });


            // show items in columns
            dom.loadCards(boardId, statusId)

            boardColumn.appendChild(boardColumnContent)

            boardColumns.appendChild(boardColumn)

            boardColumnContent.addEventListener('dragover', (event) => {
                event.preventDefault();
                const card = document.querySelector('.dragging');
                const afterElement = this.getDragAfterElement(boardColumnContent, event.clientY);
                if (boardColumnContent.dataset.boardid === card.parentNode.dataset.boardid) {
                    if (afterElement == null) {
                        boardColumnContent.appendChild(card);
                    } else {
                        boardColumnContent.insertBefore(card, afterElement);
                    }
                    fetch(`/modify-card-status/${boardId}/${statusId}/${card.dataset.cardid}`)
                }
            });
        }


    },
    sortColumn: function(board_id, status_id, event) {
        let obj = []
        
        let nodes = event.target.parentNode.childNodes;
        for (let i = 0; i < nodes.length; i++) {
            nodes[i].dataset.order = i;
            let valami = {
                'card_id': nodes[i].dataset.cardid,
                'new_order': nodes[i].dataset.order
            }
            obj.push(valami);
        }
        let json = JSON.stringify(obj);
        fetch(`/modify-cards-order/${json}`);
    },
    getDragAfterElement: function(container, y) {
        let draggableElements = [...container.querySelectorAll('.draggable:not(.dragging)')];
        return draggableElements.reduce((closest, child) => {
            const box = child.getBoundingClientRect();
            const offset = y - box.top - box.height / 2;
            if (offset < 0 && offset > closest.offset) {
                return { offset: offset, element: child};  
            } else {
                return closest;
            }
        }, {offset: Number.NEGATIVE_INFINITY}).element;
    }
};
