import React, { useState, useEffect } from 'react';
import {
  EuiFlexGroup,
  EuiFlexItem,
  EuiFormRow,
  EuiHeaderLogo,
  EuiButton,
  EuiSuperSelect,
  EuiFieldText,
  EuiFieldPassword,
  EuiSpacer,
  EuiFlexGrid,
  EuiCard,
  EuiIcon,
  EuiHorizontalRule,
  EuiPageHeader,
} from '@elastic/eui';

import datasourceService from 'services/datasources';

const WarehouseForm = () => {
  // const [availDatasources, setAvailDatasources] = useState([]);
  const [datasourceType, setDatasourceType] = useState('snowflake');
  const [datasourceName, setDatasourceName] = useState('');

  const [account, setAccount] = useState('');
  const [user, setUser] = useState('');
  const [password, setPassword] = useState('');
  const [warehouse, setWarehouse] = useState('');
  const [database, setDatabase] = useState('');
  
  const [host, setHost] = useState('');
  const [port, setPort] = useState('');

  const submitForm = async () => {
    let body;
    if (datasourceType == "snowflake") {
    body = {
      name: datasourceName,
      type: datasourceType,
      configuration: {
        driver: datasourceType,
        account: account,
        user: user,
        password: password,
        warehouse: warehouse,
        database: database,
      },
    };
    } else if (datasourceType == "postgres") {
    body = {
      name: datasourceName,
      type: datasourceType,
      configuration: {
        user: user,
        password: password,
        host: host,
        port: parseInt(port),
        database: database,
      },
    };
    }
    await datasourceService.create(body);

    window.location.reload();
  };

  // useEffect(() => {
  //   async function loadDatasourceTypes() {
  //     let res = await datasourceTypeService.getAll();

  //     if (res !== null && res.datasource_types) {
  //       setAvailDatasources(res.datasource_types);
  //     }
  //   }
  //   loadDatasourceTypes();
  // }, []);

  const onChange = (value: any) => {
    setDatasourceType(value);
  };

  return (
    <div>
      <EuiFlexGrid columns={3}>
        <EuiFlexItem>
          <EuiCard
            icon={<EuiIcon type="snowflake" size="xl" />}
            selectable={{
              onClick: () => onChange("snowflake"),
              isSelected: datasourceType == "snowflake",
              isDisabled: false,
            }}
            title="Snowflake"
            description="Connect to Snowflake Data Warehouse"
          />
        </EuiFlexItem>
        <EuiFlexItem>
          <EuiCard
            selectable={{
              onClick: () => onChange("postgres"),
              isSelected: datasourceType == "postgres",
              isDisabled: false,
            }}
            icon={<EuiIcon type="logoPostgres" size="xl" />}
            title="PostgreSQL"
            description="Connect to PostgreSQL Database"
          />
        </EuiFlexItem>
        <EuiFlexItem>
          <EuiCard
            isDisabled
            selectable={{
              onClick: undefined,
              isSelected: false,
              isDisabled: true,
            }}
            icon={<EuiIcon type="logoGoogleG" size="xl" />}
            title="BigQuery"
            description="Connect to Google BigQuery Data Warehouse"
          />
        </EuiFlexItem>
        <EuiFlexItem>
          <EuiCard
            isDisabled
            selectable={{
              onClick: undefined,
              isSelected: false,
              isDisabled: true,
            }}
            icon={<EuiIcon type='logoAWS' size="xl" />}
            title="Redshift"
            description="Connect to AWS Redshift Data Warehouse"
          />
        </EuiFlexItem>
      </EuiFlexGrid>

      <EuiHorizontalRule />

        {datasourceType == "postgres" && <div>
              <EuiPageHeader
                iconType="logoPostgres"
                pageTitle="PostgreSQL"
                description="Connect to PostgreSQL Database"
              />
              <EuiHorizontalRule />
              <EuiFormRow label="Name for Data Source">
                <EuiFieldText
                  placeholder="Company Data Warehouse"
                  onChange={(e) => setDatasourceName(e.target.value)}
                  value={datasourceName}
                />
              </EuiFormRow>
              <EuiFormRow label="User">
                <EuiFieldText
                  placeholder="MONOSI_USER"
                  onChange={(e) => setUser(e.target.value)}
                  value={user}
                />
              </EuiFormRow>
              <EuiFormRow label="Password">
                <EuiFieldPassword
                  placeholder="password123"
                  onChange={(e) => setPassword(e.target.value)}
                  value={password}
                />
              </EuiFormRow>
              <EuiFormRow label="Host">
                <EuiFieldText
                  placeholder="host"
                  onChange={(e) => setHost(e.target.value)}
                  value={host}
                />
              </EuiFormRow>
              <EuiFormRow label="Port">
                <EuiFieldText
                  placeholder="5432"
                  onChange={(e) => setPort(e.target.value)}
                  value={port}
                />
              </EuiFormRow>
              <EuiFormRow label="Database">
                <EuiFieldText
                  placeholder="SNOWFLAKE_SAMPLE_DATA"
                  onChange={(e) => setDatabase(e.target.value)}
                  value={database}
                />
              </EuiFormRow>
        </div>}
        {datasourceType == "snowflake" && <div>
              <EuiPageHeader
                iconType="snowflake"
                pageTitle="Snowflake"
                description="Connect to Snowflake Data Warehouse"
              />
              <EuiHorizontalRule />
              <EuiFormRow label="Name for Data Source">
                <EuiFieldText
                  placeholder="Company Data Warehouse"
                  onChange={(e) => setDatasourceName(e.target.value)}
                  value={datasourceName}
                />
              </EuiFormRow>
              <EuiFormRow label="Account">
                <EuiFieldText
                  placeholder="abc123"
                  onChange={(e) => setAccount(e.target.value)}
                  value={account}
                />
              </EuiFormRow>
              <EuiFormRow label="Warehouse">
                <EuiFieldText
                  placeholder="COMPUTE_WH"
                  onChange={(e) => setWarehouse(e.target.value)}
                  value={warehouse}
                />
              </EuiFormRow>
              <EuiFormRow label="User">
                <EuiFieldText
                  placeholder="MONOSI_USER"
                  onChange={(e) => setUser(e.target.value)}
                  value={user}
                />
              </EuiFormRow>
              <EuiFormRow label="Password">
                <EuiFieldPassword
                  placeholder="password123"
                  onChange={(e) => setPassword(e.target.value)}
                  value={password}
                />
              </EuiFormRow>
              <EuiFormRow label="Database">
                <EuiFieldText
                  placeholder="SNOWFLAKE_SAMPLE_DATA"
                  onChange={(e) => setDatabase(e.target.value)}
                  value={database}
                />
              </EuiFormRow>
        </div>}

      <EuiFlexGroup justifyContent="flexEnd">
        <EuiButton
          fill
          style={{ justifyContent: 'flex-end' }}
          onClick={submitForm}
        >
          Save
        </EuiButton>
      </EuiFlexGroup>
    </div>
  );
};

export default WarehouseForm;
