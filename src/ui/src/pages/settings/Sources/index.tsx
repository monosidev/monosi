import React, { useState, useEffect } from "react";

import {
  CpuFill,
  Collection,
  ArrowRepeat,
  CloudDownloadFill,
  PersonCircle,
} from "react-bootstrap-icons";
import BootstrapTable from "react-bootstrap-table-next";
import paginationFactory from "react-bootstrap-table2-paginator";

import datasourceService from "services/datasources";
import Page from "components/Page";

import Flyout from "components/Flyout";
import DatasourceForm from "components/forms/DatasourceForm";
import { ToastContainer, Toast } from "react-bootstrap";
import { format } from "date-fns";
import { formatTimestamp } from "utils/timestampFormatting";
import { toast } from "sonner";

const SourcesSettings: React.FC = () => {
  const [datasources, setDatasources] = useState<any[]>([]);
  const [testLoading, setTestLoading] = useState<boolean>(false);
  // TODO: Componentize this
  const [toastVisible, setToastVisible] = useState<boolean>(false);

  let flyout = <Flyout name="Data Source" form={<DatasourceForm />} />;

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
    setTestLoading(true);
    setToastVisible(true);
    async function testDatasource(ds_id: any) {
      let res = await datasourceService.test(ds_id);
      if (res !== null && res.datasource) {
        if (res.datasource.connection) {
          toast.success("Connection was successful.");
          // alert("Connection was successful.");
        } else {
          toast.error("Connection was unsuccessful.");
          // alert("Connection was unsuccessful.");
        }
      } else {
        toast.error("Connection was unsuccessful.");
        // alert("Connection was unsuccessful.");
      }
      setTestLoading(false);
      setToastVisible(false);
    }
    testDatasource(ds_id);
  };

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
  };

  const columns = [
    {
      dataField: "status",
      text: "Status",
      formatter: (cell: any, row: any) => {
        return <span className="badge rounded-pill bg-success">Enabled</span>;
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
            <span style={{ textDecoration: "none" }}>{row.name}</span>
            <small className="d-block">{row.description}</small>
          </div>
        );
      },
    },
    {
      dataField: "created_at",
      text: "Created At",
      formatter: (cell: any, row: any) => {
        return formatTimestamp(row.created_at);
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
              disabled={process.env.REACT_APP_IS_DEMO === "true"}
            >
              Test
            </button>
            <button
              onClick={() => handleDelete(row.id)}
              type="button"
              className="btn btn-sm btn-outline-danger"
              disabled={process.env.REACT_APP_IS_DEMO === "true"}
            >
              Delete
            </button>
          </div>
        );
      },
    },
  ];

  const SourceToasts = () => (
    <ToastContainer position={"top-end"} style={{ paddingTop: 10 }}>
      <Toast onClose={() => setToastVisible(false)}>
        <Toast.Header>
          <ArrowRepeat className="bi" width="24" height="24" />
          <strong className="me-auto" style={{ paddingLeft: 12 }}>
            Testing Connection
          </strong>
        </Toast.Header>
      </Toast>
    </ToastContainer>
  );

  return (
    <Page selectedTab="settings">
      <div style={{ paddingLeft: 96 }} className="bg-light">
        <div className="container">
          <main className="col-md-12 ms-sm-auto col-lg-12">
            <div className="container">
              <div className="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
                <h1 className="h2">Settings</h1>
                <div className="btn-toolbar mb-2 mb-md-0"></div>
              </div>
              <div className="d-flex align-items-start">
                <div
                  className="nav flex-column nav-pills me-3 col-md-3"
                  id="v-pills-tab"
                  role="tablist"
                  aria-orientation="vertical"
                >
                  <div className="list-group">
                    <a
                      href="/settings/profile"
                      className="list-group-item list-group-item-action"
                      aria-current="true"
                    >
                      <div className="d-flex w-100">
                        <PersonCircle className="bi" width="24" height="24" />
                        <h5 className="mb-1 mx-3">Profile</h5>
                      </div>
                      <small className="text-muted">Edit account details</small>
                    </a>
                    <a
                      href="/settings/sources"
                      className="list-group-item list-group-item-action active"
                    >
                      <div className="d-flex w-100">
                        <CloudDownloadFill
                          className="bi"
                          width="24"
                          height="24"
                        />
                        <h5 className="mb-1 mx-3">Data Sources</h5>
                      </div>
                      <small>Manage connected data sources</small>
                    </a>
                    <a
                      href="/settings/integrations"
                      className="list-group-item list-group-item-action"
                    >
                      <div className="d-flex w-100">
                        <Collection className="bi" width="24" height="24" />
                        <h5 className="mb-1 mx-3">Integrations</h5>
                      </div>
                      <small className="text-muted">
                        Manage third-party connections
                      </small>
                    </a>
                  </div>
                </div>
                <div className="tab-content w-100 mx-4" id="v-pills-tabContent">
                  <div
                    className="tab-pane fade show active"
                    id="v-pills-home"
                    role="tabpanel"
                    aria-labelledby="v-pills-home-tab"
                  >
                    <div className="d-flex flex-wrap justify-content-center">
                      <form className="col-12 col-lg-auto mb-2 mb-lg-0 me-lg-auto">
                        <h2>Data Sources</h2>
                      </form>
                      <div className="text-end">{flyout}</div>
                    </div>
                    <hr className="mb-4" />
                    <div className="table-responsive custom-table custom-table-responsive">
                      <BootstrapTable
                        keyField="id"
                        data={datasources}
                        columns={columns}
                        bordered={false}
                        pagination={paginationFactory({ sizePerPage: 10 })}
                      />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </main>
        </div>
      </div>
      {toastVisible && <SourceToasts />}
    </Page>
  );
};

export default SourcesSettings;
