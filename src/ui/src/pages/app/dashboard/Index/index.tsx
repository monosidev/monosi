import React, { useState, useEffect } from 'react';
import { ChevronRight, CloudArrowUpFill, CpuFill, ExclamationTriangle, ExclamationTriangleFill } from 'react-bootstrap-icons';

import BootstrapPage from 'components/BootstrapPage';

import './dashboard.css';


const DashboardIndex: React.FC = () => {
  return (
    <BootstrapPage selectedTab="dashboard">
      <div style={{paddingLeft: 96}} className="bg-light">
        <div className="container">
          <main className="col-md-12 ms-sm-auto col-lg-12">
            <div className="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
              <h1 className="h2">Home</h1>
              <div className="btn-toolbar mb-2 mb-md-0">
              </div>
            </div>

            <h4>Getting Started</h4>
            <div className="row row-cols-1 row-cols-lg-2 align-items-stretch g-4 py-2">
              <div className="col">
                <div className="card mb-3" >
                  <div className="row g-0" style={{height: '241px'}}>
                    <div className="col-md-6 d-flex flex-column" style={{backgroundImage: "url('unsplash-photo-2.jpg')"}}>
                    <div className="card card-cover text-white bg-dark rounded-5 shadow-lg" style={{height: '100%', textAlign: 'center', justifyContent: 'center'}}>
                        <h2 className="mb-2 display-8 lh-1 fw-bold">Data Quality</h2>
                        <a href="/monitors" className="align-items-center me-3ml-2 text-white text-decoration-none">
                          <small>Centralize & Monitor</small>
                          <ChevronRight className="bi me-2 pt-1" width={'1em'} height={'1em'} />
                        </a>
                      </div>
                    </div>
                    <div className="col-md-6 d-flex">
                      <div className="card-body" style={{alignSelf: 'center'}}>
                        <h4>Monitor, Alert, Analyze</h4>
                        <p className="card-text">Get insights on the quality of your data through automatic monitoring and alerting.</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div className="col">
                <div className="card mb-3" >
                  <div className="row g-0" style={{height: '241px'}}>
                    <div className="col-md-6 d-flex flex-column" style={{backgroundImage: "url('unsplash-photo-2.jpg')"}}>
                    <div className="card card-cover text-white bg-dark rounded-5 shadow-lg" style={{height: '100%', textAlign: 'center', justifyContent: 'center'}}>
                        <h2 className="mb-2 display-8 lh-1 fw-bold">Documentation</h2>
                        <a href="https://docs.monosi.dev" target="_blank" className="align-items-center me-3ml-2 text-white text-decoration-none">
                          <small>Read the docs</small>
                          <ChevronRight className="bi me-2 pt-1" width={'1em'} height={'1em'} />
                        </a>
                      </div>
                    </div>
                    <div className="col-md-6 d-flex">
                      <div className="card-body" style={{alignSelf: 'center'}}>
                        <h4>Learn & Join the Community</h4>
                        <p className="card-text">Learn the best practices for data quality, how to instrument Monosi, and talk and contribute with others.</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <hr className="dropdown-divider" />

            <div className="row row-cols-1 row-cols-lg-2 align-items-stretch g-4 py-3">
              <div className="col">
                <div className="d-flex pb-2" style={{justifyContent: 'spaceBetween'}}>
                 <h4>Connect a Data Source</h4>
               </div>
                <div className="card">
                  <div className="card-body">
                    <div className="col d-flex align-items-start">
                      <div className="icon-square bg-light text-dark flex-shrink-0 me-3">
                        <CloudArrowUpFill className="bi pt-1" />
                      </div>
                      <a href="/settings/sources" className="text-dark text-decoration-none">
                        <h5>Add Data</h5>
                        <p className="card-text">Collect metadata from popular databases and sources.</p>
                      </a>
                    </div>
                  </div>
                </div>
              </div>
              <div className="col">
                <div className="d-flex pb-2" style={{justifyContent: 'space-between'}}>
                 <h4>Connect an Integration</h4>
               </div>
                <div className="card">
                  <div className="card-body">
                    <div className="col d-flex align-items-start">
                      <div className="icon-square bg-light text-dark flex-shrink-0 me-3">
                        <ExclamationTriangleFill className="bi pt-1" width={'1em'} height={'1em'} />
                      </div>
                      <a href="/settings/integrations" className="text-dark text-decoration-none">
                        <h5>Add Alerts</h5>
                        <p className="card-text">Receive real-time alerts on data quality via Slack.</p>
                      </a>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </main>
        </div>
      </div>
    </BootstrapPage>
  );
};

export default DashboardIndex;

