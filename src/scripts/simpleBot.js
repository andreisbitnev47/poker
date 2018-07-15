import chart0 from './chart0';
import chart1 from './chart1';
import chart2 from './chart2';
import chart3 from './chart3';
import chart4 from './chart4';
import chart5 from './chart5';
import chart6 from './chart6';

// playerCnt, firstBetPosition, card1, card2, suit(1 - s, 0 - o), stackBBs, position

export default class SimpleBot{
    constructor(aggression) {
        this.aggression = aggression || 1;
        const charts = [chart0, chart1, chart2, chart3, chart4, chart5, chart6];
        this.charts = [charts[0], charts[aggression || 1]];
    }
    getSimpleHand(card1, card2, suitNr){
        const suits = ['o', 's'];
        const suit = card1 === card2 ? 'p' : suits[suitNr];
        return [card1, card2, suit];
    }
    update(reward, data) {
        const positionsMap = [null, 'UTG', 'UTG+1', 'UTG+2', 'MP1', 'MP2', 'C', 'B', 'SB', 'BB'];
        const firstBetPositionName = positionsMap[data[0]];
        const position = positionsMap[data[1]];
        const stackBBs = data[2];
        const card1 = data[3];
        const card2 = data[4];
        const suit = data[5]
        let chartNr = 0;
        const firstIn = !firstBetPositionName;
        let BBCount = Math.floor(stackBBs);
        const hand = this.getSimpleHand(card1, card2, suit);
        // if stack is less than 1 BB
        if (BBCount === 0) {
            return 1;
        }
        if (BBCount > 15) {
            BBCount = 15;
        }
        if(!firstIn) {
            chartNr = 1;
        }

        if(chartNr == 0){
            if(position == 'BB') {
                return 1;
            }
            const actionData = this.charts[chartNr][position][BBCount];
            const hands = actionData[hand[2]];
            if (hand[2] == 'p') {
                if (hands[1] === '+') {
                    if (hand[0] >= hands[0]) {
                        return 1
                    }
                }
                return Math.round(Math.random() * 10) <= this.aggression ? 1 : 0;
            } else {
                for (let i = 0; i < actionData['o']['++'].length; i++) {
                    const cards = actionData['o']['++'][i];
                    if(hand[0] >= cards[0] && hand[1] >= cards[1]){
                        return 1
                    } 
                }
                for (let i = 0; i < actionData['o']['+'].length; i++) {
                    const cards = actionData['o']['+'][i];
                    if(hand[0] == cards[0] && hand[1] >= cards[1]){
                        return 1
                    } 
                }
                for (let i = 0; i < actionData['o']['='].length; i++) {
                    const cards = actionData['o']['='][i];
                    if(hand[0] == cards[0] && hand[1] == cards[1]){
                        return 1
                    }   
                }
                if(hand[2] == 's'){
                    for (let i = 0; i < actionData['s']['++'].length; i++) {
                        const cards = actionData['s']['++'][i];
                        if(hand[0] >= cards[0] && hand[1] >= cards[1]){
                            return 1
                        } 
                    }
                    for (let i = 0; i < actionData['s']['+'].length; i++) {
                        const cards = actionData['s']['+'][i];
                        if(hand[0] == cards[0] && hand[1] >= cards[1]){
                            return 1
                        } 
                    }
                    for (let i = 0; i < actionData['s']['='].length; i++) {
                        const cards = actionData['s']['='][i];
                        if(hand[0] == cards[0] && hand[1] == cards[1]){
                            return 1
                        }   
                    }
                }
            }
            return Math.round(Math.random() * 10) <= this.aggression ? 1 : 0;
        } else if (chartNr === 1) {
            const positionsMap = {
                'UTG': 'E', 'UTG+1': 'E', 'UTG+2': 'E',
                'MP1': 'M', 'MP2': 'M',
                'C': 'C',
                'B': 'B',
                'SB': 'SB'
            }
            const firstBet = positionsMap[firstBetPositionName] || 'SB';
            const actionData = this.charts[chartNr][position][firstBet];
            if (actionData[hand[0]]) {
                if (actionData[hand[0]][hand[1]]) {
                    if (actionData[hand[0]][hand[1]][hand[2]]) {
                        const maxBbs = actionData[hand[0]][hand[1]][hand[2]];
                        if (BBCount <= maxBbs) {
                            return 1
                        }
                    }
                }
            }
            return 0;
        }
    }
}