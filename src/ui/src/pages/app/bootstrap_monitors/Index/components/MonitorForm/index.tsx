import React, { useState, useEffect } from 'react';

import { Form, Button } from 'react-bootstrap';


import datasourceService from 'services/datasources';
import MonitorService from 'services/monitors';

const MonitorForm: React.FC = () => {
  const [datasources, setDatasources] = useState([]);
  useEffect(() => {
    async function loadDatasources() {
      let res = await datasourceService.getAll();
      if (res !== null && res.datasources) {
        setDatasources(res.datasources);
      }
    }
    loadDatasources();
  }, []);

  // FORM VALUES
  const [datasource, setDatasource] = useState<any>(null);
  const [type, setType] = useState<any>('table_health');
  const [database, setDatabase] = useState<any>('');
  const [schema, setSchema] = useState<any>('');
  const [daysAgo, setDaysAgo] = useState<any>(100);
  const [table, setTable] = useState<any>('');
  const [timestampField, setTimestampField] = useState<any>('');

  const handleClick = async () => {
    const body = {
      workspace: 'default',
      source: datasource,
      type: type,
      days_ago: daysAgo,
      database: database,
      schema: schema,
      table_name: table,
      timestamp_field: timestampField,
    };
    const resp = await MonitorService.create(body);

    window.location.reload(); // TODO: Fix - dirty
  };

  const handleDatasourceChange = (name: string) => {
    setDatasource(name);
    datasources.forEach((ds: any) => {
        if (ds.name == name) {
          setDatabase(ds.config.database);
          setSchema(ds.config.schema);
        }
    })
  }

  return (
      <Form>
        <Form.Group className="mb-3" controlId="formBasicDatasource">
          <Form.Label>Data Source</Form.Label>
          <Form.Select aria-label="Datasource" onChange={(e: any) => handleDatasourceChange(e.target.value)}>
            <option>Choose a data source</option>
            {datasources.map((el: any) => {
              return (<option value={el.name}>{el.name}</option>);
            })}
          </Form.Select>
        </Form.Group>

        <Form.Group className="mb-3" controlId="formBasicType">
          <Form.Label>Type</Form.Label>
          <Form.Select aria-label="Monitor Type" onChange={(e: any) => setType(e.target.value)}>
            <option value="table_health">Table Health</option>
          </Form.Select>
        </Form.Group>

        <Form.Group className="mb-3" controlId="formBasicDatabase">
          <Form.Label>Database</Form.Label>
          <Form.Control type="text" placeholder="SNOWFLAKE_SAMPLE_DATA" disabled value={database} />
        </Form.Group>

        <Form.Group className="mb-3" controlId="formBasicSchema">
          <Form.Label>Schema</Form.Label>
          <Form.Control type="text" placeholder="TPCH_SF1000" disabled value={schema} />
        </Form.Group>

        <Form.Group className="mb-3" controlId="formBasicSchema">
          <Form.Label>Lookback Days (# Days Ago to Fetch)</Form.Label>
          <Form.Control type="number" value={daysAgo} onChange={(e: any) => setDaysAgo(e.target.value)} />
        </Form.Group>

        <Form.Group className="mb-3" controlId="formBasicTableName">
          <Form.Label>Table</Form.Label>
          <Form.Control type="text" placeholder="ORDERS" value={table} onChange={(e: any) => setTable(e.target.value)} />
          <Form.Text className="text-muted">
              Tables should be available in the database and schema specified for the data source.
          </Form.Text>
        </Form.Group>

        <Form.Group className="mb-3" controlId="formBasicTimestampField">
          <Form.Label>Timestamp Field</Form.Label>
          <Form.Control type="text" placeholder="o_orderdate" value={timestampField} onChange={(e: any) => setTimestampField(e.target.value)} />
          <Form.Text className="text-muted">
              Timestamp field should be a column name in the above table of the date/time type.
          </Form.Text>
        </Form.Group>

        <Button 
          variant="primary"
          onClick={handleClick}
          disabled={process.env.REACT_APP_IS_DEMO === 'true'}
          >
          Submit
        </Button>
      </Form>
  );
};

export default MonitorForm;
