import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom';
import apple from './apple.png';
import './index.css';

/* ========================== Websockets ================================ */

document.addEventListener('DOMContentLoaded', () => {
    var socket = io.connect('http://'+document.domain+':'+location.port);

    socket.on('connect', () => {
        socket.send('I am connected');
    });

    socket.on('message', data => {
        if ('new_game' in data) {   
            window.alert(`Created game id: ${data.new_game}`)
        }
        if ('join_game' in data) {
            console.log(`Joining game: ${data.game_id}`);
        }
        if ('game_not_found' in data) {
            window.alert(`Game does not exist.`)
        }
    });

    socket.on('event_handler', data => {
        console.log(data);
    });

    document.querySelector('#create_game').onclick = () => {
        var message = {
            'type':'create_game_request',
            'data':'None'
        };
        socket.send(message);
    }

    document.querySelector('#join_game').onclick = data => {
        var message = {
            'type':'join_game',
            'data':document.querySelector('#game_id_text').value
        };
        socket.send(message);
    }
})
/* ==================================================================== */

var win = 0;
function homeClick() {
    ReactDOM.render(<Rules />, document.getElementById('root'));
}

function rulesClick() {
    ReactDOM.render(<Start />, document.getElementById('root'));
}

function startClick() {
    console.log(document.getElementById('root'));
    ReactDOM.render(<Judge />, document.getElementById('root'));
}

function judgeClick() {
    if (win < 2) {
        ReactDOM.render(<Start />, document.getElementById('root'));
        alert("Player # gets the Green Card!");
    } else {
        win = 0;
        ReactDOM.render(<Home />, document.getElementById('root'));
        alert("Player # Wins!");
    }

    win += 1;
}

function Home() {
    return (
        <div className="home_page">
            <img src={apple} height={100} width={100}/>
            <img src={apple} height={100} width={100}/>
            <img src={apple} height={100} width={100}/>
            <img src={apple} height={100} width={100}/>
            <img src={apple} height={100} width={100}/>
            <img src={apple} height={100} width={100}/>
            <img src={apple} height={100} width={100}/>
            <div>Welcome</div>
            <div className="small">to the</div>
            <div>"Apples to Apples"</div>
            <div>Web App</div>
            <button onClick={homeClick} className="play_button">Play!</button>

            <div className="start_button">
                <button id="create_game">Create New Game</button>
            </div>

            <div id="game_id_input">
                <input type="text" id="game_id_text" placeholder="Game ID"></input>
                <button type="button" id="join_game">Join Game</button>
            </div>

            <div className="apples">
                <img src={apple} height={100} width={100}/>
                <img src={apple} height={100} width={100}/>
                <img src={apple} height={100} width={100}/>
                <img src={apple} height={100} width={100}/>
                <img src={apple} height={100} width={100}/>
                <img src={apple} height={100} width={100}/>
                <img src={apple} height={100} width={100}/>
            </div>
        </div>
    );
}

function Rules() {
    return (
        <div>
            <h1 className="title">"Apples to Apples"</h1>
            <h2 className="header">How to Play</h2>
            <div className="rules">
                <ol>
                    <li>One of the players will be randomly assigned to be the judge.</li>
                    <li>All players will be dealt a private hand of seven red apple cards.</li>
                    <li>A green apple card will be selected from the top of the stack and shown to all players.</li>
                    <li>Players must then quickly choose the red apple card from their hand that they feel is best described by the green apple card.</li>
                    <li>Once each player picks their red apple card, they must submit that card to the judge.</li>
                    <li>The judge then views the chosen red apple cards but does not know who chose which cards.</li>
                    <li>The chosen red apple cards are shown for all players to see with identities still hidden.</li>
                    <li>Judge then selects the red apple card he or she thinks is best described by the green apple card.</li>
                    <li>The player whose red apple card is selected by the judge is the winner of the round and is awarded the green apple card.</li>
                    <li>To keep score, players count the green apple cards that they have won.</li>
                    <li>After each round, the red apple cards are discarded and a new set of seven red apple cards are dealt to each player again.</li>
                    <li>The role of judge is passed on to the next player and the next round begins</li>
                    <li>The first player to reach a certain number of green cards wins the game!</li>
                </ol>
            </div>
            <div className="start_button">
                <button onClick={rulesClick}>Start</button>
            </div>
        </div>
    );
}


function Start() {
    return (
        <div>
            <div className="page_title">Apples to Apples</div>
            <div className="top_level">
                <div className="score_card">
                    <div className="score">
                        Green Cards
                    </div>
                    <div className="player_score">Player 1: #</div>
                    <div className="player_score">Player 2: #</div>
                    <div className="player_score">Player 3: #</div>
                    <div className="player_score">Player 4: #</div>
                </div>
                <div className="green_card">
                    <div className="container">
                        <h4>Green Card</h4>
                        <p>Content</p>
                    </div>
                </div>
            </div>
            <table className="center">
                <tr>
                    <th>Player 2</th>
                    <td></td>
                    <th>Player 3</th>
                    <td></td>
                    <th>Player 4</th>
                </tr>
                <tr>
                    <td >
                        <img src={apple} height={110} width={110}/>
                        <div className="mini_card">
                            <div className="mini_score">
                                <p>#</p>
                            </div>
                        </div>
                    </td>
                    <td></td>
                    <td >
                        <img src={apple} height={110} width={110}/>
                        <div className="mini_card">
                            <div className="mini_score">
                                <p>#</p>
                            </div>
                        </div>
                    </td>
                    <td></td>
                    <td >
                        <img src={apple} height={110} width={110}/>
                        <div className="mini_card">
                            <div className="mini_score">
                                <p>#</p>
                            </div>
                        </div>
                    </td>
                </tr>
            </table>
            <br></br>
            <br></br>
            <br></br>
            
            <div className="my_card">
                <div className="my_card_score">
                    #
                </div>
            </div>
        
            <br></br>
            <div className="cards">
                <button className="red_card">
                    <div className="container">
                        <h4>Red Card</h4>
                    </div>
                </button>
                <button className="red_card">
                    <div className="container">
                        <h4>Red Card</h4>
                    </div>
                </button>
                <button className="red_card">
                    <div className="container">
                        <h4>Red Card</h4>
                    </div>
                </button>
                <button className="red_card">
                    <div className="container">
                        <h4>Red Card</h4>
                    </div>
                </button>
                <button className="red_card">
                    <div className="container">
                        <h4>Red Card</h4>
                    </div>
                </button>
                <button className="red_card">
                    <div className="container">
                        <h4>Red Card</h4>
                    </div>
                </button>
                <button className="red_card">
                    <div className="container">
                        <h4>Red Card</h4>
                    </div>
                </button>
            </div>
            <div>
                <button onClick={startClick} className="submit">Submit</button>
            </div>
            <br></br>
            <br></br>
            <div>
                <button className="chat">Chat</button>
            </div>
        </div>
    );
}


function Judge() {
    return (
        <div>
            <div className="page_title">Apples to Apples</div>
            <div className="top_level">
                <div className="score_card">
                    <div className="score">
                        Green Cards
                    </div>
                    <div className="player_score">Player 1: #</div>
                    <div className="player_score">Player 2: #</div>
                    <div className="player_score">Player 3: #</div>
                    <div className="player_score">Player 4: #</div>
                </div>
            </div>
            <table className="center">
                <tr>
                    <th>Player 2</th>
                    <td></td>
                    <th>Player 3</th>
                    <td></td>
                    <th>Player 4</th>
                </tr>
                <tr>
                    <td >
                        <img src={apple} height={110} width={110}/>
                        <div className="mini_card">
                            <div className="mini_score">
                                <p>#</p>
                            </div>
                        </div>
                    </td>
                    <td></td>
                    <td >
                        <img src={apple} height={110} width={110}/>
                        <div className="mini_card">
                            <div className="mini_score">
                                <p>#</p>
                            </div>
                        </div>
                    </td>
                    <td></td>
                    <td >
                        <img src={apple} height={110} width={110}/>
                        <div className="mini_card">
                            <div className="mini_score">
                                <p>#</p>
                            </div>
                        </div>
                    </td>
                </tr>
            </table>
            <br></br>
            <br></br>
            <br></br>
            <br></br>
            <br></br>
        
            <div className="judge_prompt">
                Pick the Winner!
            </div>
        
            <br></br>
            <div className="cards">
                <button className="red_card">
                    <div className="container">
                        <h4>Red Card</h4>
                    </div>
                </button>
                <button className="red_card">
                    <div className="container">
                        <h4>Red Card</h4>
                    </div>
                </button>
                <button className="red_card">
                    <div className="container">
                        <h4>Red Card</h4>
                    </div>
                </button>
                <button className="judge_green_card">
                    <div className="container">
                        <h4>Green Card</h4>
                    </div>
                </button>
            </div>
            <div>
                <button onClick={judgeClick} className="submit">Submit</button>
            </div>
            <br></br>
            <br></br>
            <div>
                <button className="chat">Chat</button>
            </div>
        </div>
    );
}

ReactDOM.render(<Home />, document.getElementById('root'));
