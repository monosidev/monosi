import React, { useState, useEffect } from 'react';
import { useParams, useLocation } from 'react-router-dom';
import { ChevronRight, ClipboardData, Server, Diagram3, Table, CpuFill, ListColumnsReverse } from 'react-bootstrap-icons';

import MonitorService from 'services/monitors';
import BootstrapPage from 'components/BootstrapPage';

import BootstrapTable from "react-bootstrap-table-next";
import paginationFactory from "react-bootstrap-table2-paginator";

import Plot from 'react-plotly.js';

const MetricsDetail: React.FC = () => {
  const { database, schema, table } = useParams<{ database: string, schema: string, table: string }>();
  const params = new URLSearchParams(useLocation().search);
  const column_name = params.get('column_name');
  const metric = params.get('metric');

  const [metrics, setMetrics] = useState([]);

  const loadMetrics = async () => {
    if (column_name == null || metric == null) return;

    let res = await MonitorService.getMetricData(database, schema, table, column_name, metric);
    if (res && res.metrics) {
      setMetrics(res.metrics);
    }
  };

  useEffect(() => {
    loadMetrics();
  }, []);


  var layout = {
    margin: {
      l: 50,
      r: 50,
      b: 0,
      t: 0,
      pad: 0
    },
    width: 1200,
  }

  const data = [{
    "x": metrics.map((el: any) => el.time_window_start),
    "y": metrics.map((el: any) => el.value),
    "name": "Values",
    "hoverinfo": "x",
    "mode": "lines+markers",
    "showlegend": false,
    "marker": {
        "color": "rgba(115, 68, 210, 1.0)"
    },
  },
  {
    "x": metrics.map((el: any) => el.time_window_start),
    "y": metrics.map((el: any) => el.expected_range_start),
    "mode": "lines",
    "hover": "skip",
    "name": "",
    "marker": {
        "color": "rgba(115, 68, 210, 0.1)"
    },
    "showlegend": false
  },
  {
    "x": metrics.map((el: any) => el.time_window_start),
    "y": metrics.map((el: any) => el.expected_range_end),
    "mode": "lines",
    "marker": {
        "color": "rgba(115, 68, 210, 0.1)"
    },
    "hover": "skip",
    "fill": "tonexty",
    "name": "",
    "fillcolor": "rgba(115, 68, 210, 0.1)",
    "showlegend": false
  }];

  const titleCase = (input: string) => {
    return input.split('_').map((el: string) => el.charAt(0).toUpperCase() + el.slice(1)).join(' ')
  }



  const columns = [
    {
      dataField: "status",
      text: "Status",
      formatter: (cell: any, row: any) => {
        return (
          <>
          {row.error == false && <span className="badge rounded-pill bg-success">Healthy</span>}
          {row.error == true && <span className="badge rounded-pill bg-danger">Unheathy</span>}
          {row.error == undefined && <span className="badge rounded-pill bg-warning">Pending</span>}
          </>
        );
      } 
    },
    {
      dataField: "time_window_start",
      text: "TS Window Start",
      sort: true
    },
    {
      dataField: "time_window_end",
      text: "TS Window End",
      sort: true
    },
    {
      dataField: "value",
      text: "Value",
    },
    {
      text: "Expected Range",
      dataField: "range",
      formatter: (cell: any, row: any) => {
        return (
          <>
          {row.expected_range_start !== undefined && <span>{row.expected_range_start} to {row.expected_range_end}</span>}
          {row.expected_range_start === undefined && <span>Pending</span>}
          </>
        );
      }
    },
  ];


  return (
    <BootstrapPage selectedTab="monitors">
      <div style={{paddingLeft: '96px'}}>
        <nav className="py-2 bg-light border-bottom">
          <div className="container d-flex flex-wrap">
            <ul className="nav me-auto">
              <li className="nav-item"><a href="/monitors" className="nav-link link-dark px-2 active" aria-current="page">Monitors</a></li>
              <li className="nav-item"><span className="nav-link link-dark px-2 text-muted">/</span></li>
              <li className="nav-item"><a href={`/monitors/${database}/${schema}/${table}`} className="nav-link link-dark px-2">{table} - Table Health</a></li>
              <li className="nav-item"><span className="nav-link link-dark px-2 text-muted">/</span></li>
              <li className="nav-item"><span className="nav-link link-dark text-muted px-2">{column_name || '-'}</span></li>
              <li className="nav-item"><span className="nav-link link-dark px-2 text-muted">/</span></li>
              <li className="nav-item"><span className="nav-link link-dark text-muted px-2">{metric || '-'}</span></li>
            </ul>
          </div>
        </nav>
        <header className="py-3 border-bottom" style={{backgroundColor: '#fff'}}>
          <div className="container d-flex flex-wrap justify-content-center">
            <div className="d-flex align-items-center mb-3 mb-lg-0 me-lg-auto text-dark text-decoration-none">
              <div className="d-flex flex-column">
                <span className="fs-4"><ListColumnsReverse style={{marginRight: 10}} /> {column_name || '-'}</span>
                <span className="fs-10"><ClipboardData style={{marginRight: 5}} /> {metric && titleCase(metric) || '-'}</span>
              </div>
            </div>

            <div className="btn-toolbar my-2 text-muted" style={{alignContent: 'center'}}>
               <span><Server /> {database}</span>
               <span style={{marginLeft: 20}}><Diagram3 /> {schema}</span>
               <span style={{marginLeft: 20}}><Table /> {table}</span>
            </div>
          </div>
        </header>
      </div>
      <div style={{paddingLeft: '96px'}} className="pt-4 bg-light">
        <div className="container">
          <main className="col-md-12 ms-sm-auto col-lg-12">
            <div className="card">
              <div className="card-body" style={{height: '100%'}}>
                <div className="btn-toolbar mb-4">
                  {/* <div className="btn-group me-2">
                                      <button type="button" className="btn btn-sm btn-outline-secondary">Share</button>
                                      <button type="button" className="btn btn-sm btn-outline-secondary">Export</button>
                                    </div>
                                    <button type="button" className="btn btn-sm btn-outline-secondary dropdown-toggle">
                                      <span data-feather="calendar"></span>
                                      This week
                                    </button> */}
                </div>
                <Plot data={data} layout={layout} />
              </div>
            </div>


            <div className="table-responsive custom-table custom-table-responsive" style={{margin: '40px 0px'}}>
              <BootstrapTable
                keyField="id"
                data={metrics}
                columns={columns}
                bordered={false}
                pagination={paginationFactory({ sizePerPage: 10 })}
              />
            </div>
          </main>
        </div>
      </div>
    </BootstrapPage>
  );
};

export default MetricsDetail;

