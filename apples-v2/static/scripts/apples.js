

var Player = function(init) {
    var self = {};
    self.id = init.id;
    self.username = init.username;
    self.type = init.player_type;
    self.score = 0;
    self.color = 'red';
    self.selected = null;
    self.hand = null;
    self.winner = false;
    self.draw = function() {
        if(self.id == selfId)
            self.color = 'blue';
    }

    Player.list[self.id] = self;
    return self;
}

Player.list = {};
var selfId = null;
var gameState = null;
var elements = document.getElementsByClassName('game_el');
var selectedCard = null;

var red_cards = document.getElementsByClassName("red_card");
for (var i = 0; i < red_cards.length; i++) {
  red_cards[i].addEventListener("click", function() {
    var current = document.getElementsByClassName("active");
    if (current.length > 0) {
        current[0].className = current[0].className.replace(" active", "");
    }
    this.className += " active";
  });
}

var socket = io.connect('http://'+document.domain+':'+location.port);
console.log('Conncted to apples server');
let current_game_id = null;
showHideElements('spectator', 'lobby');

/****************************************************
* Receive data from server via Websocket
*****************************************************/

socket.on('create_id', data => {selfId = data.your_id;});

socket.on('game_created', data => {alert(`Created game id: ${data.game}`)});

socket.on('game_not_found', () => {alert(`Game does not exist`)});

socket.on('joined_game', data => {
    var players = data.player_init;
    if (data.new_player.id == selfId) {
        // self just joined the game
        for(var i = 0; i < players.length; i++){
            var p = new Player(players[i]);
        }
        current_game_id = data.game_id;
        displayGameID(current_game_id);
    } else {
        // other player joined the game
        var p = new Player(data.new_player);
    }
});

// refresh game
socket.on('update_game', data => {
    if(data.winner_id) {
        if(Player.list[data.winner_id]){
            Player.list[data.winner_id].winner = true;
            showJudgeWinner(data.winner_id);
        }
    }
    updateGame(data.state, data.players);
    updateLeaderboard(data.players);
    if (data.selected_cards) {
        updateCards(data.selected_cards, 'red', false);
    }
    if(data.green_card) {
        updateCards(data.green_card, 'green', false);
    }
});

// refresh hand
socket.on('update_hand', data => {
    var me = Player.list[selfId];
    var oldHand = me.hand;
    if (oldHand != data.hand) {
        updateCards(data.hand, 'red', true);
    }
    me.hand = data.hand;
});

/****************************************************
* Update
*****************************************************/
function showJudgeWinner(id) {
    if (id) {
        var player = Player.list[id];
        var username = player.username;
        var text = username + ' has won!';
        var el = 'winner_message';
        if(player.type == 'judge'){
            text = 'Judge ' + username + ' presides';
            el = 'current_judge';
        }
        document.getElementById(el).innerHTML = text;
    }
}

function updateCards(cards, color, my_hand) {
    var len = cards.length;
    var targets = document.getElementsByClassName('red_card selected');
    if (color == 'red') {
        if(my_hand)
            targets = document.getElementsByClassName('red_card my_hand');
    } else {
        targets = document.getElementsByClassName('green_card');
    }
    for (var i=0; i<targets.length; i++) {
        targets[i].style.display = 'block';
        if (i > cards.length - 1) {
            targets[i].style.display = 'none';
        } else {
            targets[i].firstElementChild.innerHTML = cards[i].item;
            targets[i].lastElementChild.innerHTML = cards[i].description;
        }
    }
}

function updateLeaderboard(players) {
    var player_list = '';
    var spectator_list = 'Spectators';
    for(var i=0; i<players.length; i++){
        var p = players[i];
        var username = 'Unnamed';
            if(p.username.length > 0)
                username = p.username;
        if(p.player_type == 'spectator')
            spectator_list += '<br />' + username;
        else
            player_list += '<br />' + username + ': ' + p.score;
    }
    document.getElementById('player_list').innerHTML = player_list;
    document.getElementById('spectator_list').innerHTML = spectator_list;
}

function updateGame(state, players, green_card) {
    var judgeId = null;
    for (var i = 0; i < players.length; i++){
        var data = players[i];
        var p = Player.list[data.id];
        var oldScore = p.score;
        p.selected = data.selected_card;
        p.score = data.score;

        if(p.type == 'judge'){
            judgeId = p.id;
            showJudgeWinner(judgeId);
        }

        if ((gameState != state || (p.type != data.player_type)) && p.id == selfId) {
            showHideElements(data.player_type, state);
            gameState = state;
        }
        if(state != 'winner_selected')
            p.winner = false;

        p.type = data.player_type;
    }
}

function showHideElements(type, state) {
    console.log('type: ' + type + ', state: ' + state);
    if (Player.list[selfId] && Player.list[selfId].winner)
        type = 'winner';
    for (var i=0; i<elements.length; i++) {
        var el = elements[i];
        if (el.classList.contains(type) && el.classList.contains(state))
            el.style.display = 'block';
        else
            el.style.display = 'none';
    }
}

/****************************************************
* Send data to server via Websocket
*****************************************************/
document.querySelector('#join_game').onclick = () => {
    var game_id = document.querySelector('#game_id_input_text').value;
    var username = document.querySelector('#username_input_text').value;
    // TODO: add error message
    showHideDiv('game_div','home_page_id');
    startGame(username, game_id);
}


document.querySelector('#submit_btn_non_judge').addEventListener("mousedown", function() {
    sendSubmission();
})

document.querySelector('#submit_btn_judge').addEventListener("mousedown", function() {
    sendSubmission();
})

function sendSubmission(){
    var selected = document.getElementsByClassName('active')[0];
    if(selected){
        var item = selected.firstElementChild.innerHTML;
        console.log(item);
        var msg = {
            'card_item': item,
            'game_id': current_game_id
        }
        socket.emit('red_card_submission', msg);
    }
}

document.querySelector('#create_game').onclick = () => {
    socket.emit('create_game_request');
}

function leaveGame(game_id) {
    if (game_id !== null) {
        socket.emit('leave_game', {'game_id': game_id, 'username': username});
    }
}

function joinGame(game_id, username) {
    socket.emit('join_game', {'game_id': game_id, 'username': username});
}

/****************************************************
* Utilities
*****************************************************/
function displayGameID(game_id) {
    document.getElementById('game_id').innerHTML = 'Game ID: '+game_id;
}

function startGame(username, game_id) {
    leaveGame(current_game_id, username);
    joinGame(game_id, username);
    current_game_id = game_id;
}

document.querySelector('#show_rules_game_button').onclick = () => {
    showHideDiv('rules_page_id','game_div');
}

document.querySelector('#show_game_from_rules_button').onclick = () => {
    showHideDiv('game_div','rules_page_id');
}

function showHideDiv(newDiv, oldDiv) {
    console.log('changing view of ' + newDiv + ' and ' + oldDiv);
    document.getElementById(oldDiv).style.display = "none";
    document.getElementById(newDiv).style.display = "block";
}

