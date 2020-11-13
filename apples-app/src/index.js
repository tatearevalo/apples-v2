import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';


const rules_page = (
    <div>
        <h1 className="title">Welcome to the "Apples to Apples" Online App</h1>
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
            <button>Let's Play</button>
        </div>
    </div>
);


var initial = (
    <div>
        <table className="center">
            <tr>
                <th>Player 2</th>
                <th>Player 3</th>
                <th>Player 4</th>
            </tr>
            <tr>
                <td className="player_icon"></td>
                <td className="player_icon"></td>
                <td className="player_icon"></td>
            </tr>
        </table>
        <div className="red_card"></div>
    </div>


    );




ReactDOM.render(initial, document.getElementById('root'));
