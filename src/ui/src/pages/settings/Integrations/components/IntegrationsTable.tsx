import React, { useState, useEffect } from 'react';

import { CloudDownloadFill, PersonCircle, Tools } from 'react-bootstrap-icons';
import BootstrapTable from "react-bootstrap-table-next";
import paginationFactory from "react-bootstrap-table2-paginator";

import BootstrapPage from 'components/BootstrapPage';
import IntegrationService from 'services/integrations';

import { format } from 'date-fns';

const IntegrationsTable: React.FC = () => {
  const [integrations, setIntegrations] = useState([]);


  useEffect(() => {
    async function loadIntegrations() {
      let res = await IntegrationService.getAll();
      if (res !== null && res.integrations) {
        setIntegrations(res.integrations);
      }
    }
    loadIntegrations();
  }, []);

  const handleDelete = (id: any) => {
    async function deleteIntegration(id: string) {
        let res = await IntegrationService.delete(id);
        if (res !== null && res.datasource) {
          // success
        } else {
          //fail
        }
    }
    deleteIntegration(id);
    window.location.reload();
  }


  const columns = [
    {
      dataField: "status",
      text: "Status",
      formatter: (cell: any, row: any) => {
        return (
          <span className="badge rounded-pill bg-success">Enabled</span>
        );
      },
    },
    {
      dataField: "type",
      text: "Type",
    },
    {
      dataField: "name",
      text: "Name",
      formatter: (cell: any, row: any) => {
         return (
            <div>
               <a href="#" style={{textDecoration: 'none'}}>{row.name}</a>
               <small className="d-block">{row.description}</small>
            </div>
         )
      }
    },
    {
      dataField: "created_at",
      text: "Created At",
      formatter: (cell: any, row: any) => {
        return format(new Date(row.created_at), 'eeee, dd MMMM HH:mm:ss');
      },
    },
    {
      text: "",
      dataField: "id",
      formatter: (cell: any, row: any) => {
        return (
          <button
            onClick={() => handleDelete(row.id)}
            type="button" 
            className="btn btn-sm btn-outline-danger"
            disabled={process.env.REACT_APP_IS_DEMO === 'true'}
          >
              Delete
          </button>
        );
      },
    },
  ];

  const emptyState = () => {
    return (
      <div className="p-4 py-2 mb-4 rounded-3" style={{background: '#f1f1f1'}}>
        <div className="container-fluid py-5">
          <h1 className="display-7 fw-bold">No integrations yet.</h1>
          <p className="col-md-10 fs-4">Set up an integration to get alerts.</p>
        </div>
      </div>
    )
  }

  if (integrations.length == 0) { return emptyState() }

  return (
   <div className="table-responsive custom-table custom-table-responsive">
     <BootstrapTable
       keyField="id"
       data={integrations}
       columns={columns}
       bordered={false}
       pagination={paginationFactory({ sizePerPage: 10 })}
     />
   </div>
  );
}

export default IntegrationsTable;
