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

enum DataSourceTypes {
  SNOWFLAKE = 'snowflake',
  POSTGRESQL = 'postgresql',
  REDSHIFT = 'redshift',
}

const DatasourceForm = () => {
  const [datasourceType, setDatasourceType] = useState<DataSourceTypes>(
    DataSourceTypes.SNOWFLAKE
  );
  const [datasourceName, setDatasourceName] = useState<string>('');

  const [account, setAccount] = useState<string>('');
  const [user, setUser] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [warehouse, setWarehouse] = useState<string>('');
  const [database, setDatabase] = useState<string>('');
  const [schema, setSchema] = useState<string>('');
  const [host, setHost] = useState<string>('');
  const [port, setPort] = useState<string>('');

  const submitForm = async () => {
    let body;
    if (datasourceType === DataSourceTypes.SNOWFLAKE) {
      body = {
        name: datasourceName,
        type: datasourceType,
        config: {
          driver: datasourceType,
          account: account,
          user: user,
          password: password,
          warehouse: warehouse,
          database: database,
          schema: schema,
        },
      };
    } else if (
      datasourceType === DataSourceTypes.POSTGRESQL ||
      datasourceType === DataSourceTypes.REDSHIFT
    ) {
      body = {
        name: datasourceName,
        type: datasourceType,
        config: {
          user: user,
          password: password,
          host: host,
          port: parseInt(port),
          database: database,
          schema: schema
        },
      };
    }
    await datasourceService.create(body);

    window.location.reload();
  };

  const onChange = (value: any) => {
    setDatasourceType(value);
  };

  return (
    <div>
      <EuiFlexGrid columns={3}>
        <EuiFlexItem>
          <EuiCard
            icon={<EuiIcon type={DataSourceTypes.SNOWFLAKE} size="xl" />}
            selectable={{
              onClick: () => onChange(DataSourceTypes.SNOWFLAKE),
              isSelected: datasourceType === DataSourceTypes.SNOWFLAKE,
              isDisabled: false,
            }}
            title="Snowflake"
            description="Connect to Snowflake Data Warehouse"
          />
        </EuiFlexItem>
        <EuiFlexItem>
          <EuiCard
            selectable={{
              onClick: () => onChange(DataSourceTypes.POSTGRESQL),
              isSelected: datasourceType === DataSourceTypes.POSTGRESQL,
              isDisabled: false,
            }}
            icon={<EuiIcon type="logoPostgres" size="xl" />}
            title="PostgreSQL"
            description="Connect to PostgreSQL Database"
          />
        </EuiFlexItem>
        <EuiFlexItem>
          <EuiCard
            selectable={{
              onClick: () => onChange(DataSourceTypes.REDSHIFT),
              isSelected: datasourceType === DataSourceTypes.REDSHIFT,
              isDisabled: false,
            }}
            icon={<EuiIcon type="logoAWS" size="xl" />}
            title="Redshift"
            description="Connect to AWS Redshift Data Warehouse"
          />
        </EuiFlexItem>
      </EuiFlexGrid>

      <EuiHorizontalRule />

      {datasourceType === DataSourceTypes.POSTGRESQL && (
        <div>
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
              placeholder="postgres"
              onChange={(e) => setDatabase(e.target.value)}
              value={database}
            />
          </EuiFormRow>
          <EuiFormRow label="Schema">
            <EuiFieldText
              placeholder="public"
              onChange={(e) => setSchema(e.target.value)}
              value={schema}
            />
          </EuiFormRow>
        </div>
      )}
      {datasourceType === DataSourceTypes.REDSHIFT && (
        <div>
          <EuiPageHeader
            iconType="logoAWS"
            pageTitle="Redshift"
            description="Connect to Redshift Data Warehouse"
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
              placeholder="5439"
              onChange={(e) => setPort(e.target.value)}
              value={port}
            />
          </EuiFormRow>
          <EuiFormRow label="Database">
            <EuiFieldText
              placeholder="dev"
              onChange={(e) => setDatabase(e.target.value)}
              value={database}
            />
          </EuiFormRow>
          <EuiFormRow label="Schema">
            <EuiFieldText
              placeholder="public"
              onChange={(e) => setSchema(e.target.value)}
              value={schema}
            />
          </EuiFormRow>
        </div>
      )}
      {datasourceType === DataSourceTypes.SNOWFLAKE && (
        <div>
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
          <EuiFormRow label="Schema">
            <EuiFieldText
              placeholder="tpch_sf1000"
              onChange={(e) => setSchema(e.target.value)}
              value={schema}
            />
          </EuiFormRow>
        </div>
      )}

      <EuiSpacer />

      <div>
        <EuiFormRow>
          <EuiButton
            fill
            onClick={submitForm}
            disabled={process.env.REACT_APP_IS_DEMO === 'true'}
          >
            Save
          </EuiButton>
        </EuiFormRow>
      </div>
    </div>
  );
};

export default DatasourceForm;
