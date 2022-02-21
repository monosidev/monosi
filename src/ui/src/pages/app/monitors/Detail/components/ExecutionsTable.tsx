import React, { useState, useEffect } from 'react';
import ExecutionService from 'services/executions';
import JobService from 'services/jobs';

import BootstrapTable from "react-bootstrap-table-next";
import paginationFactory from "react-bootstrap-table2-paginator";

import ToolkitProvider from 'react-bootstrap-table2-toolkit';

const ExecutionsTable: React.FC<{monitor_id: any}> = ({ monitor_id }) => {
  const [executions, setExecutions] = useState<any[]>([]);
  const [job, setJob] = useState<any>(null);

  useEffect(() => {
    async function loadJob() {
      let res = await JobService.get(monitor_id);
      if (res !== null) {
        setJob(res);
      }
    }
    async function loadExecutions() {
      let res = await ExecutionService.get(monitor_id);
      if (res !== null && res.executions) {
        setExecutions(res.executions);
      }
    }

    if (monitor_id !== null) {
      loadExecutions();
      loadJob();
    }
  }, [monitor_id]);

  const columns = [
    {
      dataField: "state",
      text: "Status",
    },
    {
      dataField: "created_at",
      text: "Run At",
    },
  ];

  const nextRunTime = (job: any) => {
    if (job !== null) {
        return new Date(job.next_run_time).toString();
    }
    return '-';
  }
  
  return (
    <ToolkitProvider
        keyField="id"
        data={executions}
        columns={columns}
        >
        {
          props => (
            <div>
              <h3 >Executions</h3>
              <small style={{margin: '0rem 0rem 1.5rem 0'}} >Next run at: {nextRunTime(job)}</small>
              <div className="mt-4 table-responsive custom-table custom-table-responsive">
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
};

export default ExecutionsTable;

