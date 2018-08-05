const Player = require('./Player');
const Table = require('./Table');
const Dqn = require('./dqn');
const SimpleBot = require('./simpleBot');

module.exports = class Tournament{
    constructor(props) {
        const {playerCnt, playersPerTable, startingChips, maxGames} = props
        const dqnNr = Math.floor(Math.random() * playerCnt);
        this.dqn = new Dqn();
        this.timeOut = [];
        // this.dqn = new SimpleBot(6)
        const players = [...Array(playerCnt)].map((_, index) => {
            const level = index === dqnNr ? 0 : `${Math.floor(Math.random() * 6) + 1}`;
            const brain = level === 0 ? 'DQN' : `BOT-${level}`;
            const bot = level ? new SimpleBot(level) : this.dqn;
            const data = {
                id: this.uuid(),
                index,
                name: `player-${index}`,
                stack: startingChips,
                bot: bot,
                tableData: {
                    hand: undefined,
                    firstBetPosition: undefined,
                    firstBetPositionName: undefined,
                    round: undefined,
                    position: undefined,
                    playersCnt: null,
                    pot: null,
                    reward: -0.5,
                    tournamentPosition: null,
                },
                brain,
                level,
            }
            return new Player(data);
        });
        const activePlayers = players;
        const finishedPlayers = [];
        const tables = [...Array(playerCnt / playersPerTable)].map((_, tableNr) => {
            const data = {
                id: this.uuid(),
                tableNr,
                updating: false,
                players: [...Array(playersPerTable)].map((_, index) => players[tableNr * playersPerTable + index])
            }
            return new Table(data);
        }); 
        this.maxGames = maxGames;
        this.gameCnt = 0;
        this.prizes = {
            '1': 0,
            '2': 0,
            '3': 0,
            '4': 0,
            '5': 0,
            '6': 0,
        }
        this.playerCnt = playerCnt;
        this.startingChips = startingChips;
        this.playersPerTable = playersPerTable;
        this.players = players;
        this.dqnNr = dqnNr;
        this.activePlayers = players;
        this.finishedPlayers = [];
        this.tables = tables;
        this.roundsMap = [
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
            {'BB': 2200, 'SB': 1200, 'ante': 240, 'games': 12},
        ];
    }
    uuid() {
        return Math.random().toString(36).substring(2) 
            + (new Date()).getTime().toString(36);
    }
    nextRound() {
        const round = this.roundsMap[0];
        this.updateRounds();
        this.players.forEach((player) => {
            player.updateTableData({round})
        });
        Promise.all(this.tables.map(table => table.handleTableUpdate()))
            .then((results) => {
                if(results.indexOf(false) !== -1) {
                    this.resetTournament();
                }
                this.rearrangePlayers();
            })
            .catch((err) => {
                console.log(err);
            })
    }
    async rearrangePlayers() {
        const positionRewardMap = [1, 1, 0.9, 0.8, 0.6, 0.4, 0.2]
        const { tables, playersPerTable, players } = this;
        let freePlayers = [];
        tables.forEach((table) => {
            table.players.forEach((player, playerIndex) => {
                if (player.stack <= 0) {
                    delete table.players[playerIndex]
                }
            })
        });
        const tablePlayersMap = tables.map(table => table.players.filter(player => !!player).length);
        const activePlayersCnt = tablePlayersMap.reduce((prev, next) => prev + next);
        let tableCnt = tables.length;
        for(let i = 1; i <= tables.length; i++) {
            if(Math.ceil(activePlayersCnt / i) <= playersPerTable) {
                tableCnt = i;
                break;
            }
        }
        // remove last tables if there is too many
        if (tables.length > tableCnt) {
            for (let i = tables.length - tableCnt; i > 0; i--) {
                freePlayers = [...freePlayers, ...tables[tables.length - 1].players];
                tables.splice([tables.length - i], 1);
                tablePlayersMap.splice([tablePlayersMap.length - i], 1)
            }
        }
        freePlayers = freePlayers.filter(player => !!player);
        const minPlayersPerTable = Math.floor(activePlayersCnt / tableCnt);
        const maxPlayersPerTable = Math.ceil(activePlayersCnt / tableCnt);
        let tablesWithMaxPlayers = activePlayersCnt % tableCnt;
        // take players from table if too many
        tables.forEach((table, index) => {
            if (tablePlayersMap[index] > minPlayersPerTable) {
                let playersOverMin = tablePlayersMap[index] - minPlayersPerTable;
                for (let i = table.players.length - 1; i >= 0; i--) {
                    if (table.players[i] && playersOverMin) {
                        freePlayers.push(table.players[i]);
                        delete table.players[i];
                        tablePlayersMap[index]--;
                        playersOverMin--;
                    }
                }
            }
        });
        // distribute all freeplayer between tables
        const timeOut = setTimeout(function() {
            console.log('this is it')
            // this.resetTournament();
        }, 500)
        while(freePlayers.length > 0) {
          for (let i = 0; i < tables.length; i++) {
            if (tablePlayersMap[i] < minPlayersPerTable || (
                tablePlayersMap[i] < maxPlayersPerTable && tablesWithMaxPlayers
            )) {
                let playerIndex = tables[i].players.findIndex(player => !player);
                playerIndex = playerIndex === -1 ? tables[i].players.length : playerIndex;
                tables[i].players[playerIndex] = freePlayers[0];
                freePlayers.splice(0, 1);
                tablePlayersMap[i] += 1;
                if (tablePlayersMap[i] >= maxPlayersPerTable) {
                    tablesWithMaxPlayers--;
                }
                break;
            }
          }
        }
        clearTimeout(timeOut);
        tables.forEach((table) => {
            table.players = table.players.filter(table => !!table);
        });
        this.activePlayers = players.filter(player => player.stack > 0).sort((a, b) => b.stack - a.stack);
        players.forEach((player) => {
            const position = this.activePlayers.findIndex(activePlayer => activePlayer.id === player.id) + 1;
            let reward;
            if (position && position < positionRewardMap.length && this.activePlayers.length < positionRewardMap.length) {
                reward = (positionRewardMap[position] + positionRewardMap[this.activePlayers.length]) / 2;
            } else if (position) {
                reward = ((1 - this.activePlayers.length / players.length) + (1 - position / players.length)) / 2 - 1;
            } else {
                reward = -1;
            }
            player.tableData.reward = reward;
            player.tableData.tournamentPosition = position;
        });

        const dqnLost = !this.activePlayers.find(player => player.index === this.dqnNr);
        if(this.activePlayers.length > 1 && !dqnLost) {
            this.tables.forEach((table) => {
                const tableReset = table.resetTableData();
                // restart tournament if tableData reset didn't go well
                if(!tableReset) {
                    this.resetTournament();
                }
            });
            this.nextRound();
        } else {
            if(dqnLost && this.activePlayers.length > 5) {
                await this.dqn.update(-1, [0, 0, 0, 0, 0, 0]);
            } else if(dqnLost && this.activePlayers.length <= 5) {
                await this.dqn.update(positionRewardMap[this.activePlayers.length + 1], [0, 0, 0, 0, 0, 0]);
                this.prizes[this.activePlayers.length + 1] += 1;
            } else if (!dqnLost && this.activePlayers.length === 1) {
                await this.dqn.update(1, [0, 0, 0, 0, 0, 0]);
                this.prizes['1'] += 1;
            }
            this.resetTournament();
            if(this.gameCnt % 1000 == 0) {
                const saveStatus = await this.dqn.save();
                console.log(saveStatus);
                
            } 
            if(this.gameCnt >= this.maxGames) {
                console.log('finished');
                console.log(`prizes: ${JSON.stringify(this.prizes)}, 1-st: ${this.prizes['1']}, cnt: ${Object.keys(this.prizes).reduce((prev, next) => prev + this.prizes[next], 0)}`)
            } else {
                var gameCnt = this.gameCnt;
                // fs.appendFile('/home/andrei/projects/poker/logs.txt', 'game ' + gameCnt + '\n', function (err) {
                //     if (err) throw err;
                //     console.log('game', gameCnt)
                // });
                console.log('game', gameCnt)
                this.nextRound();
            }
        }
    }
    resetTournament() {
        clearTimeout(this.timeOut[0]);
        this.timeOut.splice(0, 1);
        this.timeOut.push(setTimeout(function(){
            this.resetTournament();
        }.bind(this), 1000));
        const {playerCnt, playersPerTable, startingChips} = this;
        const dqnNr = Math.floor(Math.random() * playerCnt);
        const players = [...Array(playerCnt)].map((_, index) => {
            const level = index === dqnNr ? 0 : `${Math.floor(Math.random() * 6) + 1}`;
            const brain = level === 0 ? 'DQN' : `BOT-${level}`;
            const bot = level ? new SimpleBot(level) : this.dqn;
            const data = {
                id: this.uuid(),
                index,
                name: `player-${index}`,
                stack: startingChips,
                bot: bot,
                tableData: {
                    hand: undefined,
                    firstBetPosition: undefined,
                    firstBetPositionName: undefined,
                    round: undefined,
                    position: undefined,
                    playersCnt: null,
                    pot: null,
                    reward: -0.5,
                    tournamentPosition: null,
                },
                brain,
                level,
            }
            return new Player(data);
        });
        const activePlayers = players;
        const finishedPlayers = [];
        const tables = [...Array(playerCnt / playersPerTable)].map((_, tableNr) => {
            const data = {
                id: this.uuid(),
                tableNr,
                updating: false,
                players: [...Array(playersPerTable)].map((_, index) => players[tableNr * playersPerTable + index])
            }
            return new Table(data);
        });
        this.gameCnt += 1;
        this.playerCnt = playerCnt;
        this.startingChips = startingChips;
        this.playersPerTable = playersPerTable;
        this.players = players;
        this.dqnNr = dqnNr;
        this.activePlayers = players;
        this.finishedPlayers = [];
        this.tables = tables;
        this.roundsMap = [
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
            {'BB': 2200, 'SB': 1200, 'ante': 240, 'games': 12},
        ];
    }
    updateRounds() {
        --this.roundsMap[0]['games'];
        if(this.roundsMap[0]['games'] <= 0) {
            this.roundsMap.splice(0, 1);
        }
    }
}