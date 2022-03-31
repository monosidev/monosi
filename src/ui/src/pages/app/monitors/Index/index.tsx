import React, { useState, useEffect } from 'react';

import { Button, ButtonGroup } from 'react-bootstrap';
import MonitorService from 'services/monitors';
import Page from 'components/Page';
import MonitorsTable from './components/MonitorsTable';

enum MonitorFilters {
  ENABLED = "enabled", 
  PENDING = "pending", 
  DISABLED = "disabled"
}


const MonitorsIndex: React.FC = () => {
  const [monitors, setMonitors] = useState<any[]>([]);
  const [monitorFilter, setMonitorFilter] = useState<MonitorFilters>(MonitorFilters.ENABLED);
  const [filteredMonitors, setFilteredMonitors] = useState<any[]>(monitors);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const loadMonitors = async () => {
    setIsLoading(true);
    let res = await MonitorService.getAll();
    if (res && res.monitors) {
      setMonitors(res.monitors);
      filterMonitors(MonitorFilters.ENABLED, res.monitors);
    }
    setIsLoading(false);
  };

  useEffect(() => {
    loadMonitors();
  }, []);

  const filterMonitors = async (filterType: MonitorFilters, monitors: any[]) => {
    setMonitorFilter(filterType);
    let filteredMonitors = [];

    switch (filterType) {
      case MonitorFilters.PENDING: { 
        filteredMonitors = monitors.filter(m => m.metrics === 0 && m.timestamp_field !== null)
        break; 
     } 
     case MonitorFilters.DISABLED: {
        filteredMonitors = monitors.filter(m => m.timestamp_field === null)
        break; 
     } 
     default: { 
        filteredMonitors = monitors.filter(m => m.timestamp_field !== null && m.metrics !== 0)
        break; 
     } 
    }

    setFilteredMonitors(filteredMonitors);
  }

  return (
    <Page selectedTab="monitors">
      <div style={{paddingLeft: 96}} className="bg-light">
        <div className="container">
          <main className="col-md-12 ms-sm-auto col-lg-12">
            <div className="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
              <h1 className="h2">Monitors</h1>
            </div>

            <ButtonGroup aria-label="Status Filter" style={{paddingBottom: 24}}>
              <Button variant={monitorFilter === MonitorFilters.ENABLED ? "primary" : "secondary"} onClick={() => filterMonitors(MonitorFilters.ENABLED, monitors)}>Succeeded</Button>
              <Button variant={monitorFilter === MonitorFilters.PENDING ? "primary" : "secondary"} onClick={() => filterMonitors(MonitorFilters.PENDING, monitors)}>Pending</Button>
              <Button variant={monitorFilter === MonitorFilters.DISABLED ? "primary" : "secondary"} onClick={() => filterMonitors(MonitorFilters.DISABLED, monitors)}>Disabled</Button>
            </ButtonGroup>

            <MonitorsTable
              monitors={filteredMonitors}
              isLoading={isLoading}
            />
          </main>
        </div>
      </div>
    </Page>
  );
};

export default MonitorsIndex;
