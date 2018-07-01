import React, { Component } from 'react';

class Player extends Component {
    render() {
        const { hand, name, brain, stack, position } = this.props.player;

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
    
        function update() {
    
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