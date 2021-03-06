import React, { Component } from 'react';
import Table from '../Table';
import './Mtt.css';
import Dqn from '../../scripts/dqn';

class Mtt extends Component {
    constructor(props) {
        super(props);
        const {playerCnt, playersPerTable, startingChips} = props
        const dqnNr = Math.floor(Math.random() * playerCnt);
        const players = [...Array(playerCnt)].map((_, index) => {
            const level = index === dqnNr ? 0 : `${Math.floor(Math.random() * 6) + 1}`;
            const brain = level === 0 ? 'DQN' : `BOT-${level}`;
            return {
                id: this.uuid(),
                index,
                name: `player-${index}`,
                stack: startingChips,
                inGame: false,
                timeToAct: false,
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
        });
        const activePlayers = players;
        const finishedPlayers = [];
        const tables = [...Array(playerCnt / playersPerTable)].map((_, tableNr) => (
            {
                id: this.uuid(),
                tableNr,
                updating: false,
                players: [...Array(playersPerTable)].map((_, index) => players[tableNr * playersPerTable + index])
            }
        ));
        this.state = {
            dqnNr,
            players,
            activePlayers,
            finishedPlayers,
            tables,
            update: false,
            resetTableData: false,
            gameCnt: 0,
            roundsMap: [
                {'BB': 50, 'SB': 25, 'ante': 10, 'games': 3},
                {'BB': 100, 'SB': 50, 'ante': 20, 'games': 4},
                {'BB': 200, 'SB': 100, 'ante': 40, 'games': 4},
                {'BB': 400, 'SB': 200, 'ante': 60, 'games': 5},
                {'BB': 600, 'SB': 300, 'ante': 80, 'games': 6},
                {'BB': 800, 'SB': 400, 'ante': 100, 'games': 12},
                {'BB': 1000, 'SB': 500, 'ante': 120, 'games': 12},
            ],
            currentRound: undefined
        }
      }
    uuid() {
        return Math.random().toString(36).substring(2) 
               + (new Date()).getTime().toString(36);
    }
    updatePlayers(playersToUpdate) {
        const players = [...this.state.players];
        playersToUpdate.forEach(player => {
            players[player.index] = player
        });
        this.setState({
            players,
            resetTableData: false,
        })
    }
    updateTable(tableNr, updating) {
        const tables = [...this.state.tables];
        let update = this.state.update;
        if (updating) {
            update = false;
        }
        tables[tableNr]['updating'] = updating;

        const tablesUpdated = !tables.find(table => table.updating);
        this.setState({
            tables,
            update
        }, () => {
            if (tablesUpdated) {
                this.rearrangePlayers();
            }
        })
    }

    rearrangePlayers() {
        const tables = [...this.state.tables];
        const { playersPerTable } = this.props;
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
        // distribute all freeplayers between tables
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
        tables.forEach((table) => {
            table.players = table.players.filter(table => !!table);
        });

        const players = [...this.state.players];
        const activePlayers = players.filter(player => player.stack > 0).sort((a, b) => b.stack - a.stack);
        const positionRewardMap = [1, 1, 0.9, 0.8, 0.6, 0.4, 0.2]
        players.forEach((player) => {
            const position = activePlayers.findIndex(activePlayer => activePlayer.name === player.name) + 1;
            let reward;
            if (position && position < positionRewardMap.length && activePlayers.length <= positionRewardMap.length) {
                reward = positionRewardMap[position];
            } else if (position) {
                reward = ((1 - activePlayers.length / players.length) + (1 - position / players.length)) / 2 - 1;
            } else {
                reward = -1;
            }
            player.tableData.reward = reward;
            player.tableData.tournamentPosition = position;
        });

        this.setState({
            tables,
            players,
            resetTableData: true,
        }, () => {
            const dqnLost = !activePlayers.find(player => player.index === this.state.dqnNr);
            // if(activePlayers.length > 1 && !dqnLost) {
            //     this.nextRound();
            // } else {
            //     const dqn = new Dqn();
            //     if(dqnLost) {
            //         dqn.update(-1, [0, 0, 0, 0, 0, 0]);
            //     } else {
            //         dqn.update(1, [0, 0, 0, 0, 0, 0]);
            //     }
            //     this.resetTournament()
            // }
        })
    }
    resetTournament() {
        const {playerCnt, playersPerTable, startingChips} = this.props
        const dqnNr = Math.floor(Math.random() * playerCnt);
        const players = [...Array(playerCnt)].map((_, index) => {
            const level = index === dqnNr ? 0 : `${Math.floor(Math.random() * 6) + 1}`;
            const brain = level === 0 ? 'DQN' : `BOT-${level}`;
            return {
                id: this.uuid(),
                index,
                name: `player-${index}`,
                stack: startingChips,
                inGame: false,
                timeToAct: false,
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
        });
        const activePlayers = players;
        const finishedPlayers = [];
        const tables = [...Array(playerCnt / playersPerTable)].map((_, tableNr) => (
            {
                id: this.uuid(),
                tableNr,
                updating: false,
                players: [...Array(playersPerTable)].map((_, index) => players[tableNr * playersPerTable + index])
            }
        ));
        this.setState({
            dqnNr,
            players,
            activePlayers,
            finishedPlayers,
            tables,
            update: false,
            resetTableData: false,
            gameCnt: 0,
            currentRound: undefined
        });
    }
    updateRounds() {
        const roundsMap = [...this.state.roundsMap];
        --roundsMap[0]['games'];
        if(roundsMap[0]['games'] <= 0) {
            roundsMap.splice(0, 1);
        }
        this.setState({roundsMap})
    }
    nextRound() {
        const round = {...this.state.roundsMap[0]};
        this.updateRounds();
        this.setState({
            update: true,
            currentRound: round
        });
    }
    render() {
        const {tables, update, resetTableData, players } = this.state;
        return (
        <div className="content">
            <button onClick={() => this.nextRound()}>Update</button>
            {/* <button onClick={() => this.setState({resetTableData: true})}>Reset</button> */}
            <div className="tables">
                <p>Money: {players.reduce((prev, next) => prev + next.stack, 0)}</p>
                <p>Players: {players.reduce((prev, next) => next.stack > 0 ? prev + 1 : prev, 0)}</p>
                {tables.map((table, index) => (
                    <Table 
                        key={table.id}
                        players={table.players}
                        tableNr={index}
                        update={update}
                        resetTableData={resetTableData}
                        round={this.state.currentRound}
                        updatePlayers={this.updatePlayers.bind(this)}
                        updateTable={this.updateTable.bind(this)}
                    />
                ))}
            </div>
        </div>
        );
    }
}

export default Mtt;