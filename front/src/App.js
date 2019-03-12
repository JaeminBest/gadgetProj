import React, { Component } from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import { Home, Workspace } from 'pages';

import { Header, Nav } from 'components';

class App extends Component {
  render() {
    return (
      <Router>
        <div>
          
          <Nav/>
          <Route exact path="/" component={Home}/>
          <Route path="/workspace" component={Workspace}/>
        </div>
      </Router>
      /*
      <div className="App">

      </div>
      */
    );
  }
}

export default App;
