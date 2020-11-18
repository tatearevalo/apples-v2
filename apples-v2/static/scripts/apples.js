
document.addEventListener('DOMContentLoaded', () => {
    var socket = io.connect('http://'+document.domain+':'+location.port);
    let current_game_id = null;

    /****************************************************
    * Receive data from server via Websocket
    *****************************************************/

    // connection
    socket.on('connect', () => {console.log('Connected with apples server.')});

    // game created
    socket.on('game_created', data => {alert(`Created game id: ${data.game}`)});

    // game not found
    socket.on('game_not_found', () => {alert(`Game does not exist`)});

    // new player joined the game
    socket.on('joined_game', data=> {
        console.log(`joined: ${data.game_id}`)
    });


    /****************************************************
    * Send data to server via Websocket
    *****************************************************/

    // create game request
    document.querySelector('#create_game').onclick = () => {
        socket.emit('create_game_request');
    };

    // join game 
    document.querySelector('#join_game').onclick = data => {
        var game_id = document.querySelector('#game_id_input_text').value;
        var username = document.querySelector('#username_input_text').value;
        leaveGame(current_game_id, username);
        joinGame(game_id, username);
        current_game_id = game_id;
        window.location.href = '/game/' + current_game_id;
        console.log('hellow ');
        addPlayerToGame(username);
    };

    function leaveGame(game_id) {
        if (game_id !== null) {
            socket.emit('leave_game', {'game_id': game_id, 'username': username});
        }
    };

    function joinGame(game_id, username) {
        socket.emit('join_game', {'game_id': game_id, 'username': username});
    };

    /****************************************************
    * Update html of game page
    *****************************************************/
    // TODO - need to stop rendering templates. instead,
    // we should just clear all of the HTML with javascript
    // and build the game board with javascript

    function addPlayerToGame(username) {
        console.log('adding ' + username);
        var new_elem = document.createElement('div');
        new_elem.setArrtibute('class', 'player_score');
        new_elem.setArrtibute('id', username + '_score');
        new_elem.innerHTML = username 

        var score_card = document.getElementByClassName('score_card');
        score_card.innerHTML += new_elem;
    };

})
