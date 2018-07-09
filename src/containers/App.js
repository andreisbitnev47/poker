import React, { Component } from 'react';
import Mtt from './Mtt';

class App extends Component {
  render() {
    return (
      <div className="App">
        <Mtt playerCnt={36} playersPerTable={9} startingChips={500}/>
      </div>
    );
  }
}

export default App;
