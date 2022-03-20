import React, { useState, useEffect } from 'react';
import MonitorService from 'services/monitors';

import { Server, Diagram3 } from 'react-bootstrap-icons';
import BootstrapTable from "react-bootstrap-table-next";
import paginationFactory from "react-bootstrap-table2-paginator";

import ToolkitProvider, { Search } from 'react-bootstrap-table2-toolkit';

import './table.css';

const BootstrapMonitorsTable: React.FC<{
  monitors: any;
}> = ({ monitors }) => {

  const titleCase = (input: string) => {
    return input.split('_').map((el: string) => el.charAt(0).toUpperCase() + el.slice(1)).join(' ')
  }

  const handleDelete = (id: any) => {
    async function deleteMonitor(id: string) {
        let res = await MonitorService.delete(id);
        if (res !== null && res.monitor) {
          // success
        } else {
          //fail
        }
    }
    deleteMonitor(id);
    window.location.reload();
  }

  const columns = [
    {
      dataField: "metrics",
      text: "Status",
      formatter: (cell: any, row: any) => {
        return (
          <span className="badge rounded-pill bg-success">{row.metrics} passed</span>
        );
      },
      search: false,
    },
    // {
    //   dataField: "source",
    //   text: "Data Source",
    //   sort: true
    // },
    {
      dataField: "type",
      text: "Type",
      formatter: (cell: any, row: any) => {
        return titleCase(row.type);
      },
      filterValue: (_: any, row: any) => titleCase(row.type),
    },
    {
      dataField: "name",
      text: "Name",
      sort: true,
      formatter: (cell: any, row: any) => {
        return (
          <div>
            <a href={"/monitors/"+row.id} style={{textDecoration: 'none'}}>{row.table_name}</a>
            <small className="d-block">
              <span><Server /> {row.database}</span>
              <span style={{marginLeft: 10}}><Diagram3 /> {row.schema}</span>
            </small>
          </div>
        )
      },
      filterValue: (_: any, row: any) => [row.table_name, row.database, row.schema].join(' '),
    },
    {
      dataField: "metrics",
      text: "Metrics",
      sort: true,
    },
    {
      dataField: "created_at",
      text: "Last Update",
      sort: true,
      formatter: (cell: any, row: any) => {
        return new Date(row.created_at).toDateString();
      },
      filterValue: (cell: any, row: any) => row.created_at,
    },
    {
      dataField: "id",
      text: "",
      formatter: (cell: any, row: any) => {
          return(
            <button 
              onClick={() => handleDelete(row.id)} 
              type="button" 
              className="btn btn-sm btn-outline-danger"
              disabled={process.env.REACT_APP_IS_DEMO === 'true'}>
              Delete
            </button>
          );
      },
    },
  ];

  const emptyState = () => {
    return (
      <div className="p-5 mb-4 rounded-3" style={{background: '#f1f1f1'}}>
        <div className="container-fluid py-5">
          <h1 className="display-5 fw-bold">Sorry, no data quality yet!</h1>
          <p className="col-md-8 fs-4">You need to create a data source in order to start monitoring, alerting, and increasing your data quality.</p>
          <small>If you haven't created a data source yet, <a href="/settings/sources">start there</a></small>
        </div>
      </div>
    )
  }
  
  if (monitors.length == 0) {
        return emptyState();
  }
  else {
          return (
          <ToolkitProvider
            keyField="id"
            data={monitors}
            columns={columns}
            search
            >
            {
                props => (
                  <div>
                    <Search.SearchBar { ...props.searchProps } />
                    <div className="table-responsive custom-table custom-table-responsive">
                      <BootstrapTable
                        { ...props.baseProps }
                        bordered={false}
                        pagination={paginationFactory({ sizePerPage: 10 })}
                      />
                    </div>
                  </div>
                )
            }
            </ToolkitProvider>
          );
  }
};

export default BootstrapMonitorsTable;

