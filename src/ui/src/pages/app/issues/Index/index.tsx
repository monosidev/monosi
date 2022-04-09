import React from 'react';

import Page from 'components/Page';
import IssuesTable from './components/IssuesTable';

const IssuesIndex: React.FC = () => {
  return (
    <Page selectedTab="issues">
      <div style={{paddingLeft: 96}} className="bg-light">
        <div className="container">
          <main className="col-md-12 ms-sm-auto col-lg-12">
            <div className="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
              <h1 className="h2">Issues</h1>
            </div>

            <IssuesTable />
          </main>
        </div>
      </div>
    </Page>
  );
};

export default IssuesIndex;

