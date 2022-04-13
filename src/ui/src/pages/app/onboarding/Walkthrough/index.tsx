import React from 'react';
import Page from 'components/Page';
import { Button, Col, Row } from 'react-bootstrap';

const DashboardIndex: React.FC = () => {
  return (
    <Page selectedTab="dashboard">
      <div style={{paddingLeft: 96}} className="bg-light">
        <div className="container">
          <main className="col-md-12 ms-sm-auto col-lg-12">
            <div className="pt-3 pb-2 mb-3"></div>
            <div className="row">

              <div className="py-5 text-center col-md-8 mx-auto">
                <img className="d-block mx-auto mb-4" src="https://www.monosi.dev/images/monosi_logo.png" alt="" height="72" />
                <div className="pb-4">
                  <h2>MonoSi Walkthrough</h2>
                  <p className="lead">Start monitoring your data quality in minutes.</p>
                    <div className="row align-items-md-stretch mb-4">
                      <div className="col-md-6">
                        <div className="h-80 p-5 text-white bg-dark rounded-3">
                          <h2>2-min Demo Video</h2>
                          <button className="btn btn-outline-light" type="button">Watch</button>
                        </div>
                      </div>
                      <div className="col-md-6">
                        <div className="h-80 p-5 bg-light border rounded-3">
                          <h2>Explore Demo Data</h2>
                          <button className="btn btn-outline-secondary" type="button">Browse</button>
                        </div>
                      </div>
                    </div>
                  <Button variant="primary btn-lg">Set up a data source</Button>
                </div>
                <Button variant="outline-secondary btn-sm">Skip Onboarding</Button>
              </div>

            </div>
          </main>
        </div>
      </div>
    </Page>
  );
};

export default DashboardIndex;


