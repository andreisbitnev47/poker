import React, { Component } from 'react';
import Mtt from './Mtt';

class App extends Component {
  render() {
    return (
      <div className="App">
        <Mtt playerCnt={6} playersPerTable={3} startingChips={500}/>
      </div>
    );
  }
}

export default App;
