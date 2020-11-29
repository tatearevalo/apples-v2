

var Player = function(init){
    var self = {};
    self.id = init.id;
    self.username = init.username;
    self.type = init.player_type;
    self.score = 0;
    self.color = 'red';
    self.selected = null;
    self.hand = null;
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
var gameState = null;
var lastWinnerId = null;
var currentJudgeId = null;

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
        updateGame(data.state, data.players, data.green_card);
    });

    // refresh hand
    socket.on('update_hand', data => {
        var me = Player.list[selfId];
        var oldHand = me.hand;
        me.hand = data.hand;
        if(oldHand == null){
            for(var i=0; i < data.hand.length; i++){
                var card = data.hand[i];
                var cardDiv = document.createElement('div');
                cardDiv.setAttribute('class', 'hand_card');
                var cardItem = cardDiv.appendChild('span');
                cardItem.setAttribute('class', 'card_item');
                cardItem.textContent = card.item;
                var cardDesc = cardDiv.appendChild('span');
                cardDesc.setAttribute('class', 'card_desc');
                cardDesc.textContent = card.description;

                document.getElementById('my_hand').appendChild(cardDiv);
            }
        }

    });

    /****************************************************
    * Update
    *****************************************************/
    function updateLeaderboard(player) {
        console.log(player.type);
        var text = document.getElementById(player.type).innerHTML;
        text += '<br />';
        if (player.username.length !== 0)
            text += player.username;
        else
            text += 'Unnamed';
        document.getElementById(player.type).innerHTML = text;
    }

    function updateGame(state, players, greenCard) {
        console.log('updating game');

        for (var i = 0; i < players.length; i++){
            var data = players[i];
            var p = Player.list[data.id];
            var oldScore = p.score;
            p.type = data.player_type;
            p.selected = data.selected_card;

            if(p.type == 'judge')
                currentJudgeId = p.id;

            if (oldScore < data.score){
                p.winner = true;
                lastWinnerId = p.id;
                p.score = data.score;
                //update leaderboard
            }

            if(p.id == selfId){

            }

        }

        if (gameState != state){
            showNewState(gameState, state, greenCard);
            gameState = state;
        }
            }
    };

    function showNewState(oldState, newState, greenCard) {
        var msg = '';
        var me = Player.list[selfId];
        var myCardsDiv = document.getElementById('my_hand');
        var submitBtn = document.getElementById('submit_button');
        var greenCardDiv = document.getElementById('green_card');
        var playedCardsDiv = document.getElementById('selected_cards_container');

        //states include: lobby, submission, judging, winner
        if (newState == 'lobby'){
            msg = 'Waiting for players to join...';

            greenCardDiv.style.display = 'none';
            playedCardsDiv.style.display = 'none';
            submitBtn.style.display = 'none';

            //if olState != null, hide seleected cards 

        } else if(newState == 'submission'){
            if(me.type == 'active_player'){
                msg = 'Select a card to submit';
                submitBtn.style.display = 'block';
                myCardsDiv.style.display = 'block';
            }else{
                msg = 'Players are deliberating...';
                if(me.type == 'judge'){
                    msg += '<br />You are the judge';
                }
            }

            playedCardsDiv.style.display = 'none';
            greenCardDiv.style.display = 'block';
            document.getElementById('green_card_item').innerHTML = greenCard.item;
            document.getElementById('green_card_disc').innerHTML = greenCard.description;


            //oldState must be lobby, winner, null
            //if !spectator, show own hand, make hand cards selectable

        } else if(newState == 'judging'){
            if(me.type != 'judge'){
                submitBtn.style.display = 'none';
                var judge = Player.list[currentJudgeId];
                if(judge != null)
                    msg = 'Judge ' + judge.username + ' is deliberating...';
            }else{
                submitBtn.style.display = 'block';
                msg = 'Select the best card';
            }

            playedCardsDiv.style.display = 'block';
            //delete selected_cards, make new divs
            //if !judge, hide submit button
            //make hand cards unselectable
            //if selfid is judge, then make the hand cards darker,
            //and the selected_cards become selectable, and submit button show

        } else if(newState == 'winner'){
            if(me.winner){
                msg = 'Congratulations, you won!';
            }else{
                var username = Player.list[lastWinnerId].username;
                msg = username + 'has won!';
            }

            submitBtn.style.display = 'none';
            //highlight winner's selected_card

        }
        if(me.type == 'spectator' && oldState != 'lobby' && newState != 'lobby')
            msg += '<br />You are spectating';

        document.getElementById("game_message").innerHTML = msg;
    }

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

    document.querySelector('#submit_button').onclick = () => {
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
