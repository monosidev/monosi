import React from 'react';
import '@elastic/eui/dist/eui_theme_light.css';
import {
  BrowserRouter as Router,
  Route,
  Redirect,
  Switch,
} from 'react-router-dom';

import 'App.css';

import MonitorsIndex from 'pages/app/monitors/Index';
// import MonitorsDetail from 'pages/app/monitors/Detail';

import IntegrationsSettings from 'pages/settings/Integrations';
import SourcesSettings from 'pages/settings/Datasources';
import AccountSettings from 'pages/settings/Account';

function App() {
  return (
    <div className="App" style={{ minHeight: '100vh' }}>
      <Router>
        <Switch>
          <Route exact path="/monitors">
              <MonitorsIndex />
          </Route>
{/*          <Route exact path="/monitors/:id">
              <MonitorsDetail />
          </Route>*/}

          <Route exact path="/settings/profile">
              <AccountSettings />
          </Route>
          <Route exact path="/settings/sources">
              <SourcesSettings />
          </Route>
          <Route exact path="/settings/integrations">
              <IntegrationsSettings />
          </Route>

          <Route path="*">
              <Redirect to="/monitors" />
          </Route>
        </Switch>
      </Router>
    </div>
  );
}

export default App;

