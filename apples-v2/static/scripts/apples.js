

var Player = function(init){
    var self = {};
    self.id = init.id;
    self.username = init.username;
    self.type = init.player_type;
    self.score = 0;
    self.color = 'red';
    self.cards = [];
    self.winner = false;

    self.update = function(pack){


    }

    self.draw = function(){
        if(self.id == selfId)
            self.color = 'blue';

    }

    Player.list[self.id] = self;
    return self;
}
Player.list = {};
var selfId = null;

document.addEventListener('DOMContentLoaded', () => {
    var socket = io.connect('http://'+document.domain+':'+location.port);
    console.log('Conncted to apples server');
    let current_game_id = null;

    /****************************************************
    * Receive data from server via Websocket
    *****************************************************/

    // game created
    socket.on('game_created', data => {alert(`Created game id: ${data.game}`)});

    // game not found
    socket.on('game_not_found', () => {alert(`Game does not exist`)});

    // self joined the game
    socket.on('joined_game', data => {
        var players = data.player_init;
        if(data.new_player.id == selfId){
            // self just joined the game
            for(var i = 0; i < players.length; i++){
                var p = new Player(players[i]);
                updateLeaderboard(p);
            }
            current_game_id = data.game_id;
            displayGameID(current_game_id);
        } else {
            // other player joined the game
            var p = new Player(data.new_player);
            updateLeaderboard(p);
        }
    });

    socket.on('create_id', data => {
        selfId = data.your_id;
    });

    // refresh game
    socket.on('update_game', data => {
        console.log('[client] updating game');
        updateGame(data.state, data.players);
    });

    // refresh hand
    socket.on('update_hand', data => {
        var me = Player.list[selfId];
        me.cards = data.hand;
    });

    /****************************************************
    * Update
    *****************************************************/
    function updateLeaderboard(player) {
        console.log(player.type);
        var text = document.getElementById(player.type).innerHTML;
        text += '<br />';
        if(player.username.length !== 0)
            text += player.username;
        else
            text += 'Unnamed';
        document.getElementById(player.type).innerHTML = text;
    }

    function updateGame(state, players) {
        console.log('updating game');



        /*
        var new_elem = document.createElement('div');
        new_elem.setArrtibute('class', 'player_score');
        new_elem.setArrtibute('id', username + '_score');
        new_elem.innerHTML = username 

        var score_card = document.getElementByClassName('score_card');
        score_card.innerHTML += new_elem;
        */
    };

    function displayGameID(game_id) {
        document.getElementById('game_id').innerHTML = 'Game ID: '+game_id;
    };

    /****************************************************
    * Send data to server via Websocket
    *****************************************************/
    document.querySelector('#join_game').onclick = () => {
        var game_id = document.querySelector('#game_id_input_text').value;
        var username = document.querySelector('#username_input_text').value;
        // TODO: add error message
        showHideDiv('game_div','home_page_id');
        startGame(username, game_id);
    };    

    document.querySelector('#submit_card_game_button').onclick = () => {
        var card = document.querySelector('#active_card').value;
        socket.emit('play_card', card);
    };

    // create game request
    document.querySelector('#create_game').onclick = () => {
        socket.emit('create_game_request');
    };

    function startGame(username, game_id) {
        leaveGame(current_game_id, username);
        joinGame(game_id, username);
        current_game_id = game_id;
    }

    function showHideDiv(newDiv, oldDiv) {
        console.log('changing view of ' + newDiv + ' and ' + oldDiv);
        document.getElementById(oldDiv).style.display = "none";
        document.getElementById(newDiv).style.display = "block";
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
    * Utilities
    *****************************************************/
    document.querySelector('#show_rules_game_button').onclick = () => {
        showHideDiv('rules_page_id','game_div');
    };

    document.querySelector('#show_game_from_rules_button').onclick = () => {
        showHideDiv('game_div','rules_page_id');
    };
})
