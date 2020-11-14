import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';


const home_page = (
    <div className="home_page">
        <div>Welcome</div>
        <div className="small">to the</div>
        <div>"Apples to Apples"</div>
        <div>Web App</div>
        <button className="play_button">Let's Play!</button>
    </div>

);


const rules_page = (
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
            <button>Start</button>
        </div>
    </div>
);


var initial = (
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
                <td className="player_icon">
                    <div className="mini_card">
                        <div className="mini_score">
                            <p>#</p>
                        </div>
                    </div>
                </td>
                <td></td>
                <td className="player_icon">
                    <div className="mini_card">
                        <div className="mini_score">
                            <p>#</p>
                        </div>
                    </div>
                </td>
                <td></td>
                <td className="player_icon">
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
            <button className="submit">Submit</button>
        </div>
        <br></br>
        <br></br>
        <div>
            <button className="chat">Chat</button>
        </div>
    </div>
    );


var judge_page = (
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
                <td className="player_icon">
                    <div className="mini_card">
                        <div className="mini_score">
                            <p>#</p>
                        </div>
                    </div>
                </td>
                <td></td>
                <td className="player_icon">
                    <div className="mini_card">
                        <div className="mini_score">
                            <p>#</p>
                        </div>
                    </div>
                </td>
                <td></td>
                <td className="player_icon">
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
            <button className="submit">Submit</button>
        </div>
        <br></br>
        <br></br>
        <div>
            <button className="chat">Chat</button>
        </div>
    </div>
);




ReactDOM.render(initial, document.getElementById('root'));
