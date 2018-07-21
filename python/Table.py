from Player import Player
import eval7
from pprint import pprint

class Table():
    def __init__(self, props):
        sbPlayer = 0
        for index, player in enumerate(props["players"]):
            player["tableData"]["position"] = self.givePosition(index, sbPlayer, len(props["players"]))
            player["tableData"]["playersCnt"] = len(props["players"]);
        self.players = props["players"];
        self.sbPlayer = sbPlayer
        self.activePosition = 0
        self.firstBetPosition = False
        self.pot = [0] * len(props["players"])
        self.deck = []
        self.board = []
        self.winners = []
    
    def givePosition(self, playerIndex, sbPlayer, playersCnt):
        positions = ["SB", "BB", "UTG", "UTG+1", "UTG+2", "MP1", "MP2", "C", "B"];
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
        correctedPositions = positionsCorrectionObj[str(playersCnt)];
        if playerIndex == sbPlayer:
            return "SB"
        positionindex = playerIndex - sbPlayer;
        correctedPositionIndex = positionindex if positionindex > 0 else positionindex + playersCnt;
        return correctedPositions[correctedPositionIndex];
    
    def handleTableUpdate(self):
        self.takeBlinds()
        self.giveCards()
        self.playerTurn()
    
    def takeAmount(self, stack, bet):
         return bet if stack > bet else stack
     
    def takeBlinds(self):
        for index, player in enumerate(self.players):
            roundData = player["tableData"]["round"]
            if roundData["ante"]:
                ante = self.takeAmount(player["stack"], roundData["ante"])
                player["stack"] -= ante
                self.pot[index] += ante
            if player["tableData"]["position"] == "SB":
                SB = self.takeAmount(player["stack"], roundData["SB"])
                player["stack"] -= SB
                self.pot[index] += SB
            if player["tableData"]["position"] == "BB":
                BB = self.takeAmount(player["stack"], roundData["BB"])
                player["stack"] -= BB
                self.pot[index] += BB
                
    def giveCards(self):
        self.deck = eval7.Deck()
        self.deck.shuffle()
        self.board = deck.deal(5)
        
        #give cards to players
        for player in self.players:
            player["tableData"]["hand"] = deck.deal(2)
    
    def resetTableData(self):
        if len(self.players) <= 1:
            return
        self.sbPlayer = self.sbPlayer + 1 if self.sbPlayer < len(self.players) else 0
        self.pot = [0] * len(self.players)
        self.firstBetPosition = False
        for index, player in enumerate(self.players):
            player["tableData"]["position"] = self.givePosition(index, self.sbPlayer, len(self.players))
            player["tableData"]["playersCnt"] = len(self.players)
            player["tableData"]["pot"] = self.pot
            player["tableData"]["firstBetPosition"] = self.firstBetPosition
            player["tableData"]["round"] = False
    
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
            if player["tableData"]["position"] == positionTurns[self.activePosition]:
                activePlayerIndex = index
                break
        
        activePlayer = self.players[activePlayerIndex];
        firstBetPositionName = positionTurnsMap[str(len(self.players))][self.firstBetPosition] if self.firstBetPosition != False else False
        activePlayer["tableData"]["firstBetPositionName"] = firstBetPositionName
        betAmount = activePlayer.update()
        if betAmount != 0 and not self.firstBetPosition:
            self.firstBetPosition = firstBetPosition
        activePlayer["stack"] -= betAmount
        activePlayer["inGame"] = True if betAmount > 0 else False
        #if player is BB, and everyone folded || BB is bigger than any other bet
        firstIn = self.firstBetPosition == False
        if (firstIn == True and betAmount == 0 and self.activePosition == self.players.length - 1) or (firstIn == True and betAmount == 0 and not [x for x in self.pot if x > self.pot[activePlayerIndex]]):
            activePlayer["inGame"] = True
        self.pot[activePlayerIndex] += betAmount
        self.activePosition += 1
        if self.activePosition >= len(self.players):
            self.activePosition = 0
            self.distributePot()
        else:
            self.playerTurn()
            
        
class Table {

    distributePot() {
        const players = this.players;
        let hands = []; 
        let handNames = [];
        const board = this.board
        const pot = this.pot
        function translateCard(card){
            const mapCards = {"10": "T", "11": "J", "12": "Q", "13": "K", "14": "A"};
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
            playersStart: [...this.players].map(player => player.name + " - " + player.stack),
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
        currentHand.playersEnd = [...players].map(player => player.name + " - " + player.stack);
    }
};

module.exports = Table;

import eval7
from pprint import pprint
deck = eval7.Deck()
deck.shuffle()
hand = deck.deal(7)
eval7.evaluate(hand)