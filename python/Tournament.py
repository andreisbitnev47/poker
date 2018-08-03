from Player import Player
from Table import Table
from random import randint
from ai import Dqn
from SimpleBot import SimpleBot
import math as math
import time
from Logger import logger

class Tournament():
    
    def __init__(self, playerCnt, playersPerTable, startingChips, maxGames):
        dqnNr = randint(1, playerCnt)
        logger('DQN - ' + str(dqnNr), 'default')
        players = []
        #self.dqn = Dqn(6,2,0.9)
        #self.dqn.load()
        self.dqn = SimpleBot(1)
        for x in range(playerCnt):
            level = 0 if x == dqnNr else randint(1, 6)
            bot = self.dqn if level == 0 else SimpleBot(level)
            data = {"index": x,
                    "name": 'player-'+ str(x),
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
                        "reward": -0.8,
                        "tournamentPosition": False
                        }
                    }
            players.append(Player(data))
            
        tables = []
        for tableNr in range(int(playerCnt / playersPerTable)):
            tablePlayers = []
            for playerNr in range(playersPerTable):
                tablePlayers.append(players[tableNr * playersPerTable + playerNr])
            data = {"tableNr": tableNr, "updating": False, "players": tablePlayers, "logger": logger}
            tables.append(Table(data))
         
        self.maxGames = maxGames
        self.gameCnt = 0
        self.prizes = {
            '1': 0,
            '2': 0,
            '3': 0,
            '4': 0,
            '5': 0,
            '6': 0,
        }
        self.playerCnt = playerCnt
        self.startingChips = startingChips
        self.playersPerTable = playersPerTable
        self.players = players
        self.dqnNr = dqnNr
        self.activePlayers = players
        self.finishedPlayers = []
        self.tables = tables
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
            {'BB': 1600, 'SB': 800, 'ante': 180, 'games': 12},
            {'BB': 1800, 'SB': 900, 'ante': 200, 'games': 12},
            {'BB': 2000, 'SB': 1000, 'ante': 220, 'games': 12},
        ]
        self.dqnResults = {}
        logger(self.gameCnt, 'game')
    def nextRound(self):
        roundData = self.roundsMap[0]
        logger(roundData, 'round')
        self.updateRounds()
        for player in self.players:
            player.updateTableData("round", roundData)
        for tableNr, table in enumerate(self.tables):
            logger('table: ' + str(tableNr), 'tableNr')
            table.handleTableUpdate()
        self.rearrangePlayers()
        
    def results(self):
        return self.dqnResults
    
    def saveDqn(self):
        #self.dqn.save()
        print('saved')
        
    def rearrangePlayers(self):
        positionRewardMap = [1, 1, 0.9, 0.8, 0.6, 0.4, 0.2]
        freePlayers = []
        tablePlayersMap = [0] * len(self.tables)
        self.activePlayers = []
        for tableNr, table in enumerate(self.tables):
            tablePlayers = table.getPlayers()
            for playerNr, player in enumerate(tablePlayers):
                if player.getData("stack") <= 0:
                    tablePlayers[playerNr] = False
                else:
                    tablePlayersMap[tableNr] += 1
                    self.activePlayers.append(tablePlayers[playerNr])
            table.updatePlayers(tablePlayers)
            
        tableCnt = len(self.tables)
        for i in range(tableCnt):
            if math.ceil(len(self.activePlayers) / (i + 1)) <= self.playersPerTable:
                tableCnt = i + 1
                break
        # remove last tables if there is too many
        if len(self.tables) > tableCnt:
            for i in range(len(self.tables) - tableCnt):
                freePlayers = self.tables[len(self.tables) - 1].getPlayers()
                del self.tables[len(self.tables) - 1]
                del tablePlayersMap[len(tablePlayersMap) - 1]
        
        freePlayers = [player for player in freePlayers if player != False]
        
        minPlayersPerTable = math.floor(len(self.activePlayers) / len(self.tables))
        maxPlayersPerTable = math.ceil(len(self.activePlayers) / len(self.tables))
        tablesWithMaxPlayers = len(self.activePlayers) % len(self.tables)
        logger({"min": minPlayersPerTable, "max": maxPlayersPerTable, "maxCnt": tablesWithMaxPlayers}, 'minMax')
        # take players from table if too many
        for index, table in enumerate(self.tables):
            tablePlayers = table.getPlayers()
            if tablePlayersMap[index] > minPlayersPerTable:
                playersOverMin = tablePlayersMap[index] - minPlayersPerTable
                for i, player in enumerate(tablePlayers):
                    if not not player and playersOverMin > 0:
                        freePlayers.append(player)
                        tablePlayers[i] = False
                        tablePlayersMap[index] -= 1
                        playersOverMin -= 1
            table.updatePlayers(tablePlayers)
            
        
        # distribute all freeplayer between tables
        while len(freePlayers) > 0:
            for i, table in enumerate(self.tables):
                tablePlayers = table.getPlayers()
                if (tablePlayersMap[i] < minPlayersPerTable) or (tablePlayersMap[i] < maxPlayersPerTable and tablesWithMaxPlayers > 0):
                    playerIndex = len(tablePlayers)
                    for index, player in enumerate(tablePlayers):
                        if not player:
                            playerIndex = index
                            break
                    table.setPlayer(freePlayers[0], playerIndex)
                    del freePlayers[0]
                    tablePlayersMap[i] += 1
                    if tablePlayersMap[i] >= maxPlayersPerTable:
                        tablesWithMaxPlayers -= 1
                    break
                table.updatePlayers(tablePlayers)
        
        # remove empty players from table
        for table in self.tables:
            unsortedTablePlayers = table.getPlayers()
            tablePlayers = [player for player in unsortedTablePlayers if not not player]
            table.updatePlayers(tablePlayers)
        
        def useStack(player):
            return player.getData("stack")
        # sort activeplayers by stack size
        self.activePlayers.sort(key=useStack)
        
        for player in self.players:
            position = 0
            for index, activePlayer in enumerate(self.activePlayers):
                if activePlayer.getData("name") == player.getData("name"):
                    position = index + 1
                    break
            reward = -0.8
            if position != 0 and position < len(positionRewardMap) and len(self.activePlayers) < len(positionRewardMap):
                reward = (positionRewardMap[position] + positionRewardMap[len(self.activePlayers)]) / 2
            elif position != 0:
                reward = ((1 - len(self.activePlayers) / len(self.players)) + (1 - position / len(self.players))) / 2 - 1
            else:
                reward = -1
            player.updateTableData("reward", reward)
            player.updateTableData("tournamentPosition", position)
            
        dqnPlayer = [x for x in self.activePlayers if x.getData("index") == self.dqnNr]
        dqnLost = not dqnPlayer
        # logger(len(self.activePlayers) + 1, 'dqnPlace', 'results.txt')
        try:
            self.dqnResults[str(len(self.activePlayers) + 1)] += 1
        except:
            self.dqnResults[str(len(self.activePlayers) + 1)] = 1
        
        if len(self.activePlayers) > 1 and not dqnLost:
            for table in self.tables:
                table.resetTableData()
            self.nextRound()
        else:
            if dqnLost and len(self.activePlayers) > 5:
                self.dqn.update(-1, [0, 0, 0, 0, 0, 0])
            elif dqnLost and len(self.activePlayers) <= 5:
                self.dqn.update(positionRewardMap[len(self.activePlayers) + 1], [0, 0, 0, 0, 0, 0])
                #self.prizes[self.activePlayers.length + 1] += 1
            elif not dqnLost and len(self.activePlayers) == 1:
                self.dqn.update(1, [0, 0, 0, 0, 0, 0])
                #self.prizes['1'] += 1
            self.resetTournament()
            time.sleep(1) 
            if self.gameCnt >= self.maxGames:
                self.saveDqn()
                logger('Finished', 'default')
                print(self.dqnResults)
                #console.log(`prizes: ${this.prizes}, 1-st: ${this.prizes['1']}, cnt: ${Object.keys(this.prizes).reduce((prev, next) => prev + this.prizes[next], 0)}`)
            else:
                self.nextRound()
                    
    def resetTournament(self):
        dqnNr = randint(1, self.playerCnt)
        players = []
        for x in range(self.playerCnt):
            level = 0 if x == dqnNr else randint(1, 6)
            bot = self.dqn if level == 0 else SimpleBot(level)
            data = {"index": x,
                    "name": 'player-'+ str(x),
                    "stack": self.startingChips,
                    "bot": bot,
                    "tableData":{
                        "hand": False,
                        "firstBetPosition": False,
                        "firstBetPositionName": False,
                        "round": False,
                        "position": False,
                        "playersCnt": False,
                        "pot": False,
                        "reward": -0.8,
                        "tournamentPosition": False
                        }
                    }
            players.append(Player(data))
            
        tables = []
        for tableNr in range(int(self.playerCnt / self.playersPerTable)):
            tablePlayers = []
            for playerNr in range(self.playersPerTable):
                tablePlayers.append(players[tableNr * self.playersPerTable + playerNr])
            data = {"tableNr": tableNr, "updating": False, "players": tablePlayers, "logger": logger}
            tables.append(Table(data))
        
        self.players = players
        self.dqnNr = dqnNr
        self.activePlayers = players
        self.finishedPlayers = []
        self.tables = tables
        self.gameCnt += 1
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
        ]
        logger(self.gameCnt, 'game')
        print('game: ' + str(self.gameCnt))
        # save every 50 games
        if self.gameCnt % 50 == 0:
            self.saveDqn()
    
    def updateRounds(self):
        self.roundsMap[0]['games'] -= 1
        if self.roundsMap[0]['games'] <= 0:
            del self.roundsMap[0]

tournament = Tournament(36, 9, 500, 10);
tournament.nextRound()