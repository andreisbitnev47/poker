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
                name: `player-${index}`,
                stack: startingChips,
                position: undefined,
                status: 'active',
                table: undefined,
                timeToAct: false,
                brain,
                level,
            }
        });
        const tables = [...Array(playerCnt / playersPerTable)].map((_, tableNr) => (
            {
                tableNr,
                players: [...Array(playersPerTable)].map((_, index) => players[tableNr * playersPerTable + index])
            }
        ));
        this.state = {
            players,
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
    // tables: [
    //     {
    //         pot: 300,
    //         players: [
    //             {
    //                 name: 'asd',
    //                 hand: [[11,'s'], [12, 's']],
    //                 pot: '500',
    //                 position: 'MP1',
    //             }
    //         ]
    //     }
    // ]
    updateTable(table) {
        const tables = [...this.state.tables];
        tables[table.tableNr] = table;
        this.setState({
            tables,
            update: false
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
            currentRound: round,
            update: true
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
                        table={table} 
                        tableNr={index}
                        update={update}
                        round={this.state.currentRound}
                        updateTable={this.updateTable.bind(this)}
                    />
                ))}
            </div>
        </div>
        );
    }
}

export default Mtt;