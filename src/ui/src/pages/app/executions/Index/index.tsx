import React from 'react';

import BootstrapPage from 'components/BootstrapPage';
import ExecutionsTable from './components/ExecutionsTable';
import JobsTable from './components/JobsTable';
import { Tab, Tabs } from 'react-bootstrap';

const ExecutionsIndex: React.FC = () => {
  return (
    <BootstrapPage selectedTab="executions">
      <div style={{paddingLeft: 96}} className="bg-light">
        <div className="container">
          <main className="col-md-12 ms-sm-auto col-lg-12">
            <div className="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
              <h1 className="h2">Executions</h1>
            </div>

            <Tabs defaultActiveKey="executions" id="tabs" className="mb-4">
                <Tab eventKey="executions" title="Executions">
                    <ExecutionsTable />
                </Tab>
                <Tab eventKey="jobs" title="Jobs">
                    <JobsTable />
                </Tab>
            </Tabs>
          </main>
        </div>
      </div>
    </BootstrapPage>
  );
};

export default ExecutionsIndex;
