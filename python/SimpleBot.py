    constructor(aggression) {
        this.aggression = aggression || 1;
        const charts = [chart0, chart1, chart2, chart3, chart4, chart5, chart6];
        this.charts = [charts[0], charts[aggression || 1]];
    }
    def getSimpleHand(card1, card2, suitNr)
        suits = ['o', 's']
        suit = 'p' if card1 == card2 else suits[suitNr]
        return [card1, card2, suit]

    def update(data) {
        const positionsMap = [null, 'UTG', 'UTG+1', 'UTG+2', 'MP1', 'MP2', 'C', 'B', 'SB', 'BB'];
        const firstBetPositionName = positionsMap[data[0]];
        const position = positionsMap[data[1]];
        const stackBBs = data[2];
        const card1 = data[3];
        const card2 = data[4];
        const suit = data[5];
        let chartNr = 0;
        const firstIn = !firstBetPositionName;
        let BBCount = Math.floor(stackBBs);
        const hand = this.getSimpleHand(card1, card2, suit);
        // if stack is less than 1 BB
        if (BBCount === 0) {
            resolve(1);
        }
        if (BBCount > 15) {
            BBCount = 15;
        }
        if(!firstIn) {
            chartNr = 1;
        }

        if(chartNr == 0){
            if(position == 'BB') {
                resolve(1);
            }
            const actionData = this.charts[chartNr][position][BBCount];
            const hands = actionData[hand[2]];
            if (hand[2] == 'p') {
                if (hands[1] === '+') {
                    if (hand[0] >= hands[0]) {
                        resolve(1)
                    }
                }
                resolve(Math.round(Math.random() * 10) <= this.aggression ? 1 : 0);
            } else {
                for (let i = 0; i < actionData['o']['++'].length; i++) {
                    const cards = actionData['o']['++'][i];
                    if(hand[0] >= cards[0] && hand[1] >= cards[1]){
                        resolve(1)
                    } 
                }
                for (let i = 0; i < actionData['o']['+'].length; i++) {
                    const cards = actionData['o']['+'][i];
                    if(hand[0] == cards[0] && hand[1] >= cards[1]){
                        resolve(1)
                    } 
                }
                for (let i = 0; i < actionData['o']['='].length; i++) {
                    const cards = actionData['o']['='][i];
                    if(hand[0] == cards[0] && hand[1] == cards[1]){
                        resolve(1)
                    }   
                }
                if(hand[2] == 's'){
                    for (let i = 0; i < actionData['s']['++'].length; i++) {
                        const cards = actionData['s']['++'][i];
                        if(hand[0] >= cards[0] && hand[1] >= cards[1]){
                            resolve(1)
                        } 
                    }
                    for (let i = 0; i < actionData['s']['+'].length; i++) {
                        const cards = actionData['s']['+'][i];
                        if(hand[0] == cards[0] && hand[1] >= cards[1]){
                            resolve(1)
                        } 
                    }
                    for (let i = 0; i < actionData['s']['='].length; i++) {
                        const cards = actionData['s']['='][i];
                        if(hand[0] == cards[0] && hand[1] == cards[1]){
                            resolve(1)
                        }   
                    }
                }
            }
            resolve(Math.round(Math.random() * 10) <= this.aggression ? 1 : 0);
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
                            resolve(1)
                        }
                    }
                }
            }
            resolve(0);
        }
    }

    def giveAdvice(self):
        global tableData
        charts = [fileSystem.readJson(fileSystem.chart0), fileSystem.readJson(fileSystem.chart1)];
        chartNr = 0;
        anteCof = 0;
        first = self.checkFirstIn();
        BBCount = self.countBB()
        self.turnData['bbs'] = BBCount
        self.turnData['first'] = first
        if BBCount == 0:
            return 'push'
        
        if(BBCount > 15):
            tableData += 'too many BBs/'
            return 'fold/'
        hand = self.getSimpleHand()
        self.turnData['hand'] = str(hand[0])+str(hand[1])+str(hand[2])
        position = self.players[0]['position']
        if(first):
            chartNr = 0 
        else:
            chartNr = 1
        if(chartNr == 0):
            if(position == 'BB'):
                return 'push'
            actionData = charts[chartNr][position][str(BBCount)]
            hands = actionData[hand[2]]
            percent = ''
            if(actionData['%']):
                percent = str(actionData['%']) + ' %'
            else:
                percent = 'no chart available'
            
            if(hand[2] == 'p'):
                if(hands[1] == '+'):
                    if(hand[0] >= hands[0]):
                        return 'push/percent: '+percent
                return 'fold'
            else:
                for cards in actionData['o']['++']:
                    if(hand[0] >= cards[0] and hand[1] >= cards[1]):
                        return 'push/percent: '+percent
                for cards in actionData['o']['+']:
                    if(hand[0] == cards[0] and hand[1] >= cards[1]):
                        return 'push/percent: '+percent
                for cards in actionData['o']['=']:
                    if(hand[0] == cards[0] and hand[1] == cards[1]):
                        return 'push/percent: '+percent
                if(hand[2] == 's'):
                    for cards in actionData['s']['++']:
                        if(hand[0] >= cards[0] and hand[1] >= cards[1]):
                            return 'push/percent: '+percent
                    for cards in actionData['s']['+']:
                        if(hand[0] == cards[0] and hand[1] >= cards[1]):
                            return 'push/percent: '+percent
                    for cards in actionData['s']['=']:
                        if(hand[0] == cards[0] and hand[1] == cards[1]):
                            return 'push/percent: '+percent
            return 'fold'
        elif chartNr == 1:
            firstBet = False
            if self.firstBet == 'UTG' or self.firstBet == 'UTG+1' or self.firstBet == 'UTG+2':
                firstBet = 'E'
            elif self.firstBet == 'MP1' or self.firstBet == 'MP2':
                firstBet = 'M'
            elif self.firstBet == 'C':
                firstBet = 'C'
            elif self.firstBet == 'B':
                firstBet = 'B'
            else:
                firstBet = 'SB'
            self.turnData['firstbet'] = firstBet
            actionData = charts[chartNr][position][firstBet]           
            if str(hand[0]) in actionData:
                if str(hand[1]) in actionData[str(hand[0])]:
                    if str(hand[2]) in actionData[str(hand[0])][str(hand[1])]:
                        maxBbs = actionData[str(hand[0])][str(hand[1])][str(hand[2])]
                        if BBCount <= maxBbs:
                            return 'push'
            return 'fold'