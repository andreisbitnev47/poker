import math as math
from random import randint
from chart0 import chart0
from chart1 import chart1
from chart2 import chart2
from chart3 import chart3
from chart4 import chart4
from chart5 import chart5
from chart6 import chart6

class SimpleBot():    
    def __init__(self, aggression):
        self.aggression = aggression
        charts = [chart0, chart1, chart2, chart3, chart4, chart5, chart6]
        self.charts = [charts[0], charts[aggression]]
        
    def getSimpleHand(self, card1, card2, suitNr):
        suits = ['o', 's']
        suit = 'p' if card1 == card2 else suits[suitNr]
        return [card1, card2, suit]

    def update(self, reward, data):
        positionsMap = [False, 'UTG', 'UTG+1', 'UTG+2', 'MP1', 'MP2', 'C', 'B', 'SB', 'BB']
        firstBetPositionName = positionsMap[data[0]]
        position = positionsMap[data[1]]
        stackBBs = data[2]
        card1 = data[3]
        card2 = data[4]
        suit = data[5]
        chartNr = 0
        firstIn = not firstBetPositionName
        BBCount = math.floor(stackBBs)
        hand = self.getSimpleHand(card1, card2, suit)
        # if stack is less than 1 BB
        if BBCount == 0:
            return 1
        if BBCount > 15:
            BBCount = 15
        if not firstIn:
            chartNr = 1

        if chartNr == 0:
            if position == 'BB':
                return 1
            actionData = self.charts[chartNr][position][str(BBCount)]
            hands = actionData[hand[2]]
            if hand[2] == 'p':
                if hands[1] == '+':
                    if hand[0] >= hands[0]:
                        return 1
                return 1 if randint(0, 10) <= self.aggression else 0
            else:
                for cards in actionData['o']['++']:
                    if(hand[0] >= cards[0] and hand[1] >= cards[1]):
                        return 1
                for cards in actionData['o']['+']:
                    if(hand[0] == cards[0] and hand[1] >= cards[1]):
                        return 1
                for cards in actionData['o']['=']:
                    if(hand[0] == cards[0] and hand[1] == cards[1]):
                        return 1
                if(hand[2] == 's'):
                    for cards in actionData['s']['++']:
                        if(hand[0] >= cards[0] and hand[1] >= cards[1]):
                            return 1
                    for cards in actionData['s']['+']:
                        if(hand[0] == cards[0] and hand[1] >= cards[1]):
                            return 1
                    for cards in actionData['s']['=']:
                        if(hand[0] == cards[0] and hand[1] == cards[1]):
                            return 1
            return 1 if randint(0, 10) <= self.aggression else 0
        
        elif chartNr == 1:
            positionsMap = {
                'UTG': 'E', 'UTG+1': 'E', 'UTG+2': 'E',
                'MP1': 'M', 'MP2': 'M',
                'C': 'C',
                'B': 'B',
                'SB': 'SB'
            }
            firstBet = positionsMap[firstBetPositionName] or 'SB'

            actionData = self.charts[chartNr][position][firstBet]           
            if str(hand[0]) in actionData:
                if str(hand[1]) in actionData[str(hand[0])]:
                    if str(hand[2]) in actionData[str(hand[0])][str(hand[1])]:
                        maxBbs = actionData[str(hand[0])][str(hand[1])][str(hand[2])]
                        if BBCount <= maxBbs:
                            return 1
            return 0