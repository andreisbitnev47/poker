import React, { Component } from 'react';
import './Table.css';
import Player from '../Player';
const Hand = require('pokersolver').Hand;

class Table extends Component {
    constructor(props) {
        super(props);
        const sbPlayer = 0;
        const players = [...props.players];
        players.forEach((player, index) => {
            player.tableData.position = this.givePosition(index, sbPlayer, props.players.length);
            player.tableData.round = props.round;
            player.tableData.playersCnt = props.playersCnt;
        });
        props.updatePlayers(players);
        this.state = {
            sbPlayer,
            update: props.update,
            activePosition: 0,
            firstBetPosition: undefined,
            pot: Array(players.length).fill(0),
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
            const {tableNr, updateTable} = this.props;
            const updating = true;
            updateTable(tableNr, updating);
            this.handleTableUpdate(nextProps.round);
        }
    }

    takeAmount(stack, bet) {
        return stack > bet ? bet : stack;
    }

    takeBlinds(round) {
        return new Promise((resolve, reject) => {
            const players = [...this.props.players];
            const pot = [...this.state.pot];
            players.forEach((player, index) => {
                if (round.ante) {
                    const ante = this.takeAmount(player.stack, round.ante);
                    player.stack -= ante;
                    pot[index] += ante;
                }
                if (player.tableData.position === 'SB') {
                    const SB = this.takeAmount(player.stack, round.SB);
                    player.stack -= SB;
                    pot[index] += SB;
                }
                if (player.tableData.position === 'BB') {
                    const BB = this.takeAmount(player.stack, round.BB);
                    player.stack -= BB;
                    pot[index] += BB;;
                }
            });
            this.props.updatePlayers(players);
            this.setState({pot}, () => {
                resolve()
            });
        })
    }

    giveCards() {
        return new Promise((resolve, reject) => {
            const players = [...this.props.players];

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
            players.forEach(player => {
                player.tableData.hand = [];
                for(let i =0; i<2; i++) {
                    player.tableData.hand.push(takeCardFromDeck());
                }
            });

            //add cards to deck
            for(let i =0; i<5; i++) {
                board.push(takeCardFromDeck());
            }
            this.props.updatePlayers(players);
            this.setState({deck, board}, () => {resolve()})
        });
    }

    playerTurn() {
        const players = [...this.props.players]
        const {firstBetPosition, pot, activePosition} = this.state;
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
        const activePlayer = players.find(player => player.tableData.position === positionTurns[activePosition]);
        activePlayer.timeToAct = true;
        activePlayer.tableData.firstBetPosition = firstBetPosition;
        activePlayer.tableData.pot = pot;
        this.props.updatePlayers(players);
    }

    distributePot() {
        const players = [...this.props.players];
        let hands = []; 
        let handNames = [];
        const board = [...this.state.board];
        const pot = [...this.state.pot];
        function translateCard(card){
            const mapCards = {'10': 'T', '11': 'J', '12': 'Q', '13': 'K', '14': 'A'};
            return parseInt(card[0]) > 9 ? mapCards[card[0]] + card[1] : card[0] + card[1];
        }
        players.forEach((player, index) => {
            if(player.inGame) {
                const hand = Hand.solve([...player.tableData.hand, ...this.state.board].map(card => translateCard(card)));
                hand.index = index;
                hands.push(hand);
            }
        });
        const places = [];
        while (hands.length) {
            places.push(Hand.winners(hands).map(winner => winner.index));
            handNames.push(Hand.winners(hands).map(winner => winner.descr));
            places[places.length - 1].forEach(place => {
                hands = hands.filter(hand => hand.index != place);
            });
        }
        places.forEach((place) => {
            let betAmounts = [];
            let winnerPlayers = [];
            place.forEach((playerIndex) => {
                betAmounts.push(pot[playerIndex]);
                winnerPlayers.push(players[playerIndex]);
            });
            for(let i = 0; i < pot.length; i++) {
                let potPieces = winnerPlayers.length;
                winnerPlayers.forEach((winner, index) => {
                    const piece = pot[i] / potPieces < betAmounts[index] ? pot[i] / potPieces : betAmounts[index];
                    winner.stack += piece;
                    pot[i] -= piece;
                    potPieces -= 1;
                });
            }
        });
        this.props.updatePlayers(players);
    }

    setNextPlayer(betAmount, playerIndex) {
        let {firstBetPosition, pot, activePosition} = this.state;
        const {tableNr, updateTable, updatePlayers} = this.props;
        const players = [...this.props.players];
        if (betAmount && !firstBetPosition) {
            firstBetPosition = activePosition;
        }
        players[playerIndex]['stack'] -= betAmount;
        players[playerIndex]['timeToAct'] = false;
        players[playerIndex]['inGame'] = !!betAmount;
        updatePlayers(players);
        pot[playerIndex] += betAmount;
        activePosition += 1;
        
        if (activePosition >= players.length) {
            activePosition = 0
            this.setState({firstBetPosition, pot, activePosition}, () => {
                this.distributePot();
                updateTable(tableNr, false);
            })
        } else {
            this.setState({firstBetPosition, pot, activePosition}, () => {
                this.playerTurn();
            })
        }
        
    }

    // resetTableData() {
    //     this.setState({
    //         sbPlayer,
    //         update: props.update,
    //         activePosition: 0,
    //         firstBetPosition: undefined,
    //         pot: Array(players.length).fill(0),
    //         deck: [],
    //         board: []
    //     })
    // }

    async handleTableUpdate(round) {
        const players = [...this.props.players];
        const { sbPlayer } = this.state;
        players.forEach((player, index) => {
            player.tableData.position = this.givePosition(index, sbPlayer, players.length);
            player.tableData.round = this.props.round;
            player.tableData.playersCnt = players.length;
        });
        this.props.updatePlayers(players);
        await this.takeBlinds(round);
        await this.giveCards();
        this.playerTurn();
    }

    render() {
        const { players } = this.props;
        const { pot, board } = this.state;
        return (
            <div className="table">
                <p>POT: {pot.reduce((prev, cur) => prev+cur)}, BOARD: {board.reduce((prev, cur) => prev + ' ' + cur[0] + cur[1], '')}</p>
                {players.map((player, index) => (
                    <Player 
                        key={`player-${index}`} 
                        player={player}
                        index={index} 
                        setNextPlayer={this.setNextPlayer.bind(this)}
                    />
                ))}
            </div>
        );
    } 
};

export default Table;