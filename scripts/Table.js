const Player = require('./Player');
const Hand = require('pokersolver').Hand;

class Table {
    constructor(props) {
        const sbPlayer = 0;
        const players = props.players;
        players.forEach((player, index) => {
            player.tableData.position = this.givePosition(index, sbPlayer, props.players.length);
            player.tableData.playersCnt = props.players.length;
        });
        this.players = players;
        this.sbPlayer = sbPlayer;
        this.activePosition = 0;
        this.firstBetPosition = undefined;
        this.pot = Array(players.length).fill(0);
        this.deck = [];
        this.board = [];
        this.winners = [];
        this.history = [];
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

    handleTableUpdate() {
        return new Promise((resolve, reject) => {
            this.takeBlinds();
            this.giveCards();
            resolve(this.playerTurn());
        });
    }

    takeAmount(stack, bet) {
        return stack > bet ? bet : stack;
    }

    takeBlinds() {
        const players = this.players;
        const pot = this.pot;
        players.forEach((player, index) => {
            const round = player.tableData.round;
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
    }

    giveCards() {
        const players = this.players

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
        this.deck = deck;
        this.board = board;
    }

    resetTableData() {
        const players = this.players;
        if(players.length <= 1) {
            return
        }
        this.sbPlayer = this.sbPlayer < players.length ? this.sbPlayer + 1 : 0;
        this.pot = Array(players.length).fill(0);
        this.firstBetPosition = undefined;
        players.forEach((player, index) => {
            player.updateTableData({
                position: this.givePosition(index, this.sbPlayer, players.length),
                playersCnt: players.length,
                pot: this.pot,
                firstBetPosition: this.firstBetPosition,
                round: undefined,
            })
        });
    }

    playerTurn() {
        return new Promise((resolve, reject) => {
            const players = this.players
            let {firstBetPosition, pot} = this;
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
            const activePlayerIndex = players.findIndex(player => player.tableData.position === positionTurns[this.activePosition]);
            const activePlayer = players[activePlayerIndex];
            const firstBetPositionName = positionTurnsMap[players.length.toString()][firstBetPosition];
            
            if(!activePlayer) {
                console.log('asd');
            }
            activePlayer.updateTableData({
                firstBetPositionName
            });
            activePlayer.update().then((betAmount) => {
                if (betAmount && !this.firstBetPosition) {
                    this.firstBetPosition = this.activePosition;
                }
                activePlayer.set('stack', activePlayer.stack - betAmount);
                activePlayer.set('inGame', !!betAmount);
                // if player is BB, and everyone folded || BB is bigger than any other bet
                const firstIn = this.firstBetPosition == undefined;
                if ((firstIn && !betAmount && this.activePosition === players.length - 1) || 
                    (!firstIn && !betAmount && !this.pot.find(playerBetAmount => playerBetAmount > this.pot[activePlayerIndex])) ) {
                        activePlayer.set('inGame', true);
                }
                pot[activePlayerIndex] += betAmount;
                this.activePosition += 1;
                if (this.activePosition >= players.length) {
                    this.activePosition = 0
                    this.distributePot();
                    resolve();
                } else {
                    resolve(this.playerTurn());
                }
            });
        });
    }

    distributePot() {
        const players = this.players;
        let hands = []; 
        let handNames = [];
        const board = this.board
        const pot = this.pot
        function translateCard(card){
            const mapCards = {'10': 'T', '11': 'J', '12': 'Q', '13': 'K', '14': 'A'};
            return parseInt(card[0]) > 9 ? mapCards[card[0]] + card[1] : card[0] + card[1];
        }
        players.forEach((player, index) => {
            if(player.inGame) {
                const hand = Hand.solve([...player.tableData.hand, ...board].map(card => translateCard(card)));
                hand.index = index;
                hands.push(hand);
            }
        });
        const places = [];
        const winners = Hand.winners(hands);
        const currentHand = {
            playersStart: [...this.players].map(player => player.name + ' - ' + player.stack),
            firstBetPosition: this.firstBetPosition,
            pot: [...this.pot],
            board,
            hands,
            winners,
        }
        while (hands.length) {
            places.push(Hand.winners(hands).map(winner => winner.index));
            handNames.push(Hand.winners(hands).map(winner => winner.descr));
            places[places.length - 1].forEach(place => {
                hands = hands.filter(hand => hand.index != place);
            });
        }
        places.forEach((place) => {
            place.sort((a, b) => pot[a] - pot[b]);
            for(let i = 0; i < pot.length; i++) {
                // give back pot to winnerPlayer
                if(place.includes(i)) {
                    players[i].stack += pot[i]
                } else {
                    let potPieces = place.length;
                    place.forEach((winnerIndex) => {
                        // if potPiece is bigger than player bet, potPiece = player bet
                        const piece = pot[i] / potPieces < pot[winnerIndex] ? pot[i] / potPieces : pot[winnerIndex];
                        players[winnerIndex].stack += piece;
                        pot[i] -= piece;
                        potPieces -= 1;
                    });
                }
            }
            // set winnerPlayers potPieces to 0
            place.forEach((winnerIndex) => {pot[winnerIndex] = 0});
        });
        // if some potPieces are not 0, return them
        pot.forEach((potPiece, index) => {
            if(potPiece > 0) {
                players[index] += potPiece;
            }
        });
        currentHand.playersEnd = [...players].map(player => player.name + ' - ' + player.stack);
    }
};

module.exports = Table;