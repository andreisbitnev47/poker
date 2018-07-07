import React, { Component } from 'react';
import Table from '../Table';
import './Mtt.css';

class Mtt extends Component {
    constructor(props) {
        super(props);
        const {playerCnt, playersPerTable, startingChips} = props
        const dqnNr = Math.floor(Math.random() * playerCnt);
        const players = [...Array(playerCnt)].map((_, index) => {
            const level = index === dqnNr ? 0 : `${Math.floor(Math.random() * 6) + 1}`;
            const brain = level === 0 ? 'DQN' : `BOT-${level}`;
            return {
                index,
                name: `player-${index}`,
                stack: startingChips,
                inGame: false,
                timeToAct: false,
                tableData: {
                    hand: undefined,
                    firstBetPosition: undefined,
                    round: undefined,
                    position: undefined,
                    playersCnt: null,
                    pot: null,
                },
                brain,
                level,
            }
        });
        const activePlayers = players;
        const finishedPlayers = [];
        const tables = [...Array(playerCnt / playersPerTable)].map((_, tableNr) => (
            {
                tableNr,
                updating: false,
                players: [...Array(playersPerTable)].map((_, index) => players[tableNr * playersPerTable + index])
            }
        ));
        this.state = {
            players,
            activePlayers,
            finishedPlayers,
            tables,
            update: false,
            gameCnt: 0,
            roundsMap: [
                {'BB': 50, 'SB': 25, 'ante': 10, 'games': 3},
                {'BB': 100, 'SB': 50, 'ante': 20, 'games': 4},
                {'BB': 200, 'SB': 100, 'ante': 40, 'games': 4},
                {'BB': 400, 'SB': 200, 'ante': 60, 'games': 5},
                {'BB': 600, 'SB': 300, 'ante': 80, 'games': 6},
                {'BB': 800, 'SB': 400, 'ante': 100, 'games': 7}
            ],
            currentRound: undefined
        }
      }
    updatePlayers(playersToUpdate) {
        const players = [...this.state.players];
        playersToUpdate.forEach(player => {
            players[player.index] = player
        });
        this.setState({
            players
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
        const activePlayers = tablePlayersMap.reduce((prev, next) => prev + next);
        let tableCnt = tables.length;
        for(let i = 1; i <= tables.length; i++) {
            if(Math.ceil(activePlayers / i) <= playersPerTable) {
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
        const minPlayersPerTable = Math.floor(activePlayers / tableCnt);
        const maxPlayersPerTable = Math.ceil(activePlayers / tableCnt);
        let tablesWithMaxPlayers = activePlayers % tableCnt;
        // take players from table if too many
        tables.forEach((table, index) => {
            if (tablePlayersMap[index] > minPlayersPerTable) {
                let playersOverMin = tablePlayersMap[index] - minPlayersPerTable;
                for (let i = table.players.length - 1; i >= 0; i--) {
                    if (table.players[i] && playersOverMin) {
                        freePlayers.push(table.players[i]);
                        delete table.players[i];
                        playersOverMin--;
                    }
                }
            }
        });
        // distribute all freeplayer between tables
        let tableNr = 0;
        while (freePlayers.length) {
            if (tablePlayersMap[tableNr] < minPlayersPerTable || (
                tablePlayersMap[tableNr] < maxPlayersPerTable && tablesWithMaxPlayers
            )) {
                let playerIndex = tables[tableNr].players.findIndex(player => !player);
                playerIndex = playerIndex === -1 ? tables[tableNr].players.length : playerIndex;
                tables[tableNr].players[playerIndex] = freePlayers[0];
                freePlayers.splice(0, 1);
                tablePlayersMap[tableNr] += 1;
                if (tablePlayersMap[tableNr] >= maxPlayersPerTable) {
                    tablesWithMaxPlayers--;
                }
            }
            tableNr = tableNr < tables.length - 1 ? tableNr + 1 : 0;
        }
        tables.forEach((table) => {
            table.players = table.players.filter(table => !!table);
        });
        this.setState({
            tables
        })
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
        const {tables, update} = this.state;
        return (
        <div className="content">
            <button onClick={() => this.nextRound()}>Update</button>
            <div className="tables">
                {tables.map((table, index) => (
                    <Table 
                        key={index}
                        players={table.players}
                        tableNr={index}
                        update={update}
                        round={this.state.currentRound}
                        playersCnt={this.state.activePlayers.length}
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