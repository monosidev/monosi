import React, { useEffect, useState } from 'react';
import { Button, ButtonGroup } from 'react-bootstrap';

import { Server, Diagram3 } from 'react-bootstrap-icons';
import BootstrapTable from "react-bootstrap-table-next";
import paginationFactory from "react-bootstrap-table2-paginator";

import ToolkitProvider, { Search } from 'react-bootstrap-table2-toolkit';

import { formatTimestamp } from 'utils/timestampFormatting';

import './table.css';

enum MonitorFilters {
  ENABLED = "enabled", 
  PENDING = "pending", 
  DISABLED = "disabled"
}


const MonitorsTable: React.FC<{
  monitors: any;
  isLoading: boolean;
}> = ({ monitors, isLoading }) => {
  const [monitorFilter, setMonitorFilter] = useState<MonitorFilters>(MonitorFilters.ENABLED);
  const [filteredMonitors, setFilteredMonitors] = useState<any[]>(monitors);

  useEffect(() => {
      setMonitorsByFilter(MonitorFilters.ENABLED, monitors);
  }, [monitors])

  const titleCase = (input: string) => {
    return input.split('_').map((el: string) => el.charAt(0).toUpperCase() + el.slice(1)).join(' ')
  }

  const columns = [
    {
      dataField: 'metrics',
      text: "Status",
      formatter: (cell: any, row: any) => {
        // if (row.timestamp_field === null) {
        //         return (
        //           <span className="badge rounded-pill bg-danger">Disabled</span>
        //         )
        // } else 
        if (row.metrics == 0) {
                return (
                  <span className="badge rounded-pill bg-warning">Pending</span>
                );
        } else {
                return (
                  <span className="badge rounded-pill bg-success">Enabled</span>
                );
        }
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
        return formatTimestamp(row.created_at)
      },
      filterValue: (cell: any, row: any) => row.created_at,
    },
  ];

  const loadingState = () => (
    <div className="p-5 mb-4 rounded-3" style={{background: '#f1f1f1'}}>
      <div className="container-fluid py-5">
        <h1 className="display-5 fw-bold">Loading data quality monitors.</h1>
        <p className="col-md-8 fs-4">This may take a few seconds.</p>
      </div>
    </div>
  );

  const filterMonitors = (filterType: MonitorFilters, monitors: any[]) => {
    let filteredMonitors = [];

    switch (filterType) {
      case MonitorFilters.PENDING: { 
        filteredMonitors = monitors.filter(m => m.metrics === 0 && m.timestamp_field !== null)
        break; 
     } 
     case MonitorFilters.DISABLED: {
        filteredMonitors = []
        break; 
     } 
     default: { 
        filteredMonitors = monitors.filter(m => m.timestamp_field !== null && m.metrics !== 0)
        break; 
     } 
    }
    return filteredMonitors;
  }

  const setMonitorsByFilter = async (filterType: MonitorFilters, monitors: any[]) => {
    setMonitorFilter(filterType);
    let filteredMonitors = filterMonitors(filterType, monitors);
    setFilteredMonitors(filteredMonitors);
  }

  const buttonFilters = () => {
        return (
            <ButtonGroup aria-label="Status Filter" style={{'paddingRight': 20}}>
              <Button variant={monitorFilter === MonitorFilters.ENABLED ? "primary" : "secondary"} onClick={() => setMonitorsByFilter(MonitorFilters.ENABLED, monitors)}>Succeeded ({filterMonitors(MonitorFilters.ENABLED, monitors).length})</Button>
              <Button variant={monitorFilter === MonitorFilters.PENDING ? "primary" : "secondary"} onClick={() => setMonitorsByFilter(MonitorFilters.PENDING, monitors)}>Pending ({filterMonitors(MonitorFilters.PENDING, monitors).length})</Button>
              <Button variant={monitorFilter === MonitorFilters.DISABLED ? "primary" : "secondary"} onClick={() => setMonitorsByFilter(MonitorFilters.DISABLED, monitors)}>Disabled ({filterMonitors(MonitorFilters.DISABLED, monitors).length})</Button>
            </ButtonGroup>
        )
  }

  const filters = (props: any) => {
        return (
              <div className={'float-end'} style={{paddingBottom: 10}}>
                      {buttonFilters()}
                      <Search.SearchBar { ...props.searchProps } />
              </div>
        );
  }

  const emptyState = () => {
    return (
        <div>
            <div style={{height: 58}}>
            {filters('')}
            </div>
            <div className="p-5 mb-4 rounded-3" style={{background: '#f1f1f1'}}>
              <div className="container-fluid py-5">
                <h1 className="display-5 fw-bold">No {monitorFilter} monitors yet!</h1>
                <p className="col-md-8 fs-4">Add a data source to start monitoring, or check for monitors in a different state.</p>
                <small>If you haven't created a data source yet, <a href="/settings/sources">start there.</a></small>
                <br/>
              </div>
            </div>
        </div>
     )
  };

  
  if(isLoading) {
    return loadingState();
  } else if (filteredMonitors.length === 0) {
    return emptyState();
  } else {
    return (
    <ToolkitProvider
      keyField="id"
      data={filteredMonitors}
      columns={columns}
      search
      >
      {
          props => (
            <div>
              {filters(props)}
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

export default MonitorsTable;

