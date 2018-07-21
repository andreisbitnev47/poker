const SimpleBot = require('./simpleBot');
const Dqn = require('./dqn'); 
module.exports = class Player {
    constructor(props) {
        this.id = props.id;
        this.index = props.index;
        this.name = props.name;
        this.stack = props.stack;
        this.tableData = props.tableData;
        this.bot = props.level ? new SimpleBot(props.level) : new Dqn();
        this.brain = props.brain;
    }
    set(propName, value) {
        this[propName] = value;
    }
    updateTableData(data) {
        this.tableData = {...this.tableData, ...data};
    }
    formatHand(hand){
        if(!hand) {
            return undefined;
        }
        const firstCard = hand[0][0] > hand[1][0] ? hand[0][0] : hand[1][0];
        const secondCard = hand[0][0] < hand[1][0] ? hand[0][0] : hand[1][0];
        const sop = hand[0][1] === hand[1][1] ? 1 : 0;
        return [firstCard, secondCard, sop];
    }
    update() {
        return new Promise((resolve, reject) => {
            const {hand, firstBetPositionName, round, position, playersCnt, pot, reward, tournamentPosition} = this.tableData;
            const { player, setNextPlayer, index } = this;
            // const action = Math.floor(Math.random() * 2);
            const formattedHand = this.formatHand(hand)
            const anteCoefficient = 0.67;
            const stackBBs = this.stack / (round.BB + round.ante * playersCnt * anteCoefficient);
            const positionsMap = [null, 'UTG', 'UTG+1', 'UTG+2', 'MP1', 'MP2', 'C', 'B', 'SB', 'BB'];
            const firstBetPosition = positionsMap.indexOf(firstBetPositionName);
            const playerPosition = positionsMap.indexOf(position);
            const data = [
                firstBetPosition === -1 ? 0 : firstBetPosition, // firstBetPosition
                playerPosition, // position
                stackBBs,
                formattedHand[0], // card1
                formattedHand[1], // card2
                formattedHand[2] // suit
            ];
            
            this.bot.update(reward, data).then((action) => {
                resolve(this.stack * action);
            });
        });
    }
}