import React, { useState, useEffect } from 'react';

import { ArrowRepeat } from 'react-bootstrap-icons';
import BootstrapTable from "react-bootstrap-table-next";
import paginationFactory from "react-bootstrap-table2-paginator";

import { ToastContainer, Toast } from 'react-bootstrap';

import datasourceService from 'services/datasources';
import { formatTimestamp } from 'utils/timestampFormatting';

const SourcesTable: React.FC = () => {
  const [toastVisible, setToastVisible] = useState<boolean>(false);
  const [datasources, setDatasources] = useState<any[]>([]);

  useEffect(() => {
    async function loadDatasources() {
      let res = await datasourceService.getAll();
      if (res !== null && res.datasources) {
        setDatasources(res.datasources);
      }
    }
    loadDatasources();
  }, []);

  const handleTest = (ds_id: number) => {
    setToastVisible(true);
    async function testDatasource(ds_id: any) {
        let res = await datasourceService.test(ds_id);
        if (res !== null && res.datasource) {
          if (res.datasource.connection) {
            alert("Connection was successful.");
          } else {
            alert("Connection was unsuccessful.");
          }
        } else {
          alert("Connection was unsuccessful.");
        }
        setToastVisible(false);
    }
    testDatasource(ds_id);
  }

  const handleDelete = (ds_id: any) => {
    async function deleteDatasource(ds_id: string) {
        let res = await datasourceService.delete(ds_id);
        if (res !== null && res.datasource) {
          // success
        } else {
          //fail
        }
    }
    deleteDatasource(ds_id);
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
               <span style={{textDecoration: 'none'}}>{row.name}</span>
               <small className="d-block">{row.description}</small>
            </div>
         )
      }
    },
    {
      dataField: "created_at",
      text: "Created At",
      formatter: (cell: any, row: any) => {
        return formatTimestamp(row.created_at)
      },
    },
    {
      text: "",
      dataField: "id",
      formatter: (cell: any, row: any) => {
        return (
          <div className="btn-group">
                  <button 
                    onClick={() => handleTest(row.id)} 
                    type="button" 
                    className="btn btn-sm btn-outline-secondary"
                    disabled={process.env.REACT_APP_IS_DEMO === 'true'}
                  >
                        Test
                  </button>
                  <button 
                    onClick={() => handleDelete(row.id)}
                    type="button" 
                    className="btn btn-sm btn-outline-danger"
                    disabled={process.env.REACT_APP_IS_DEMO === 'true'}
                  >
                        Delete
                  </button>
          </div>
        );
      },
    },
  ];

  const SourceToasts = () => (
    <ToastContainer position={"top-end"} style={{paddingTop: 10}}>
      <Toast onClose={() => setToastVisible(false)}>
        <Toast.Header>
          <ArrowRepeat className="bi" width="24" height="24"/>
          <strong className="me-auto" style={{paddingLeft: 12}}>Testing Connection</strong>
        </Toast.Header>
      </Toast>
    </ToastContainer>
  );

  const emptyState = () => {
    return (
      <div className="p-4 py-2 mb-4 rounded-3" style={{background: '#f1f1f1'}}>
        <div className="container-fluid py-5">
          <h1 className="display-7 fw-bold">No data sources yet.</h1>
          <p className="col-md-10 fs-4">Set up a data source to start monitoring.</p>
        </div>
      </div>
    )
  }

  if (datasources.length == 0) { return emptyState() }

  return (
   <div className="table-responsive custom-table custom-table-responsive">
     <BootstrapTable
       keyField="id"
       data={datasources}
       columns={columns}
       bordered={false}
       pagination={paginationFactory({ sizePerPage: 10 })}
     />
     {toastVisible && <SourceToasts />}
   </div>
  );
}

export default SourcesTable;
