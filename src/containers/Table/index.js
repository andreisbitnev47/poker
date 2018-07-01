import React, { Component } from 'react';
import './Table.css';
import Player from '../Player';

class Table extends Component {
    constructor(props) {
        super(props);
        const sbPlayer = 0;
        props.table.players.forEach((player, index) => {
            player.position = this.givePosition(index, sbPlayer, props.table.players.length)
        });
        this.state = {
            sbPlayer,
            update: props.update,
            table: props.table,
            activePosition: 0,
            pot: 0,
            deck: [],
            board: []
        }
    }

    givePosition(playerIndex, sbPlayer, playersCnt) {
        const positions = ['SB', 'BB', 'UTG', 'UTG+1', 'UTG+2', 'MP1', 'MP2', 'C', 'B'];
        //not needed here
        const positionsMap = {'B': 6, 'SB': 7, 'BB': 8, 'UTG': 0, 'UTG+1': 1, 'UTG+2': 2, 'MP1': 3, 'MP2': 4, 'C': 5};
        const positionsCorrectionObj = {
            '9': ['SB', 'BB', 'UTG', 'UTG+1', 'UTG+2', 'MP1', 'MP2', 'C', 'B'], 
            '8': ['SB', 'BB', 'UTG+1', 'UTG+2', 'MP1', 'MP2', 'C', 'B'], 
            '7': ['SB', 'BB', 'UTG+2', 'MP1', 'MP2', 'C', 'B'], 
            '6': ['SB', 'BB', 'MP1', 'MP2', 'C', 'B'], 
            '5': ['SB', 'BB', 'MP2', 'C', 'B'], 
            '4': ['SB', 'BB', 'C', 'B'], 
            '3': ['SB', 'BB', 'B'], 
            '2': ['SB', 'BB']
        };
        const correctedPositions = positionsCorrectionObj[playersCnt.toString()];
        if(playerIndex === sbPlayer) {
            return 'SB'
        }
        const positionindex = playerIndex - sbPlayer;
        const correctedPositionIndex = positionindex > 0 ? positionindex : positionindex + playersCnt;
        return correctedPositions[correctedPositionIndex];
    }

    componentWillReceiveProps(nextProps) {
        if(nextProps.update === true && nextProps.round) {
            this.handleTableUpdate(nextProps.round);
        }
    }

    takeAmount(stack, bet) {
        return stack > bet ? bet : stack;
    }

    takeBlinds(round) {
        return new Promise((resolve, reject) => {
            const table = {...this.state.table};
            let pot = this.state.pot;
            table.players.forEach(player => {
                if (round.ante) {
                    const ante = this.takeAmount(player.stack, round.ante);
                    player.stack -= ante;
                    pot += ante;
                }
                if (player.position === 'SB') {
                    const SB = this.takeAmount(player.stack, round.SB);
                    player.stack -= SB;
                    pot += SB;
                }
                if (player.position === 'BB') {
                    const BB = this.takeAmount(player.stack, round.BB);
                    player.stack -= BB;
                    pot += BB;
                }
            });
            this.setState({table, pot}, () => {resolve()});
        })
    }

    takeCardFromDeck() {
        return new Promise((resolve, reject) => {
            const deck = [...this.state.deck];
            const cardNo = Math.floor(Math.random() * this.state.deck.length);
            const card = deck[cardNo];
            deck.splice(cardNo, 1);
            this.setState({deck}, () => {resolve(card)})
        });
    }

    giveCards() {
        return new Promise((resolve, reject) => {
            const table = {...this.state.table};

            const cardSuits = ['s', 'c', 'h', 'd']
            const cardValues = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
            const deck = [];
            const board = [];

            function takeCardFromDeck() {
                const cardNo = Math.floor(Math.random() * deck.length);
                const card = deck[cardNo];
                deck.splice(cardNo, 1);
                return card;
            }

            // create deck
            cardSuits.forEach(suit => {
                cardValues.forEach(cardValue => {
                    deck.push([cardValue, suit])
                });
            });

            // add cards to players
            table.players.forEach(player => {
                player.hand = [];
                for(let i =0; i<2; i++) {
                    player.hand.push(takeCardFromDeck());
                }
            });

            //add cards to deck
            for(let i =0; i<5; i++) {
                board.push(takeCardFromDeck());
            }
            this.setState({deck, table, board}, () => {resolve})
        });
    }

    playerTurn() {
        const { table, activePosition } = this.state;
        const { players } = this.state.table;
        const positionTurnsMap = {
            '9': ['UTG', 'UTG+1', 'UTG+2', 'MP1', 'MP2', 'C', 'B', 'SB', 'BB'], 
            '8': ['UTG+1', 'UTG+2', 'MP1', 'MP2', 'C', 'B', 'SB', 'BB'], 
            '7': ['UTG+2', 'MP1', 'MP2', 'C', 'B', 'SB', 'BB'], 
            '6': ['MP1', 'MP2', 'C', 'B', 'SB', 'BB'], 
            '5': ['MP2', 'C', 'B', 'SB', 'BB'], 
            '4': ['C', 'B', 'SB', 'BB'], 
            '3': ['B', 'SB', 'BB'], 
            '2': ['SB', 'BB']
        }
        const positionTurns = positionTurnsMap[players.length.toString()];
        const activePlayer = players.find(player => player.position === positionTurns[activePosition]);
        activePlayer.timeToAct = true;
    }

    updatePlayer(player) {

    }

    async handleTableUpdate(round) {
        await this.takeBlinds(round);
        await this.giveCards();
        this.playerTurn();
        this.props.updateTable(this.state.table);
    }

    render() {
        const { players } = this.state.table;
        const { table, pot, board } = this.state;
        return (
            <div className="table">
                <p>POT: {pot}, BOARD: {board.reduce((prev, cur) => prev + ' ' + cur[0] + cur[1], '')}</p>
                {players.map((player, index) => (
                    <Player key={`player-${index}`} player={player} updatePlayer={this.updatePlayer.bind(this)}/>
                ))}
            </div>
        );
    } 
};

export default Table;