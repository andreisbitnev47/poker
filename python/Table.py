import eval7

class Table():
    def __init__(self, props):
        sbPlayer = 0
        for index, player in enumerate(props["players"]):
            player.updateTableData("position", self.givePosition(index, sbPlayer, len(props["players"])))
            player.updateTableData("playersCnt", len(props["players"]))
        self.players = props["players"]
        self.sbPlayer = sbPlayer
        self.activePosition = 0
        self.firstBetPosition = False
        self.pot = [0] * len(props["players"])
        self.deck = []
        self.board = []
        self.winners = []
    
    def givePosition(self, playerIndex, sbPlayer, playersCnt):
        positionsCorrectionObj = {
            "9": ["SB", "BB", "UTG", "UTG+1", "UTG+2", "MP1", "MP2", "C", "B"], 
            "8": ["SB", "BB", "UTG+1", "UTG+2", "MP1", "MP2", "C", "B"], 
            "7": ["SB", "BB", "UTG+2", "MP1", "MP2", "C", "B"], 
            "6": ["SB", "BB", "MP1", "MP2", "C", "B"], 
            "5": ["SB", "BB", "MP2", "C", "B"], 
            "4": ["SB", "BB", "C", "B"], 
            "3": ["SB", "BB", "B"], 
            "2": ["SB", "BB"]
        }
        correctedPositions = positionsCorrectionObj[str(playersCnt)]
        if playerIndex == sbPlayer:
            return "SB"
        positionindex = playerIndex - sbPlayer
        correctedPositionIndex = positionindex if positionindex > 0 else positionindex + playersCnt
        return correctedPositions[correctedPositionIndex]
    
    def handleTableUpdate(self):
        self.takeBlinds()
        self.giveCards()
        self.playerTurn()
    
    def takeAmount(self, stack, bet):
         return bet if stack > bet else stack
     
    def takeBlinds(self):
        for index, player in enumerate(self.players):
            roundData = player.getTableData("round")
            if roundData["ante"]:
                ante = self.takeAmount(player.getData("stack"), roundData["ante"])
                player.updateStack(-ante)
                self.pot[index] += ante
            if player.getTableData("position") == "SB":
                SB = self.takeAmount(player.getData("stack"), roundData["SB"])
                player.updateStack(-SB)
                self.pot[index] += SB
            if player.getTableData("position") == "BB":
                BB = self.takeAmount(player.getData("stack"), roundData["BB"])
                player.updateStack(-BB)
                self.pot[index] += BB
                
    def giveCards(self):
        self.deck = eval7.Deck()
        self.deck.shuffle()
        self.board = self.deck.deal(5)
        
        #give cards to players
        for player in self.players:
            player.updateTableData("hand", self.deck.deal(2))
    
    def resetTableData(self):
        if len(self.players) <= 1:
            return
        self.sbPlayer = self.sbPlayer + 1 if self.sbPlayer < len(self.players) else 0
        self.pot = [0] * len(self.players)
        self.firstBetPosition = False
        for index, player in enumerate(self.players):
            player.updateTableData("position", self.givePosition(index, self.sbPlayer, len(self.players)))
            player.updateTableData("playersCnt", len(self.players))
            player.updateTableData("pot", self.pot)
            player.updateTableData("firstBetPosition", self.firstBetPosition)
            player.updateTableData("round", False)
    
    def playerTurn(self):
        positionTurnsMap = {
            "9": ["UTG", "UTG+1", "UTG+2", "MP1", "MP2", "C", "B", "SB", "BB"], 
            "8": ["UTG+1", "UTG+2", "MP1", "MP2", "C", "B", "SB", "BB"], 
            "7": ["UTG+2", "MP1", "MP2", "C", "B", "SB", "BB"], 
            "6": ["MP1", "MP2", "C", "B", "SB", "BB"], 
            "5": ["MP2", "C", "B", "SB", "BB"], 
            "4": ["C", "B", "SB", "BB"], 
            "3": ["B", "SB", "BB"], 
            "2": ["SB", "BB"]
        }
        positionTurns = positionTurnsMap[str(len(self.players))]
        activePlayerIndex = False
        for index, player in enumerate(self.players):
            if player.getTableData("position") == positionTurns[self.activePosition]:
                activePlayerIndex = index
                break
        
        activePlayer = self.players[activePlayerIndex]
        firstBetPositionName = positionTurnsMap[str(len(self.players))][self.firstBetPosition] if self.firstBetPosition != False else False
        activePlayer.updateTableData("firstBetPositionName", firstBetPositionName)
        betAmount = activePlayer.update()
        if betAmount != 0 and not self.firstBetPosition:
            self.firstBetPosition = self.activePosition
        activePlayer.updateStack(-betAmount)
        activePlayer.updateData("inGame", True if betAmount > 0 else False)
        #if player is BB, and everyone folded || BB is bigger than any other bet
        firstIn = self.firstBetPosition == False
        if (firstIn == True and betAmount == 0 and self.activePosition == len(self.players) - 1) or (firstIn == True and betAmount == 0 and not [x for x in self.pot if x > self.pot[activePlayerIndex]]):
            activePlayer.updateData("inGame", True)
        self.pot[activePlayerIndex] += betAmount
        self.activePosition += 1
        if self.activePosition >= len(self.players):
            self.activePosition = 0
            self.distributePot()
        else:
            self.playerTurn()
            
    def getPlayers(self):
        return self.players
    
    def updatePlayers(self, players):
        self.players = players
    
    def distributePot(self):
        hands = []
        for index, player in enumerate(self.players):
            if player.getData("inGame"):
                score = eval7.evaluate(self.board + player.getTableData("hand"))
                hand = {"index": index, "score": score}
                hands.append(hand)
                
        places = []
        minScore = 0
        def useScore(hand):
            return hand["score"]
        
        # sort hands by score
        hands.sort(key=useScore, reverse=True)
        
        # add players to places
        for hand in hands:
            if hand["score"] != minScore:
                places.append([hand["index"]])
            else:
                places[len(places) - 1].append(hand["index"])

        for place in places:
            def usePot(playerIndex):
                return self.pot[playerIndex]
            place.sort(key=usePot, reverse=True)
            for i, playerPot in enumerate(self.pot):
                # give back pot to winnerPlayer
                if i in place:
                    self.players[i].updateStack(self.pot[i])
                else:
                    potPieces = len(place)
                    for winnerIndex in place:
                        # if potPiece is bigger than player bet, potPiece = player bet
                        piece = self.pot[i] / potPieces if self.pot[i] / potPieces < self.pot[winnerIndex] else self.pot[winnerIndex]
                        self.players[winnerIndex].updateStack(piece)
                        self.pot[i] -= piece
                        potPieces -= 1
            # set winnerPlayers potPieces to 0
            for winnerIndex in place:
                self.pot[winnerIndex] = 0
        # if some potPieces are not 0, return them
        for index, potPiece in enumerate(self.pot):
            if potPiece > 0:
                self.players[index].updateStack(potPiece)