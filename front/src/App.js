import React, { Component } from 'react';
import Workspace from './pages/Workspace.js';

import { Header } from 'components';

class App extends Component {
  render() {
    return (
      <div className="App">
        <Header/>
        <Workspace/>
      </div>
    );
  }
}

export default App;
