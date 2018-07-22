class Player():
    def __init__(self, props):
        self.id = props.id
        self.index = props.index
        self.name = props.name
        self.stack = props.stack
        self.tableData = props.tableData
        self.bot = props.bot
        self.brain = props.brain
    
    def formatHand(self, hand):
        translatedHand = [self.translateCard(hand[0]), self.translateCard(hand[1])]
        firstCard = translatedHand[0][0] if translatedHand[0][0] > translatedHand[1][0] else translatedHand[1][0]
        secondCard = translatedHand[0][0] if translatedHand[0][0] < translatedHand[1][0] else translatedHand[1][0]
        sop = 1 if translatedHand[0][1] == translatedHand[1][1] else 0
        return [firstCard, secondCard, sop]
    
    def translateCard(card):
        mapCards = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
        cardList = list(str(card))
        return [mapCards[cardList[0]], cardList[1]]
    
    def update(self):        
        formattedHand = self.formatHand(self.tableData["hand"])
        anteCoefficient = 0.67
        stackBBs = self.stack / (self.tableData["round"]["BB"] + self.tableData["round"]["ante"] * self.tableData["playersCnt"] * anteCoefficient)
        positionsMap = [False, 'UTG', 'UTG+1', 'UTG+2', 'MP1', 'MP2', 'C', 'B', 'SB', 'BB']
        firstBetPosition = positionsMap.index(self.tableData["firstBetPositionName"])
        playerPosition = positionsMap.index(self.tableData["position"])
        data = [self.tableData["reward"],
                0 if firstBetPosition == -1 else firstBetPosition,
                playerPosition,
                stackBBs,
                formattedHand[0], #card1
                formattedHand[1], #card2
                formattedHand[2] #suit
                ]
        return self.bot.update(data)