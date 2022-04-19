import React, { useState, useEffect } from 'react';

import BootstrapTable from "react-bootstrap-table-next";
import paginationFactory from "react-bootstrap-table2-paginator";
import ToolkitProvider, { Search } from 'react-bootstrap-table2-toolkit';

import { formatTimestamp } from 'utils/timestampFormatting';

import IssueService from 'services/issues';


const IssuesTable: React.FC = () => {
  const [issues, setIssues] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  useEffect(() => {
    async function loadIssues() {
      setIsLoading(true);
      let res = await IssueService.getAll();
      if (res !== null && res.issues) {
        setIssues(res.issues);
      }
      setIsLoading(false);
    }

    loadIssues();
  }, []);

  const columns = [
    {
      dataField: "type",
      text: "Type",
      search: false,
    },
    {
      dataField: "entity",
      text: "Entity",
    },
    {
      dataField: "message",
      text: "Message",
      search: false,
    },
    {
      dataField: "value",
      text: "Value",
      search: false,
    },
    {
      dataField: "created_at",
      text: "Timestamp",
      sort: true,
      formatter: (cell: any, row: any) => {
        return formatTimestamp(row.created_at)
      },
      search: false,
    },
  ];
  
  const emptyState = () => {
    return (
        <div>
            <div className="p-5 mb-4 rounded-3" style={{background: '#f1f1f1'}}>
              <div className="container-fluid py-5">
                <h1 className="display-5 fw-bold">No issues yet!</h1>
                <p className="col-md-8 fs-4">Anomalies or issues that occur will show up here.</p>
                <br/>
              </div>
            </div>
        </div>
     )
  };

  const loadingState = () => (
    <div className="p-5 mb-4 rounded-3" style={{background: '#f1f1f1'}}>
      <div className="container-fluid py-5">
        <h1 className="display-5 fw-bold">Loading issues</h1>
        <p className="col-md-8 fs-4">This may take a few seconds.</p>
      </div>
    </div>
  );

  if(isLoading) {
    return loadingState();
  } else if (issues.length === 0) {
    return emptyState();
  } else {
    return(
      <ToolkitProvider
          keyField="id"
          data={issues}
          columns={columns}
          >
          {
            props => (
                  <div>
                    <div style={{paddingBottom: 10}} className={'float-end'}>
                      <Search.SearchBar { ...props.searchProps } />
                    </div>
                    <div className="mt-4 table-responsive custom-table custom-table-responsive">
                      <BootstrapTable
                        { ...props.baseProps }
                        bordered={false}
                        pagination={issues.length < 10 ? undefined : paginationFactory({ sizePerPage: 10 })}
                      />
                    </div>
                  </div>

            )
          }
        </ToolkitProvider>
    );
  }


};

export default IssuesTable;

