from Player import Player
from Table import Table
from random import randint
from ai import Dqn
from SimpleBot import SimpleBot
import math as math

class Tournament():
    
    def __init__(self, playerCnt, playersPerTable, startingChips, maxGames):
        dqnNr = randint(1, playerCnt)
        players = []
        self.dqn = Dqn(5,3,0.9)
        for x in range(playerCnt):
            level = 0 if x == dqnNr else randint(1, 6)
            bot = self.dqn if level == 0 else SimpleBot(level)
            data = {"index": x,
                    "name": 'player-'+ x,
                    "stack": startingChips,
                    "bot": bot,
                    "tableData":{
                        "hand": False,
                        "firstBetPosition": False,
                        "firstBetPositionName": False,
                        "round": False,
                        "position": False,
                        "playersCnt": False,
                        "pot": False,
                        "reward": -0.5,
                        "tournamentPosition": False
                        }
                    }
            players.append(Player(data))
            
        tables = []
        for tableNr in range(playerCnt / playersPerTable):
            tablePlayers = []
            for playerNr in range(playersPerTable):
                tablePlayers.append(players[tableNr * playersPerTable + playerNr])
            data = {"tableNr": tableNr, "updating": False, "players": tablePlayers}
            tables.append(Table(data))
         
        self.maxGames = maxGames;
        self.gameCnt = 0;
        self.prizes = {
            '1': 0,
            '2': 0,
            '3': 0,
            '4': 0,
            '5': 0,
            '6': 0,
        }
        self.playerCnt = playerCnt;
        self.startingChips = startingChips;
        self.playersPerTable = playersPerTable;
        self.players = players;
        self.dqnNr = dqnNr;
        self.activePlayers = players;
        self.finishedPlayers = [];
        self.tables = tables;
        self.roundsMap = [
            {'BB': 50, 'SB': 25, 'ante': 10, 'games': 3},
            {'BB': 100, 'SB': 50, 'ante': 20, 'games': 4},
            {'BB': 200, 'SB': 100, 'ante': 40, 'games': 4},
            {'BB': 400, 'SB': 200, 'ante': 60, 'games': 5},
            {'BB': 600, 'SB': 300, 'ante': 80, 'games': 6},
            {'BB': 800, 'SB': 400, 'ante': 100, 'games': 12},
            {'BB': 1000, 'SB': 500, 'ante': 120, 'games': 12},
            {'BB': 1200, 'SB': 600, 'ante': 140, 'games': 12},
            {'BB': 1400, 'SB': 700, 'ante': 160, 'games': 12},
        ];
    def nextRound(self):
        roundData = self.roundsMap[0];
        self.updateRounds();
        for player in self.players:
            player["round"] = roundData
        for table in self.tables:
            table.handleTableUpdate()
        self.rearrangePlayers()
    
    def rearrangePlayers(self):
        positionRewardMap = [1, 1, 0.9, 0.8, 0.6, 0.4, 0.2]
        freePlayers = []
        tablePlayersMap = [0] * len(self.tables - 1)
        activePlayersCnt = 0
        for tableNr, table in enumerate(self.tables):
            for playerNr, player in enumerate(table["players"]):
                if player["stack"] <= 0:
                    table["players"][playerNr] = {"stack": -1}
                else:
                    tablePlayersMap[tableNr] += 1
                    activePlayersCnt += 1
        tableCnt = len(self.tables)
        for i in range(tableCnt):
            if math.ceil(activePlayersCnt / i) <= self.playersPerTable:
                tableCnt = i
                break
        # remove last tables if there is too many
        if len(self.tables) > tableCnt:
            for i in range(len(self.tables) - tableCnt):
                freePlayers + self.tables[len(self.tables) - 1]["players"]
                self.tables.pop(len(self.tables) - 1)
                tablePlayersMap.pop(len(tablePlayersMap) - 1)
        
        freePlayers = [player for player in freePlayers if player["stack"] != -1]
        minPlayersPerTable = math.floor(activePlayersCnt / activePlayersCnt)
        maxPlayersPerTable = math.ceil(activePlayersCnt / activePlayersCnt)
        tablesWithMaxPlayers = activePlayersCnt % tableCnt
        
        # take players from table if too many
        for index, table in enumerate(self.tables):
            if tablePlayersMap[index] > minPlayersPerTable:
                playersOverMin = tablePlayersMap[index] - minPlayersPerTable
                for i, player in enumerate(table["players"]):
                    if player["stack"] != -1 and playersOverMin > 0:
                        freePlayers.append(player)
                        table["players"][i] = {"stack": -1}
                        tablePlayersMap[index] -= 1
                        playersOverMin -= 1
        
        # distribute all freeplayer between tables
        while len(freePlayers) > 0:
            for i, table in enumerate(self.tables):
                if (tablePlayersMap[i] < minPlayersPerTable) or (tablePlayersMap[i] < maxPlayersPerTable and tablesWithMaxPlayers > 0):
                    playerIndex = len(table["palyers"])
                    for index, player in enumerate(table["players"]):
                        if player["stack"] == -1:
                            playerIndex = index
                            break
                    table["players"][playerIndex] = freePlayers[0]
                    del freePlayers[0]
                    tablePlayersMap[i] += 1;
                    if tablePlayersMap[i] >= maxPlayersPerTable:
                        tablesWithMaxPlayers -= 1
                    break
        
            for table in self.tables:
                table["players"] = [player for player in table["players"] if player["stack"] != -1]
            self.activePlayers = [player for player in self.players if player["stack"] > 0]
            def useStack(player):
                return player["stack"]
            # sort activeplayers by stack size
            self.activePlayers.sort(key=useStack)
            
            for player in self.players:
                position = 0
                for index, activePlayer in enumerate(self.activePlayers):
                    if activePlayer.name == player.name:
                        position = index + 1
                        break
                reward = -0.5
                if position != 0 and position < len(positionRewardMap) and len(self.activePlayers) < len(positionRewardMap):
                    reward = (positionRewardMap[position] + positionRewardMap[len(self.activePlayers)]) / 2
                elif position != 0:
                    reward = ((1 - len(self.activePlayers) / len(self.players)) + (1 - position / len(self.players))) / 2 - 1
                else:
                    reward = -1
                player["tableData"]["reward"] = reward
                player["tableData"]["tournamentPosition"] = position
                
            dqnLost = not [x for x in self.activePlayers if x["index"] == self.dqnNr]
            if len(self.activePlayers) > 1 and not dqnLost:
                for table in self.tables:
                    table.resetTableData()
                self.nextRound()
            else:
                if dqnLost and len(self.activePlayers) > 5:
                    self.dqn.update(-1, [0, 0, 0, 0, 0, 0])
                elif dqnLost and len(self.activePlayers) <= 5:
                    self.dqn.update(positionRewardMap[len(self.activePlayers) + 1], [0, 0, 0, 0, 0, 0])
                    #self.prizes[self.activePlayers.length + 1] += 1;
                elif not dqnLost and len(self.activePlayers) == 1:
                    self.dqn.update(1, [0, 0, 0, 0, 0, 0]);
                    #self.prizes['1'] += 1;
                self.resetTournament()
                if self.gameCnt >= self.maxGames:
                    print('Finished')
                    #console.log(`prizes: ${this.prizes}, 1-st: ${this.prizes['1']}, cnt: ${Object.keys(this.prizes).reduce((prev, next) => prev + this.prizes[next], 0)}`)
                else:
                    print('game: ' + self.gameCnt)
                    self.nextRound()
                    
    def resetTournament(self):
        dqnNr = randint(1, self.playerCnt)
        players = []
        for x in range(self.playerCnt):
            level = 0 if x == dqnNr else randint(1, 6)
            bot = self.dqn if level == 0 else SimpleBot(level)
            data = {"index": x,
                    "name": 'player-'+ x,
                    "stack": self.startingChips,
                    "bot": bot,
                    "tableData":{
                        "hand": False,
                        "firstBetPosition": False,
                        "round": False,
                        "position": False,
                        "playersCnt": False,
                        "pot": False,
                        "reward": -0.5,
                        "tournamentPosition": False
                        }
                    }
            players.append(Player(data))
            
        tables = []
        for tableNr in range(self.playerCnt / self.playersPerTable):
            tablePlayers = []
            for playerNr in range(self.playersPerTable):
                tablePlayers.append(players[tableNr * self.playersPerTable + playerNr])
            data = {"tableNr": tableNr, "updating": False, "players": tablePlayers}
            tables.append(Table(data))

        self.players = players;
        self.dqnNr = dqnNr;
        self.activePlayers = players;
        self.finishedPlayers = [];
        self.tables = tables;
        self.roundsMap = [
            {'BB': 50, 'SB': 25, 'ante': 10, 'games': 3},
            {'BB': 100, 'SB': 50, 'ante': 20, 'games': 4},
            {'BB': 200, 'SB': 100, 'ante': 40, 'games': 4},
            {'BB': 400, 'SB': 200, 'ante': 60, 'games': 5},
            {'BB': 600, 'SB': 300, 'ante': 80, 'games': 6},
            {'BB': 800, 'SB': 400, 'ante': 100, 'games': 12},
            {'BB': 1000, 'SB': 500, 'ante': 120, 'games': 12},
            {'BB': 1200, 'SB': 600, 'ante': 140, 'games': 12},
            {'BB': 1400, 'SB': 700, 'ante': 160, 'games': 12},
        ];
    
    def updateRounds(self):
        self.roundsMap[0]['games'] -= 1
        if self.roundsMap[0]['games'] <= 0:
            del self.roundsMap[0]