import React, { useState, useEffect } from 'react';
import { EuiPanel, EuiSearchBar, EuiSpacer } from '@elastic/eui';

import AppPage from 'components/AppPage';
import MonitorService from 'services/monitors';
import Flyout from 'components/Flyout';

import MonitorForm from './components/MonitorForm';
import SearchAndFilters from './components/SearchAndFilters';
import MonitorsTable from './components/MonitorsTable';

const initialQuery = EuiSearchBar.Query.MATCH_ALL;

const MonitorsIndex: React.FC = () => {
  const [tableQuery, setTableQuery] = useState(initialQuery);

  const [monitors, setMonitors] = useState([]);
  const [loading, setLoading] = useState(false);

  const loadMonitors = async () => {
    setLoading(true);

    let res = await MonitorService.getAll();
    if (res && res.monitors) {
      setMonitors(res.monitors);
    }

    setLoading(false);
  };

  useEffect(() => {
    loadMonitors();
  }, []);


  let flyout = <Flyout name="Monitor" form={<MonitorForm />} />

  return (
    <AppPage 
      title={'Monitors'} 
      rightSideItems={[flyout]}
      >
      <SearchAndFilters setTableQuery={setTableQuery} monitors={monitors} />
      <EuiSpacer size="s" />
      <EuiPanel>
        <MonitorsTable
          query={tableQuery}
          monitors={monitors}
          loading={loading}
        />
      </EuiPanel>
    </AppPage>
  );
};

export default MonitorsIndex;
