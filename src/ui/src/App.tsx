import React, { useEffect, useState } from "react";
import "@elastic/eui/dist/eui_theme_light.css";
import {
  BrowserRouter as Router,
  Route,
  Redirect,
  Switch,
} from "react-router-dom";

import "App.css";
// import MonitorsDetail from 'pages/app/monitors/Detail';
import UserService from "services/users";

import IntegrationsSettings from "pages/settings/Integrations";
import IssuesIndex from "pages/app/issues/Index";
import SourcesSettings from "pages/settings/Sources";
import ProfileSettings from "pages/settings/Profile";
import DashboardIndex from "pages/app/dashboard/Index";
import ExecutionsIndex from "pages/app/executions/Index";
import MonitorsIndex from "pages/app/monitors/Index";
import MonitorsDetail from "pages/app/monitors/Detail";
import MetricsDetail from "pages/app/metrics/Detail";
import OnboardingGettingStarted from "pages/app/onboarding/GettingStarted";
import { Toaster } from "sonner";

function RequireSetup({ children }: { children: JSX.Element }) {
  const [isSetup, setIsSetup] = useState(true);

  useEffect(() => {
    const retrieveUser = async () => {
      let user;
      let resp = await UserService.getAll();
      if (resp && resp["user"]) {
        user = resp["user"];
      }
      setIsSetup(user !== null && user["email"] !== null);
    };
    retrieveUser();
  }, []);

  if (isSetup) {
    return children;
  } else {
    return (
      <Switch>
        <Route exact path="/getting-started">
          <OnboardingGettingStarted />
        </Route>
        <Redirect to={"/getting-started"} />
      </Switch>
    );
  }
}

function App() {
  return (
    <div className="App" style={{ minHeight: "100vh" }}>
      <Toaster
        richColors
        position="top-center"
        expand
        visibleToasts={1}
        offset="15px"
      />
      <Router>
        <RequireSetup>
          <Switch>
            <Route exact path="/">
              <DashboardIndex />
            </Route>
            <Route exact path="/monitors">
              <MonitorsIndex />
            </Route>
            <Route exact path="/issues">
              <IssuesIndex />
            </Route>
            <Route exact path="/monitors/:id">
              <MonitorsDetail />
            </Route>
            <Route exact path="/monitors/:id/metrics">
              <MetricsDetail />
            </Route>

            <Route exact path="/executions">
              <ExecutionsIndex />
            </Route>

            <Route exact path="/settings">
              <Redirect to="/settings/profile" />
            </Route>
            <Route exact path="/settings/profile">
              <ProfileSettings />
            </Route>
            <Route exact path="/settings/sources">
              <SourcesSettings />
            </Route>
            <Route exact path="/settings/integrations">
              <IntegrationsSettings />
            </Route>
            <Route path="*">
              <Redirect to="/" />
            </Route>
          </Switch>
        </RequireSetup>
      </Router>
    </div>
  );
}

export default App;
