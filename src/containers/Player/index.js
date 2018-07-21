import React, { Component } from 'react';
import SimpleBot from '../../scripts/simpleBot';
import Dqn from '../../scripts/dqn';

class Player extends Component {
    constructor(props) {
        super(props);
        const level = props.player.level;
        const bot = level ? new SimpleBot(props.player.level) : new Dqn();
        this.state = {
            bot,
            id: props.player.id,
            timeToAct: props.timeToAct
        }
    }

    componentWillReceiveProps(nextProps) {
        if(nextProps.player && nextProps.player.timeToAct && nextProps.player.id === this.state.id && !this.state.timeToAct) {
            this.setState({timeToAct: nextProps.player.timeToAct}, () => {
                this.update(nextProps.player.tableData);
            });
        }
    }

    update({hand, firstBetPositionName, round, position, playersCnt, pot, reward, tournamentPosition}) {
        const { player, setNextPlayer, index } = this.props;
        // const action = Math.floor(Math.random() * 2);
        const formattedHand = this.formatHand(hand)
        const anteCoefficient = 0.67;
        const stackBBs = this.props.player.stack / (round.BB + round.ante * playersCnt * anteCoefficient);
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
        
        this.state.bot.update(reward, data).then((action) => {
            setNextPlayer(player.stack * action, index);
        });
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