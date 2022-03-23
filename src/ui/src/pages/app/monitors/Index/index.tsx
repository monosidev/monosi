import React, { useState, useEffect } from 'react';

import MonitorService from 'services/monitors';
import BootstrapPage from 'components/BootstrapPage';
import Flyout from 'components/Flyout';

import MonitorForm from './components/MonitorForm';
import MonitorsTable from './components/MonitorsTable';

const MonitorsIndex: React.FC = () => {
  const [monitors, setMonitors] = useState([]);

  const loadMonitors = async () => {
    let res = await MonitorService.getAll();
    if (res && res.monitors) {
      setMonitors(res.monitors);
    }
  };

  useEffect(() => {
    loadMonitors();
  }, []);


  return (
    <BootstrapPage selectedTab="monitors">
      <div style={{paddingLeft: 96}} className="bg-light">
        <div className="container">
          <main className="col-md-12 ms-sm-auto col-lg-12">
            <div className="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
              <h1 className="h2">Monitors</h1>
            </div>

            <MonitorsTable
              monitors={monitors}
            />
          </main>
        </div>
      </div>
    </BootstrapPage>
  );
};

export default MonitorsIndex;