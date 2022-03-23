import React, { useState, useEffect } from 'react';
import { format } from 'date-fns';
import ExecutionService from 'services/executions';
import JobService from 'services/jobs';

import BootstrapTable from "react-bootstrap-table-next";
import paginationFactory from "react-bootstrap-table2-paginator";

import ToolkitProvider from 'react-bootstrap-table2-toolkit';

import { formatTimestamp } from 'utils/timestampFormatting';

const ExecutionsTable: React.FC = () => {
  const [executions, setExecutions] = useState<any[]>([]);

  useEffect(() => {
    async function loadExecutions() {
      let res = await ExecutionService.getAll();
      if (res !== null && res.executions) {
        setExecutions(res.executions);
      }
    }

    loadExecutions();
  }, []);

  const columns = [
    {
      dataField: "state",
      text: "Status",
    },
    {
      dataField: "created_at",
      text: "Run At",
      formatter: (cell: any, row: any) => {
        return formatTimestamp(row.created_at)
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
  if (executions.length == 0) {
        return emptyState();
  }

  return(
    <ToolkitProvider
        keyField="id"
        data={executions}
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

export default ExecutionsTable;

