import React, { Component } from 'react';
import SimpleBot from '../../scripts/simpleBot';

class Player extends Component {
    constructor(props) {
        super(props);
        const bot = new SimpleBot(props.player.level);
        this.state = {
            bot
        }
    }

    componentWillReceiveProps(nextProps) {
        if(nextProps.player && nextProps.player.timeToAct) {
            this.update(nextProps.player.tableData);
        }
    }

    update({hand, firstBetPosition, firstBetPositionName, round, position, playersCnt, pot}) {
        const { player, setNextPlayer, index } = this.props;
        // const action = Math.floor(Math.random() * 2);
        const formattedHand = this.formatHand(hand)
        const anteCoefficient = 0.67;
        const stackBBs = this.props.player.stack / (round.BB + round.ante * playersCnt * anteCoefficient);
        const action = this.state.bot.update(undefined, 
            {firstBetPositionName,
            position,
            stackBBs,
            card1: formattedHand[0], 
            card2: formattedHand[1], 
            suit: formattedHand[2]});
        setNextPlayer(player.stack * action, index);
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

    render() {
        const { name, brain, stack, timeToAct } = this.props.player;
        const { 
            hand,
            firstBetPosition,
            round,
            position,
            playersCnt,
            pot
        } = this.props.player.tableData;

        function translateCard(card){
            const mapCards = {'10': 'T', '11': 'J', '12': 'Q', '13': 'K', '14': 'A'};
            return parseInt(card) > 9 ? mapCards[card] : card;
        }
    
        function getSimpleHand(hand){
            if(!hand) {
                return undefined;
            }
            const firstCard = hand[0][0] > hand[1][0] ? hand[0][0] : hand[1][0];
            const secondCard = hand[0][0] < hand[1][0] ? hand[0][0] : hand[1][0];
            const sop = hand[0][0] === hand[1][0] ? 'p' : hand[0][1] === hand[1][1] ? 's' : 'o';
            return [firstCard, secondCard, sop];
        }
    
        function handForDisplay(simpleHand) {
            if(!simpleHand) {
                return undefined;
            }
            return simpleHand.map(card => translateCard(card)).reduce((acc, curVal) => acc + curVal.toString());
        }

        const simpleHand = getSimpleHand(hand);
    
        return (
            <div className="player">
                <p>{`${name} (${brain}) - ${handForDisplay(simpleHand)}`}</p>
                <p>{`$${stack}, pos - ${position}`}</p>
            </div>
        );
    }
};

export default Player;