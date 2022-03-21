import React from 'react';

import BootstrapPage from 'components/BootstrapPage';
import ExecutionsTable from './components/ExecutionsTable';

const ExecutionsIndex: React.FC = () => {
  return (
    <BootstrapPage selectedTab="executions">
      <div style={{paddingLeft: 96}} className="bg-light">
        <div className="container">
          <main className="col-md-12 ms-sm-auto col-lg-12">
            <div className="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
              <h1 className="h2">Executions</h1>
            </div>

            <ExecutionsTable />
          </main>
        </div>
      </div>
    </BootstrapPage>
  );
};

export default ExecutionsIndex;
