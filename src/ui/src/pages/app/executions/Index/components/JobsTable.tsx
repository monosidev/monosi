import React, { useState, useEffect } from 'react';
import { format } from 'date-fns';
import JobService from 'services/jobs';

import BootstrapTable from "react-bootstrap-table-next";
import paginationFactory from "react-bootstrap-table2-paginator";

import ToolkitProvider from 'react-bootstrap-table2-toolkit';

const JobsTable: React.FC = () => {
  const [jobs, setJobs] = useState<any[]>([]);

  useEffect(() => {
    async function loadJobs() {
      let res = await JobService.getAll();
      if (res !== null && res) {
        setJobs(res);
      }
    }

    loadJobs();
  }, []);

  const columns = [
    {
      dataField: "name",
      text: "Name",
    },
    {
      dataField: "trigger",
      text: "Type",
    },
    {
      dataField: "hours",
      text: "Interval (hrs)",
    },
    {
      dataField: "start_date",
      text: "Start Date",
      formatter: (cell: any, row: any) => {
        return format(new Date(row.start_date), 'eeee, dd MMMM HH:mm:ss');
      },
    },
    {
      dataField: "next_run_time",
      text: "Next Run Time",
      formatter: (cell: any, row: any) => {
        return format(new Date(row.next_run_time), 'eeee, dd MMMM HH:mm:ss');
      },
    },
  ];
  
  const emptyState = () => {
    return (
      <div className="p-5 mb-4 rounded-3" style={{background: '#f1f1f1'}}>
        <div className="container-fluid py-5">
          <h1 className="display-5 fw-bold">No jobs yet!</h1>
          <p className="col-md-8 fs-4">You need to create a data source in order to start tracking the status of ingestion jobs</p>
          <small>If you haven't created a data source yet, <a href="/settings/sources">start there</a></small>
        </div>
      </div>
    )
  }
  if (jobs.length == 0) {
        return emptyState();
  }

  return(
    <ToolkitProvider
        keyField="id"
        data={jobs}
        columns={columns}
        >
        {
          props => (
              <div className="mt-4 table-responsive custom-table custom-table-responsive">
                <BootstrapTable
                  { ...props.baseProps }
                  bordered={false}
                  pagination={paginationFactory({ sizePerPage: 10 })}
                />
              </div>
           )
        }
      </ToolkitProvider>
    );
};

export default JobsTable;


