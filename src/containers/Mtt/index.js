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
                status: 'active',
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

        this.setState({
            tables,
            update
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